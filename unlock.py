import os
import resource
import subprocess
import logging
import sys
import importlib.util

def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def check_root():
    """Проверяет, запущен ли скрипт от root."""
    if os.geteuid() != 0:
        logging.error("❌ Скрипт должен быть запущен с root-правами! Используйте sudo.")
        sys.exit(1)

def install_and_import(module_name):
    """Проверяет наличие модуля и устанавливает его при необходимости."""
    if importlib.util.find_spec(module_name) is None:
        logging.warning(f"⚠️ Устанавливаю {module_name}...")
        subprocess.run([sys.executable, "-m", "pip", "install", module_name], check=True)
    else:
        logging.info(f"✅ Модуль {module_name} уже установлен")

# Проверяем и устанавливаем модули
install_and_import("speedtest")
import speedtest

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

def get_current_sysctl_value(param):
    """Получает текущее значение sysctl параметра."""
    try:
        result = subprocess.run(["sysctl", "-n", param], check=True, stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def set_limits():
    """Снятие системных лимитов."""
    try:
        resource.setrlimit(resource.RLIMIT_NOFILE, (1000000, 1000000))
        logging.info("✅ Лимит RLIMIT_NOFILE установлен на 1000000")
    except ValueError:
        logging.warning("⚠️ Невозможно изменить RLIMIT_NOFILE")
    try:
        resource.setrlimit(resource.RLIMIT_NPROC, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
        logging.info("✅ Лимит RLIMIT_NPROC установлен на бесконечность")
    except ValueError:
        logging.warning("⚠️ Невозможно изменить RLIMIT_NPROC")

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
        current_value = get_current_sysctl_value(key)
        if current_value is None or current_value != str(value):
            run_command(["sysctl", "-w", f"{key}={value}"])
        else:
            logging.info(f"ℹ️ Параметр {key} уже установлен на {value}")

def clear_iptables():
    """Открытие всех портов и снятие ограничений iptables."""
    commands = [
        ["iptables", "-F"], ["iptables", "-X"], ["iptables", "-Z"],
        ["iptables", "-P", "INPUT", "ACCEPT"],
        ["iptables", "-P", "OUTPUT", "ACCEPT"],
        ["iptables", "-P", "FORWARD", "ACCEPT"]
    ]
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
    check_root()
    print("⚙️ Запуск оптимизации...")
    logging.info("⚙️ Запуск оптимизации...")
    set_limits()
    optimize_network()
    clear_iptables()
    disable_services()
    print("✅ Оптимизация завершена.")
    logging.info("✅ Оптимизация завершена.")

if __name__ == "__main__":
    apply_all()
