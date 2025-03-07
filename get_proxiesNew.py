import requests
import concurrent.futures
import time
from urllib.parse import urlparse

# Определяем тип прокси по ссылке
def detect_proxy_type(url):
    if 'socks4' in url.lower():
        return 'socks4'
    elif 'socks5' in url.lower():
        return 'socks5'
    else:
        return 'http'  # Если не явно, считаем http/https

# Проверка одного прокси
def check_proxy(proxy, proxy_type):
    test_url = "http://httpbin.org/ip"
    proxies = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}"
    }

    try:
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=60)
        response_time = time.time() - start_time

        if response.status_code == 200 and 1 <= response_time <= 60:
            print(f"[{proxy_type}] Рабочий ({response_time:.2f} сек): {proxy}")
            return proxy
        else:
            print(f"[{proxy_type}] Пропущен ({response_time:.2f} сек): {proxy}")
    except requests.RequestException:
        pass

    return None

# Загрузка ссылок с сайтов
def load_proxy_links(filename="ProxyLists.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Загрузка всех прокси из всех ссылок
def get_proxies_from_links(links):
    all_proxies = []
    link_protocols = {}

    for link in links:
        proxy_type = detect_proxy_type(link)
        link_protocols[link] = proxy_type

        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().splitlines()
                for proxy in proxies:
                    all_proxies.append((proxy, proxy_type))  # Сохраняем прокси и его тип
        except Exception as e:
            print(f"Ошибка при загрузке с {link}: {e}")

    return all_proxies

# Основная функция
def main():
    links = load_proxy_links("ProxyLists.txt")
    proxies_with_types = get_proxies_from_links(links)

    checked_proxies = set()

    # Многопоточная проверка прокси
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_proxy = {
            executor.submit(check_proxy, proxy, proxy_type): proxy
            for proxy, proxy_type in proxies_with_types
        }

        for future in concurrent.futures.as_completed(future_to_proxy):
            result = future.result()
            if result:
                checked_proxies.add(result)

    # Сохранение уникальных рабочих прокси в файл
    with open("gg.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(checked_proxies))

    print(f"✅ Сохранено {len(checked_proxies)} рабочих прокси в gg.txt (отклик от 1 до 60 секунд)")

if __name__ == "__main__":
    main()
