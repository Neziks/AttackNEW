import os
import resource
import subprocess
import logging
import speedtest

def setup_logging():
    logging.basicConfig(
        level=logging.INFO, 
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def run_command(command: str):
    """Выполнение команды с обработкой ошибок."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.stdout.strip():
            logging.info(f"✅ {command}: {result.stdout.strip()}")
        if result.stderr.strip():
            logging.warning(f"⚠️ Ошибка при выполнении {command}: {result.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Ошибка при выполнении {command}: {e.stderr.strip()}")

def set_limits():
    """Снятие системных лимитов."""
    limits = {
        resource.RLIMIT_NOFILE: (1000000, 1000000),
        resource.RLIMIT_NPROC: (resource.RLIM_INFINITY, resource.RLIM_INFINITY),
    }
    
    for limit, value in limits.items():
        try:
            resource.setrlimit(limit, value)
            logging.info(f"✅ Лимит {limit} установлен на {value}")
        except ValueError as e:
            logging.warning(f"⚠️ Не удалось изменить лимит {limit}: {e}")

def optimize_network():
    """Оптимизация сетевых настроек."""
    settings = {
        'net.core.somaxconn': '65535',
        'net.core.netdev_max_backlog': '5000',
        'fs.file-max': '1000000',
        'net.ipv4.tcp_rmem': '4096 87380 16777216',
        'net.ipv4.tcp_wmem': '4096 87380 16777216',
        'net.ipv4.ip_local_port_range': '1024 65535',
        'net.ipv4.tcp_mtu_probing': '1',
        'net.ipv4.tcp_fin_timeout': '15',
        'net.ipv4.tcp_keepalive_time': '1200',
        'net.ipv4.tcp_congestion_control': 'bbr',
        'net.ipv4.tcp_fastopen': '3',
        'net.ipv4.tcp_max_syn_backlog': '2048',
        'vm.swappiness': '10'
    }
    
    for key, value in settings.items():
        run_command(f'sysctl -w {key}="{value}"')

def clear_iptables():
    """Очистка iptables и отключение фаервола."""
    commands = [
        'iptables -F',
        'iptables -P INPUT ACCEPT',
        'iptables -P OUTPUT ACCEPT',
        'iptables -P FORWARD ACCEPT',
        'ufw disable'
    ]
    
    for cmd in commands:
        run_command(cmd)

def disable_services():
    """Отключение ненужных сервисов."""
    services = ["snapd", "bluetooth", "cups", "ModemManager", "whoopsie"]
    
    for service in services:
        run_command(f'systemctl stop {service}')
        run_command(f'systemctl disable {service}')

def disable_snap():
    """Отключение snap."""
    commands = [
        'systemctl stop snapd',
        'systemctl disable snapd',
        'apt-get purge snapd -y',
        'rm -rf /snap /var/snap /var/lib/snapd'
    ]
    
    for cmd in commands:
        run_command(cmd)

def disable_telemetry():
    """Отключение телеметрии."""
    commands = [
        'systemctl stop apport',
        'systemctl disable apport',
        'sysctl -w kernel.dmesg_restrict=1',
        'apt-get remove --purge ubuntu-report popularity-contest apport whoopsie -y',
        'apt-get autoremove -y',
        'apt-get clean'
    ]
    
    for cmd in commands:
        run_command(cmd)

def increase_file_limits():
    """Увеличение лимитов по открытым файлам."""
    run_command("ulimit -n 100000")

def find_best_server():
    """Поиск ближайшего и самого быстрого сервера для интернет-соединения."""
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        best_server = st.results.server
        logging.info(f"🌍 Лучший сервер: {best_server['sponsor']} ({best_server['name']}, {best_server['country']})")
        return best_server
    except Exception as e:
        logging.warning(f"⚠️ Ошибка поиска сервера Speedtest: {e}")
        return None

def apply_all():
    setup_logging()
    logging.info("⚙️ Начало оптимизации системы...")
    
    set_limits()
    optimize_network()
    clear_iptables()
    disable_services()
    disable_snap()
    disable_telemetry()
    increase_file_limits()
    
    find_best_server()
    
    logging.info("✅ Оптимизация завершена.")

if __name__ == "__main__":
    apply_all()
