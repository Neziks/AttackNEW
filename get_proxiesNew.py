import requests

# Загружаем ссылки из ProxyLists.txt
def load_proxy_links(filename="ProxyLists.txt"):
    with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Загружаем все прокси из всех ссылок
def fetch_all_proxies(links):
    all_proxies = set()

    for link in links:
        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                proxies = response.text.strip().splitlines()
                all_proxies.update(proxies)
                print(f"Загружено {len(proxies)} прокси с {link}")
            else:
                print(f"Ошибка загрузки с {link}: код {response.status_code}")
        except Exception as e:
            print(f"Не удалось получить прокси с {link}: {e}")

    return all_proxies

# Сохраняем прокси в gg.txt
def save_proxies(proxies, filename="gg.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(proxies))
    print(f"✅ Сохранено {len(proxies)} прокси в {filename}")

# Основная функция
def main():
    links = load_proxy_links("ProxyLists.txt")
    proxies = fetch_all_proxies(links)
    save_proxies(proxies)

if __name__ == "__main__":
    main()
