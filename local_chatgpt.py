import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Загрузка модели GPT-2 или GPT-Neo
model_name = "EleutherAI/gpt-neo-1.3B"  # Более мощная модель для генерации кода
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Функция генерации текста (для генерации кода или ответов на вопросы)
def generate_text(prompt, max_length=200, temperature=0.7, top_k=50):
    # Токенизация текста
    inputs = tokenizer(prompt, return_tensors="pt")
    # Генерация текста с использованием модели
    outputs = model.generate(
        inputs["input_ids"], 
        max_length=max_length,
        temperature=temperature,  # Креативность
        top_k=top_k,  # Разнообразие
        no_repeat_ngram_size=2,  # Избегаем повторений
        pad_token_id=tokenizer.eos_token_id,
        eos_token_id=tokenizer.eos_token_id
    )
    # Декодирование генерированного текста
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Функция для интерпретации и выполнения кода
def execute_code(code):
    try:
        exec(code)
    except Exception as e:
        return f"Ошибка при выполнении: {str(e)}"
    return "Код выполнен успешно."

# Главный цикл общения с пользователем
def chat():
    print("ChatGPT для Python-кодинга. Напишите 'exit' для завершения.")
    history = []  # История чата для более последовательных ответов

    while True:
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            print("Завершаю программу...")
            break

        # Проверка на выполнение кода
        if user_input.startswith("exec:"):
            code_to_execute = user_input[5:].strip()  # Убираем префикс "exec:"
            result = execute_code(code_to_execute)
            print(f"ChatGPT (Результат выполнения кода): {result}")
            continue

        # Добавление в историю
        history.append(f"Вы: {user_input}")

        # Формируем запрос с учетом всей истории
        prompt = "\n".join(history) + "\nChatGPT:"
        
        # Генерация ответа
        response = generate_text(prompt, max_length=300, temperature=0.8, top_k=50)
        
        # Добавляем ответ в историю
        history.append(f"ChatGPT: {response}")

        print(f"ChatGPT: {response}")

if __name__ == "__main__":
    chat()
