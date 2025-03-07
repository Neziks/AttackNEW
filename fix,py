import re

def extract_proxies(input_file, output_file):
    # Регулярка для IP:PORT (учитывает IPv4 и порт)
    proxy_pattern = re.compile(r'^\d{1,3}(?:\.\d{1,3}){3}:\d{1,5}$')

    proxies = set()

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if proxy_pattern.match(line):
                proxies.add(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(sorted(proxies)))

    print(f"✅ Сохранено {len(proxies)} прокси в {output_file}")

if __name__ == "__main__":
    extract_proxies('214.txt', 'gg.txt')
