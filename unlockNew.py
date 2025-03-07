import os
import resource
import subprocess

def set_limits():
    """
    Снятие системных лимитов на количество процессов, открытых файлов и виртуальную память.
    """
    # Снятие лимита на максимальное количество процессов
    resource.setrlimit(resource.RLIMIT_NPROC, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    
    # Снятие лимита на количество открытых файлов
    resource.setrlimit(resource.RLIMIT_NOFILE, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

    # Снятие лимита на виртуальную память
    resource.setrlimit(resource.RLIMIT_AS, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))

def remove_network_limits():
    """
    Снятие сетевых ограничений, улучшение работы сети.
    """
    # Разрешить больше соединений для TCP
    os.system('sysctl -w net.core.somaxconn=65535')
    
    # Увеличить размер очереди для входящих пакетов
    os.system('sysctl -w net.core.netdev_max_backlog=5000')
    
    # Увеличить количество открытых файлов для сетевых соединений
    os.system('sysctl -w fs.file-max=100000')

    # Увеличить размер буферов для сетевых соединений
    os.system('sysctl -w net.ipv4.tcp_rmem="4096 87380 16777216"')
    os.system('sysctl -w net.ipv4.tcp_wmem="4096 87380 16777216"')
    
    # Разрешить использование большого размера буферов для сетевых интерфейсов
    os.system('sysctl -w net.ipv4.ip_local_port_range="1024 65535"')

    # Увеличить максимальный размер пакетов
    os.system('sysctl -w net.ipv4.tcp_mtu_probing=1')
    
    # Установить оптимальные параметры для соединений
    os.system('sysctl -w net.ipv4.tcp_fin_timeout=15')
    os.system('sysctl -w net.ipv4.tcp_keepalive_time=1200')

def remove_iptables_limits():
    """
    Удаление всех правил iptables и разрешение всех входящих и исходящих соединений.
    """
    os.system('iptables -F')  # Очистить все правила
    
    # Разрешить все входящие и исходящие соединения
    os.system('iptables -P INPUT ACCEPT')
    os.system('iptables -P OUTPUT ACCEPT')
    os.system('iptables -P FORWARD ACCEPT')

def disable_telemetry():
    """
    Отключение всех возможных источников телеметрии в системе.
    """
    # Отключить телеметрию Ubuntu/Debian (apport)
    os.system('systemctl stop apport')
    os.system('systemctl disable apport')
    
    # Отключить системную телеметрию
    os.system('systemctl stop systemd-telemetry')
    os.system('systemctl disable systemd-telemetry')
    
    # Отключить телеметрию, связанную с ядром
    os.system('sysctl -w kernel.dmesg_restrict=1')

def disable_unnecessary_services():
    """
    Отключение ненужных сервисов для улучшения производительности.
    """
    # Отключение всех ненужных системных служб, таких как snapd, motd и другие
    os.system('systemctl stop motd-news')
    os.system('systemctl disable motd-news')

    # Отключение snapd, если не используется
    os.system('systemctl stop snapd')
    os.system('systemctl disable snapd')

    # Отключение службы логирования журналов, если она не требуется
    os.system('systemctl stop systemd-journald')
    os.system('systemctl disable systemd-journald')

    # Отключение службы загрузки информации о ядре
    os.system('systemctl stop systemd-modules-load')
    os.system('systemctl disable systemd-modules-load')

    # Отключение других ненужных сервисов по вашему выбору
    os.system('systemctl stop bluetooth')
    os.system('systemctl disable bluetooth')

def apply_all_settings():
    """
    Применение всех настроек: снятие лимитов, улучшение сети, отключение телеметрии и ненужных сервисов.
    """
    # Устанавливаем лимиты
    set_limits()
    
    # Снимаем сетевые ограничения
    remove_network_limits()
    
    # Снимаем правила iptables
    remove_iptables_limits()

    # Отключаем телеметрию
    disable_telemetry()

    # Отключаем ненужные сервисы
    disable_unnecessary_services()

    print("Все ограничения сняты, телеметрия и ненужные сервисы отключены.")

if __name__ == "__main__":
    apply_all_settings()
