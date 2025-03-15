#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <time.h>
#include <errno.h>

// Функция для отправки TCP пакетов
void send_tcp_packet(const char *ip, int port, const char *message, int duration) {
    struct sockaddr_in server_addr;
    int sock;
    time_t start_time, current_time;

    // Создаем TCP сокет
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Ошибка при создании TCP сокета");
        return;
    }

    // Устанавливаем адрес сервера
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = inet_addr(ip);

    // Подключаемся к серверу
    if (connect(sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Не удалось подключиться к серверу");
        close(sock);
        return;
    }

    time(&start_time);

    // Отправка пакетов в течение заданного времени
    while (1) {
        time(&current_time);
        if (difftime(current_time, start_time) >= duration) {
            break;
        }

        // Уникальные данные для каждого пакета (различия в сообщении)
        char unique_message[512];
        snprintf(unique_message, sizeof(unique_message), "%s - %ld", message, current_time);

        send(sock, unique_message, strlen(unique_message), 0);
        printf("Отправлен TCP пакет: %s\n", unique_message);
        usleep(500000);  // 0.5 секунда задержки между отправками
    }

    close(sock);
}

// Функция для отправки UDP пакетов
void send_udp_packet(const char *ip, int port, const char *message, int duration) {
    struct sockaddr_in server_addr;
    int sock;
    time_t start_time, current_time;

    // Создаем UDP сокет
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        perror("Ошибка при создании UDP сокета");
        return;
    }

    // Устанавливаем адрес сервера
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);
    server_addr.sin_addr.s_addr = inet_addr(ip);

    time(&start_time);

    // Отправка пакетов в течение заданного времени
    while (1) {
        time(&current_time);
        if (difftime(current_time, start_time) >= duration) {
            break;
        }

        // Уникальные данные для каждого пакета (различия в сообщении)
        char unique_message[512];
        snprintf(unique_message, sizeof(unique_message), "%s - %ld", message, current_time);

        sendto(sock, unique_message, strlen(unique_message), 0, (struct sockaddr *)&server_addr, sizeof(server_addr));
        printf("Отправлен UDP пакет: %s\n", unique_message);
        usleep(500000);  // 0.5 секунда задержки между отправками
    }

    close(sock);
}

int main() {
    char ip[50];
    int port, duration;
    char protocol[10];
    char message[256];

    // Запрос ввода данных
    printf("🌐 Введите IP-адрес: ");
    scanf("%s", ip);
    printf("🔌 Введите порт: ");
    scanf("%d", &port);
    printf("💬 Введите протокол (tcp/udp): ");
    scanf("%s", protocol);
    printf("⏳ Введите время атаки (в секундах): ");
    scanf("%d", &duration);
    printf("📝 Введите сообщение для отправки: ");
    getchar(); // Чистим буфер
    fgets(message, sizeof(message), stdin);
    message[strcspn(message, "\n")] = 0;  // Убираем лишний символ новой строки

    // Отправка пакетов в зависимости от выбранного протокола
    if (strcmp(protocol, "tcp") == 0) {
        send_tcp_packet(ip, port, message, duration);
    } else if (strcmp(protocol, "udp") == 0) {
        send_udp_packet(ip, port, message, duration);
    } else {
        printf("❌ Неизвестный протокол. Пожалуйста, выберите 'tcp' или 'udp'.\n");
    }

    return 0;
}
