import socket
import requests
import concurrent.futures
import time
import socks  # нужно установить через pip install PySocks
from urllib.parse import urlparse

# Определяем тип прокси по URL
def detect_proxy_type(url):
    url = url.lower()
    if 'socks4' in url:
        return 'socks4'
    elif 'socks5' in url:
        return 'socks5'
    else:
        return 'http'  # Если не указано, считаем что http/https

# Проверка прокси через прямое соединение
def check_proxy(proxy, proxy_type):
    host, port = proxy.split(":")
    port = int(port)

    start_time = time.time()

    try:
        if proxy_type in ['socks4', 'socks5']:
            s = socks.socksocket()
            if proxy_type == 'socks4':
                s.set_proxy(socks.SOCKS4, host, port)
            else:
                s.set_proxy(socks.SOCKS5, host, port)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(60)
        s.connect(("1.1.1.1", 80))  # Проверяем соединение с Cloudflare DNS
        s.close()

        response_time = time.time() - start_time

        if response_time <= 60:
            print(f"[{proxy_type}] Рабочий ({response_time:.2f} сек): {proxy}")
            return proxy
        else:
            print(f"[{proxy_type}] Слишком медленный ({response_time:.2f} сек): {proxy}")

    except Exception as e:
        return None

# Загрузка списка ссылок из ProxyLists.txt
def load_proxy_links(filename="ProxyLists.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Загрузка всех прокси из всех ссылок
def get_proxies_from_links(links):
    all_proxies = []
    for link in links:
        proxy_type = detect_proxy_type(link)

        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().splitlines()
                for proxy in proxies:
                    all_proxies.append((proxy, proxy_type))
        except Exception as e:
            print(f"Не удалось загрузить с {link}: {e}")

    return all_proxies

# Основная функция
def main():
    links = load_proxy_links("ProxyLists.txt")
    proxies_with_types = get_proxies_from_links(links)

    checked_proxies = set()

    # Используем ProcessPoolExecutor для полной нагрузки на процессор
    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_proxy = {
            executor.submit(check_proxy, proxy, proxy_type): proxy
            for proxy, proxy_type in proxies_with_types
        }

        for future in concurrent.futures.as_completed(future_to_proxy):
            result = future.result()
            if result:
                checked_proxies.add(result)

    # Сохраняем только IP:PORT
    with open("gg.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(checked_proxies))

    print(f"✅ Сохранено {len(checked_proxies)} рабочих прокси в gg.txt (отклик до 60 секунд)")

if __name__ == "__main__":
    main()
