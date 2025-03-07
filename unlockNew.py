import os
import resource
import subprocess

def set_limits():
    """
    Снятие системных лимитов на количество процессов, открытых файлов и виртуальную память.
    Обработаны ошибки для работы в контейнерах и облачных системах.
    """
    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        new_limit = min(hard, 1000000)
        resource.setrlimit(resource.RLIMIT_NOFILE, (new_limit, new_limit))
    except ValueError as e:
        print(f"⚠️ Не удалось поднять лимит NOFILE: {e}")

    try:
        resource.setrlimit(resource.RLIMIT_NPROC, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    except ValueError as e:
        print(f"⚠️ Не удалось поднять лимит NPROC: {e}")

    try:
        resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    except ValueError as e:
        print(f"⚠️ Не удалось поднять лимит виртуальной памяти: {e}")

def remove_network_limits():
    """
    Улучшение сетевых настроек для максимальной пропускной способности.
    """
    os.system('sysctl -w net.core.somaxconn=65535')
    os.system('sysctl -w net.core.netdev_max_backlog=5000')
    os.system('sysctl -w fs.file-max=1000000')
    os.system('sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"')
    os.system('sysctl -w net.ipv4.tcp_wmem="4096 87380 16777216"')
    os.system('sysctl -w net.ipv4.ip_local_port_range="1024 65535"')
    os.system('sysctl -w net.ipv4.tcp_mtu_probing=1')
    os.system('sysctl -w net.ipv4.tcp_fin_timeout=15')
    os.system('sysctl -w net.ipv4.tcp_keepalive_time=1200')

def remove_iptables_limits():
    """
    Полная очистка iptables и разрешение всего трафика.
    """
    os.system('iptables -F')
    os.system('iptables -P INPUT ACCEPT')
    os.system('iptables -P OUTPUT ACCEPT')
    os.system('iptables -P FORWARD ACCEPT')

def disable_telemetry():
    """
    Отключение телеметрии и систем слежки.
    """
    os.system('systemctl stop apport 2>/dev/null')
    os.system('systemctl disable apport 2>/dev/null')
    os.system('systemctl stop systemd-telemetry 2>/dev/null')
    os.system('systemctl disable systemd-telemetry 2>/dev/null')
    os.system('sysctl -w kernel.dmesg_restrict=1')

def disable_unnecessary_services():
    """
    Отключение ненужных сервисов для улучшения производительности и уменьшения слежки.
    """
    services = [
        "motd-news",
        "snapd",
        "systemd-journald",
        "systemd-modules-load",
        "bluetooth",
        "avahi-daemon",
        "cups",
        "ModemManager",
        "whoopsie"
    ]

    for service in services:
        os.system(f'systemctl stop {service} 2>/dev/null')
        os.system(f'systemctl disable {service} 2>/dev/null')

def disable_snap():
    """
    Отключение snap и очистка snapd.
    """
    os.system('systemctl stop snapd 2>/dev/null')
    os.system('systemctl disable snapd 2>/dev/null')
    os.system('apt-get purge snapd -y 2>/dev/null')
    os.system('rm -rf /snap /var/snap /var/lib/snapd 2>/dev/null')

def apply_all_settings():
    """
    Запуск всех процедур снятия ограничений, отключения слежки и оптимизации сети.
    """
    print("⚙️ Снятие системных лимитов...")
    set_limits()

    print("⚙️ Оптимизация сети...")
    remove_network_limits()

    print("⚙️ Очистка правил iptables...")
    remove_iptables_limits()

    print("⚙️ Отключение телеметрии...")
    disable_telemetry()

    print("⚙️ Отключение ненужных сервисов...")
    disable_unnecessary_services()

    print("⚙️ Отключение snap (если есть)...")
    disable_snap()

    print("✅ Все ограничения сняты, система оптимизирована, слежка отключена.")

if __name__ == "__main__":
    apply_all_settings()
