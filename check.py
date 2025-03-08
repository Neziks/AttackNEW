import socket
import threading
import requests
import time
import argparse

# Функция получения информации о домене или IP
def get_ip_info(target):
    try:
        print(f"[INFO] Получение информации о {target}")
        ip_address = socket.gethostbyname(target)
        print(f"Домен: {target}")
        print(f"IP-адрес: {ip_address}")

        checkhost_url = f"https://check-host.net/ip-info?host={ip_address}"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Python Script)"}
        
        response = requests.get(checkhost_url, headers=headers, timeout=10)
        if response.status_code == 200:
            try:
                data = response.json()
                if data:
                    return process_checkhost_data(data)
                else:
                    print("Ошибка: check-host.net вернул пустой ответ, пробуем альтернативный сервис.")
            except ValueError:
                print("Ошибка: Сервер вернул некорректный JSON, возможно блокировка или капча.")
        else:
            print(f"Ошибка: Сервер check-host.net вернул статус {response.status_code}. Пробуем альтернативные сервисы.")
        
        return use_alternate_services(ip_address)

    except socket.gaierror:
        print("Ошибка: Невозможно получить IP для указанного домена.")
    except requests.RequestException as e:
        print(f"Ошибка сети: {e}")

# Обработка данных от check-host.net
def process_checkhost_data(data):
    country = data.get('country_name', 'Неизвестно')
    city = data.get('city', 'Неизвестно')
    isp = data.get('isp', 'Неизвестно')
    org = data.get('org', 'Неизвестно')

    print(f"Страна: {country}")
    print(f"Город: {city}")
    print(f"Провайдер: {isp}")
    print(f"Организация: {org}")

    return data

# Использование альтернативных сервисов
def use_alternate_services(ip_address):
    ipinfo_url = f"https://ipinfo.io/{ip_address}/json"
    try:
        response = requests.get(ipinfo_url, timeout=10)
        if response.status_code == 200:
            print(f"[INFO] Получена информация с ipinfo.io")
            data = response.json()
            country = data.get('country', 'Неизвестно')
            city = data.get('city', 'Неизвестно')
            isp = data.get('org', 'Неизвестно')

            print(f"Страна: {country}")
            print(f"Город: {city}")
            print(f"Провайдер: {isp}")

            return data
        else:
            print(f"Ошибка: Не удалось получить данные с ipinfo.io (статус {response.status_code}).")
    except requests.RequestException as e:
        print(f"Ошибка при подключении к ipinfo.io: {e}")

    return None

# Сканирование портов
def scan_ports(ip, start_port=1, end_port=1024):
    print(f"[INFO] Сканирование портов {start_port}-{end_port} на {ip}")
    open_ports = []
    threads = []

    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        if sock.connect_ex((ip, port)) == 0:
            open_ports.append(port)
            print(f"Порт {port} открыт")
        sock.close()

    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(port,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("\nОткрытые порты:", open_ports if open_ports else "не найдены")

# Запуск программы
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Анализатор информации об IP и сканер портов.")
    parser.add_argument("target", help="Доменное имя или IP-адрес")
    parser.add_argument("--scan-ports", action="store_true", help="Сканировать порты (1-1024)")

    args = parser.parse_args()

    ip_data = get_ip_info(args.target)
    
    if args.scan_ports and ip_data:
        ip = ip_data.get("ip", args.target)
        scan_ports(ip)
