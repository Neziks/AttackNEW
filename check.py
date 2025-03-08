import socket
import threading
import requests
import time

# Функция получения информации о домене или IP
def get_ip_info(target):
    try:
        ip_address = socket.gethostbyname(target)
        print(f"Домен: {target}")
        print(f"IP-адрес: {ip_address}")

        # Проверка check-host.net
        checkhost_url = f"https://check-host.net/ip-info?host={ip_address}"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Python Script)"}
        
        response = requests.get(checkhost_url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                if data:
                    return process_checkhost_data(data, ip_address)  # Передаем ip_address
                else:
                    print("Ошибка: check-host.net вернул пустой ответ.")
            except ValueError:
                print(f"Ошибка: некорректный JSON. Возможно, блокировка или капча.")
                print(response.text[:500])  # Выводим первые 500 символов ответа для диагностики
        else:
            print(f"Ошибка: Сервер check-host.net вернул статус-код {response.status_code}.")

        return use_alternate_services(ip_address)

    except socket.gaierror:
        print("Ошибка: Невозможно получить IP для указанного домена.")
        return None
    except requests.RequestException as e:
        print(f"Ошибка: Не удалось подключиться к check-host.net ({e})")
        return None

# Обработка данных от check-host.net
def process_checkhost_data(data, ip_address):
    country = data.get('country_name', 'Неизвестно')
    city = data.get('city', 'Неизвестно')
    isp = data.get('isp', 'Неизвестно')
    org = data.get('org', 'Неизвестно')
    asn = data.get('as', 'Неизвестно')
    hostname = data.get('hostname', 'Неизвестно')

    ddos_protection = detect_ddos_protection(org, isp)
    protection_rating = get_protection_rating(org, isp)

    print(f"Страна: {country}")
    print(f"Город: {city}")
    print(f"Провайдер: {isp} ({protection_rating})")
    print(f"Организация: {org}")
    print(f"AS: {asn}")
    print(f"Хостнейм: {hostname}")
    print(f"DDoS-защита: {ddos_protection}\n")

    return ip_address

# Альтернативные сервисы
def use_alternate_services(ip_address):
    ipinfo_url = f"https://ipinfo.io/{ip_address}/json"
    try:
        response = requests.get(ipinfo_url, timeout=10)
        if response.status_code == 200:
            print(f"\n[INFO] Получена информация с ipinfo.io")
            data = response.json()

            country = data.get('country', 'Неизвестно')
            city = data.get('city', 'Неизвестно')
            isp = data.get('org', 'Неизвестно')
            hostname = data.get('hostname', 'Неизвестно')

            ddos_protection = detect_ddos_protection(isp, isp)
            protection_rating = get_protection_rating(isp, isp)

            print(f"Страна: {country}")
            print(f"Город: {city}")
            print(f"Провайдер: {isp} ({protection_rating})")
            print(f"Хостнейм: {hostname}")
            print(f"DDoS-защита: {ddos_protection}\n")

            return ip_address
        else:
            print(f"Ошибка: Не удалось получить данные с ipinfo.io (статус {response.status_code}).")
            return None
    except requests.RequestException as e:
        print(f"Ошибка при подключении к ipinfo.io: {e}")
        return None

# Проверка DDoS-защиты
def detect_ddos_protection(org, isp):
    if not org: org = ""
    if not isp: isp = ""

    protection_services = {
        "Cloudflare": "Cloudflare (очень высокая защита)",
        "DDoS-Guard": "DDoS-Guard (высокая защита)",
        "OVH": "OVH (высокая защита)",
        "StormWall": "StormWall (средняя защита)",
        "Path.net": "Path.net (очень высокая защита)",
        "G-Core Labs": "G-Core Labs (средняя защита)",
        "Qrator": "Qrator (высокая защита, РФ)",
        "Selectel": "Selectel (средняя защита, РФ)",
        "Voxility": "Voxility (высокая защита)"
    }
    for name, protection in protection_services.items():
        if name.lower() in org.lower() or name.lower() in isp.lower():
            return protection
    return "Не обнаружено или слабая защита"

# Оценка защиты DDoS
def get_protection_rating(org, isp):
    if not org: org = ""
    if not isp: isp = ""

    rating = {
        "Cloudflare": "★★★★★",
        "DDoS-Guard": "★★★★☆",
        "OVH": "★★★★☆",
        "StormWall": "★★★☆☆",
        "Path.net": "★★★★★",
        "G-Core Labs": "★★★☆☆",
        "Qrator": "★★★★☆",
        "Selectel": "★★★☆☆",
        "Voxility": "★★★★☆"
    }
    for name, stars in rating.items():
        if name.lower() in org.lower() or name.lower() in isp.lower():
            return stars
    return "★☆☆☆☆ (неизвестно)"

# Проверка пинга
def check_ping_from_countries(ip):
    print("\nПроверка пинга с разных стран:")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Python Script)"}

    try:
        response = requests.get(f"https://check-host.net/check-ping?host={ip}", headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Ошибка при запуске пинга (код {response.status_code}).")
            return

        check_id = response.json().get("request_id")
        time.sleep(5)

        result_response = requests.get(f"https://check-host.net/check-result/{check_id}", headers=headers, timeout=10).json()

        if not result_response:  # Добавлена проверка
            print("Ошибка: сервер не вернул данных.")
            return

        for location, data in result_response.items():
            pings = [x[1] for x in data if isinstance(x, list) and x[1] is not None]
            print(f"{location}: {sum(pings) / len(pings):.2f} мс" if pings else f"{location}: Нет данных")

    except requests.RequestException as e:
        print(f"Ошибка при подключении к check-host.net ({e})")
