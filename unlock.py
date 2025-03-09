import os
import resource
import subprocess
import logging
import speedtest

def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def run_command(command):
    """Безопасное выполнение команды."""
    try:
        result = subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.stdout.strip():
            logging.info(f"✅ {command}: {result.stdout.strip()}")
        if result.stderr.strip():
            logging.warning(f"⚠️ {command}: {result.stderr.strip()}")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Ошибка {command}: {e.stderr.strip()}", exc_info=True)
    except subprocess.TimeoutExpired as e:
        logging.error(f"❌ Таймаут {command}: {e}", exc_info=True)

def set_limits():
    """Снятие системных лимитов."""
    limits = {
        resource.RLIMIT_NOFILE: (1000000, 1000000),
        resource.RLIMIT_NPROC: (resource.RLIM_INFINITY, resource.RLIM_INFINITY),
    }
    
    for limit, value in limits.items():
        current = resource.getrlimit(limit)
        if current != value:
            resource.setrlimit(limit, value)
            logging.info(f"✅ Лимит {limit} установлен на {value}")
        else:
            logging.info(f"ℹ️ Лимит {limit} уже установлен")

def optimize_network():
    """Оптимизация сетевых параметров и снятие ограничений."""
    settings = {
        "net.core.somaxconn": "65535",
        "net.core.netdev_max_backlog": "10000",
        "fs.file-max": "2000000",
        "net.ipv4.tcp_rmem": "4096 87380 33554432",
        "net.ipv4.tcp_wmem": "4096 87380 33554432",
        "net.ipv4.ip_local_port_range": "1024 65535",
        "net.ipv4.tcp_mtu_probing": "1",
        "net.ipv4.tcp_fin_timeout": "10",
        "net.ipv4.tcp_keepalive_time": "600",
        "net.ipv4.tcp_congestion_control": "bbr",
        "net.ipv4.tcp_fastopen": "3",
        "net.ipv4.tcp_max_syn_backlog": "4096",
        "vm.swappiness": "1"
    }
    for key, value in settings.items():
        run_command(["sysctl", "-w", f"{key}={value}"])

def clear_iptables():
    """Открытие всех портов и снятие ограничений iptables."""
    commands = [["iptables", "-F"], ["iptables", "-X"], ["iptables", "-Z"],
                ["iptables", "-P", "INPUT", "ACCEPT"], ["iptables", "-P", "OUTPUT", "ACCEPT"],
                ["iptables", "-P", "FORWARD", "ACCEPT"]]
    for cmd in commands:
        run_command(cmd)

def disable_services():
    """Отключение ненужных сервисов."""
    services = ["snapd", "bluetooth", "cups", "ModemManager", "whoopsie"]
    for service in services:
        run_command(["systemctl", "stop", service])
        run_command(["systemctl", "disable", service])

def apply_all():
    setup_logging()
    logging.info("⚙️ Запуск оптимизации...")
    set_limits()
    optimize_network()
    clear_iptables()
    disable_services()
    logging.info("✅ Оптимизация завершена.")

if __name__ == "__main__":
    apply_all()
