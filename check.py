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

        # Check Host URL
        checkhost_url = f"https://check-host.net/ip-info?host={ip_address}"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Python Script)"}
        
        # Попытка использовать check-host.net
        response = requests.get(checkhost_url, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"\n[DEBUG] Ответ check-host.net (первые 200 символов):\n{response.text[:200]}\n")
            try:
                data = response.json()
                if data:
                    return process_checkhost_data(data)
                else:
                    print("Ошибка: check-host.net вернул пустой ответ, пробуем альтернативный сервис.")
            except ValueError:
                print(f"Ошибка: Сервер вернул некорректный JSON, возможно блокировка или капча.")
        else:
            print(f"Ошибка: Сервер check-host.net вернул статус-код {response.status_code}. Пробуем альтернативный сервис.")
        
        # Если check-host не дал ответа, используем альтернативные сервисы
        return use_alternate_services(ip_address)

    except socket.gaierror:
        print("Ошибка: Невозможно получить IP для указанного домена.")
        exit()
    except requests.RequestException as e:
        print(f"Ошибка: Не удалось подключиться к check-host.net или альтернативным сервисам ({e})")
        exit()

# Обработка данных от check-host.net
def process_checkhost_data(data):
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

# Использование альтернативных сервисов
def use_alternate_services(ip_address):
    # Используем ipinfo.io API для получения информации о IP
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

    # В случае неудачи, пробуем ipapi.com
    ipapi_url = f"https://api.ipapi.com/{ip_address}?access_key=YOUR_ACCESS_KEY"
    try:
        response = requests.get(ipapi_url, timeout=10)
        if response.status_code == 200:
            print(f"\n[INFO] Получена информация с ipapi.com")
            data = response.json()

            country = data.get('country_name', 'Неизвестно')
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
            print(f"Ошибка: Не удалось получить данные с ipapi.com (статус {response.status_code}).")
            return None
    except requests.RequestException as e:
        print(f"Ошибка при подключении к ipapi.com: {e}")
        return None

# Обнаружение DDoS-защиты
def detect_ddos_protection(org, isp):
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

# Сканирование портов
def scan_port(ip, port, open_ports):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    if sock.connect_ex((ip, port)) == 0:
        open_ports.append(port)
        print(f"Порт {port} открыт")
    sock.close()

def scan_ports(ip, start_port, end_port):
    print(f"Сканирование портов {start_port}-{end_port} на {ip}...\n")
    open_ports = []
    threads = []

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(ip, port, open_ports))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nОткрытые порты:")
    if open_ports:
        for port in open_ports:
            print(f"- Порт {port}")
    else:
        print("Открытые порты не найдены")

# Получение DNS-записей
def get_dns_records(domain):
    print("\nDNS-записи:")
    try:
        # Получение A-записей через socket
        a_records = socket.getaddrinfo(domain, None)
        for record in a_records:
            if record[1] == socket.SOCK_STREAM:
                print(f"A-запись: {record[4][0]}")
    except socket.gaierror as e:
        print(f"Ошибка при получении DNS-записей: {e}")

# Проверка пинга с разных стран
def check_ping_from_countries(ip):
    print("\nПроверка пинга с разных стран (через check-host.net):")
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Python Script)"}

    try:
        response = requests.get(f"https://check-host.net/check-ping?host={ip}", headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"Ошибка при запуске пинга (код {response.status_code}).")
            return

        check_id = response.json().get("request_id")
        time.sleep(5)

        result_response = requests.get(f"https://check-host.net/check-result/{check_id}", headers=headers, timeout=10).json()

        for location, data in result_response.items():
            if isinstance(data, list):
                pings = [x[1] for x in data if x[1] is not None]
                if pings:
                    avg_ping = sum(pings) / len(pings)
                    print(f"{location}: {avg_ping:.2f} мс")
                else:
                    print(f"{location}: Нет данных")
            else:
                print(f"{location}: Нет данных")

    except requests.RequestException as e:
        print(f"Ошибка при подключении к check-host.net ({e})")

# Основной блок
