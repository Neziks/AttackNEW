import os
import subprocess

# Увеличение лимитов по открытым файлам (например, для всех пользователей)
def increase_file_limits():
    # Устанавливаем лимит открытых файлов на 100000
    subprocess.run("ulimit -n 100000", shell=True)

# Отключение ограничений на сети
def disable_network_limits():
    # Разрешаем всем интерфейсам прослушивать порты
    subprocess.run("sysctl -w net.ipv4.ip_local_port_range='1024 65535'", shell=True)
    subprocess.run("sysctl -w net.ipv4.tcp_fin_timeout=30", shell=True)
    subprocess.run("sysctl -w net.ipv4.tcp_max_syn_backlog=2048", shell=True)

    # Отключаем фаервол
    subprocess.run("ufw disable", shell=True)

# Отключение ограничений на ресурсы памяти
def disable_memory_limits():
    subprocess.run("sysctl -w vm.swappiness=10", shell=True)

if __name__ == "__main__":
    # Включение привилегий администратора (root)
    if os.geteuid() != 0:
        print("Этот скрипт нужно запускать от имени администратора (root).")
    else:
        # Применяем изменения
        increase_file_limits()
        disable_network_limits()
        disable_memory_limits()
        print("Ограничения сняты.")
