import requests
import re

# Файл с ссылками
input_file = "ProxyLists.txt"

# Регулярное выражение для поиска прокси
proxy_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b')

# Список для хранения всех прокси
all_proxies = []

# Чтение ссылок из файла
try:
    with open(input_file, 'r') as file:
        urls = file.read().splitlines()
except FileNotFoundError:
    print(f"Файл {input_file} не найден. Убедитесь, что файл существует.")
    exit()

# Проход по всем ссылкам
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            proxies = proxy_pattern.findall(response.text)
            all_proxies.extend(proxies)
            print(f"Найдено {len(proxies)} прокси по ссылке: {url}")
        else:
            print(f"Ошибка: {response.status_code} по ссылке: {url}")
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")

# Удаление дубликатов
unique_proxies = list(set(all_proxies))

# Сохранение в файл gg
with open('gg', 'w') as f:
    for proxy in unique_proxies:
        f.write(proxy + '\n')

print(f"Всего найдено {len(unique_proxies)} уникальных прокси. Результаты сохранены в файл 'gg'.")
