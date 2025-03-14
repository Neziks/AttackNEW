package main

import (
	"fmt"
	"math/rand"
	"net"
	"runtime"
	"sync"
	"time"
)

// Функция для отправки TCP пакетов многопоточно
func sendTCP(address string, message string, duration int, ip string, port int, wg *sync.WaitGroup) {
	defer wg.Done()
	endTime := time.Now().Add(time.Duration(duration) * time.Second)
	packetsSent := int64(0)

	// Открываем одно соединение и отправляем сообщения в нем
	conn, err := net.Dial("tcp", address)
	if err != nil {
		fmt.Println("❌ Ошибка при подключении по TCP:", err)
		return
	}
	defer conn.Close()

	for time.Now().Before(endTime) {
		_, err = conn.Write([]byte(message))
		if err == nil {
			packetsSent++
		}

		// Случайная задержка, чтобы не блокировать сервер
		time.Sleep(time.Millisecond * time.Duration(rand.Intn(10)))
	}

	cps := float64(packetsSent) / float64(duration)
	fmt.Printf("🚀 CPS: %.2f | 🎯 TARGET: %s:%d | 📶 PING: N/A\n", cps, ip, port)
}

// Функция для отправки UDP пакетов многопоточно
func sendUDP(address string, message string, duration int, ip string, port int, wg *sync.WaitGroup) {
	defer wg.Done()
	endTime := time.Now().Add(time.Duration(duration) * time.Second)
	packetsSent := int64(0)

	conn, err := net.Dial("udp", address)
	if err != nil {
		fmt.Println("❌ Ошибка при подключении по UDP:", err)
		return
	}
	defer conn.Close()

	for time.Now().Before(endTime) {
		_, err = conn.Write([]byte(message))
		if err == nil {
			packetsSent++
		}

		// Случайная задержка, чтобы не блокировать сервер
		time.Sleep(time.Millisecond * time.Duration(rand.Intn(10)))
	}

	pps := float64(packetsSent) / float64(duration)
	fmt.Printf("⚡ PPS: %.2f | 🎯 TARGET: %s:%d | 📶 PING: N/A\n", pps, ip, port)
}

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU()) // Используем все ядра процессора

	var ip, protocol string
	var port, duration int

	fmt.Println("🔹 Добро пожаловать в сетевой тестер 🔹")

	fmt.Print("🌐 Введите айпи: ")
	fmt.Scan(&ip)

	fmt.Print("📡 Введите порт: ")
	fmt.Scan(&port)

	fmt.Print("🔄 Введите протокол (tcp/udp): ")
	fmt.Scan(&protocol)

	fmt.Print("⏳ Введите время (в секундах): ")
	fmt.Scan(&duration)

	address := fmt.Sprintf("%s:%d", ip, port)
	message := "Привет, мир!" // Можно заменить на произвольное сообщение

	fmt.Println("🚀 Запуск...\n")

	var wg sync.WaitGroup
	numThreads := runtime.NumCPU() * 2 // Двойное количество потоков относительно ядер
	wg.Add(numThreads)

	for i := 0; i < numThreads; i++ {
		go func() {
			switch protocol {
			case "tcp":
				sendTCP(address, message, duration, ip, port, &wg)
			case "udp":
				sendUDP(address, message, duration, ip, port, &wg)
			default:
				fmt.Println("❌ Неизвестный протокол. Используйте tcp или udp.")
			}
		}()
	}

	wg.Wait()
	fmt.Println("🎉 Завершено! Спасибо за использование! 🎉")
}
