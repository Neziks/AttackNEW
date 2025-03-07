import requests
import concurrent.futures
import time

# Функция проверки прокси
def check_proxy(proxy, proxy_type):
    url = "http://httpbin.org/ip"  # Можно заменить на любой доступный URL для проверки
    proxies = {
        "http": f"{proxy_type}://{proxy}",
        "https": f"{proxy_type}://{proxy}"
    }

    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies, timeout=60)
        response_time = time.time() - start_time

        if response.status_code == 200:
            if 1 <= response_time <= 60:
                print(f"[{proxy_type}] Подходит ({response_time:.2f} сек): {proxy}")
                return proxy  # Сохраняем только IP:PORT
            else:
                print(f"[{proxy_type}] Не подходит (время: {response_time:.2f} сек): {proxy}")
    except:
        pass

    return None

# Загрузка списка ссылок из ProxyLists.txt
def load_proxy_links(filename="ProxyLists.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Загрузка всех прокси со всех сайтов
def get_proxies_from_links(links):
    proxies = []
    for link in links:
        try:
            response = requests.get(link, timeout=15)
            if response.status_code == 200:
                proxies += response.text.strip().splitlines()
        except Exception as e:
            print(f"Ошибка загрузки с {link}: {e}")
    return proxies

# Основная функция
def main():
    links = load_proxy_links("ProxyLists.txt")
    proxies = get_proxies_from_links(links)

    valid_proxies = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_proxy = {}

        for proxy in proxies:
            for proxy_type in ['http', 'https', 'socks4', 'socks5']:
                future = executor.submit(check_proxy, proxy, proxy_type)
                future_to_proxy[future] = proxy

        for future in concurrent.futures.as_completed(future_to_proxy):
            result = future.result()
            if result and result not in valid_proxies:
                valid_proxies.append(result)

    # Сохраняем только IP:PORT (без протоколов) в gg.txt
    with open("gg.txt", "w", encoding="utf-8") as file:
        file.write("\n".join(valid_proxies))

    print(f"Сохранено {len(valid_proxies)} прокси в gg.txt (отклик от 1 до 60 секунд)")

if __name__ == "__main__":
    main()
