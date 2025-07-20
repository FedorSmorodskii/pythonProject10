import os
import random
from datetime import datetime, timedelta
import time
import shutil
from git import Repo, exc
import requests
import json

# Конфигурация
REPO_PATH = 'pythonProject8'
GIT_REMOTE = 'origin'
GIT_BRANCH = 'main'
GITHUB_TOKEN = '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'
REPO_OWNER = 'FedorSmorodskii'
REPO_NAME = 'pythonProject8'
MISTRAL_API_KEY = 'EjE8bYhrwYj6sueh5zd8R0XpjYNYjcrc'
PYTHON_FILE = 'my_file_1.py'


def setup_git_environment():
    """Настраивает окружение Git"""
    try:
        os.system('git config --global user.name "Fedor Generator"')
        os.system('git config --global user.email "fedorgenerator@example.com"')

        creds_file = os.path.expanduser('~/.git-credentials')
        with open(creds_file, 'w') as f:
            f.write(f'https://{GITHUB_TOKEN}:x-oauth-basic@github.com\n')

        return f'https://{GITHUB_TOKEN}@github.com/{REPO_OWNER}/{REPO_NAME}.git'
    except Exception as e:
        print(f"Ошибка настройки git окружения: {e}")
        raise


def clean_directory(dir_path):
    """Очищает директорию, сохраняя только скрипт"""
    try:
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                if filename == os.path.basename(__file__):
                    continue
                file_path = os.path.join(dir_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path) and filename != '.git':
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Не удалось удалить {file_path}: {e}")
    except Exception as e:
        print(f"Ошибка очистки директории: {e}")


def setup_repository(repo_url):
    """Инициализирует или обновляет репозиторий"""
    try:
        if not os.path.exists(REPO_PATH):
            os.makedirs(REPO_PATH, exist_ok=True)

        clean_directory(REPO_PATH)

        if not os.path.exists(os.path.join(REPO_PATH, '.git')):
            print(f"Клонирование репозитория в {REPO_PATH}...")
            repo = Repo.clone_from(repo_url, REPO_PATH)
            if GIT_BRANCH not in repo.heads:
                repo.git.checkout('-b', GIT_BRANCH)
            return repo

        repo = Repo(REPO_PATH)

        if GIT_REMOTE in repo.remotes:
            repo.delete_remote(GIT_REMOTE)
        repo.create_remote(GIT_REMOTE, repo_url)

        repo.git.fetch('--all')

        if f'{GIT_REMOTE}/{GIT_BRANCH}' in repo.references:
            repo.git.checkout(GIT_BRANCH)
            repo.git.reset('--hard', f'{GIT_REMOTE}/{GIT_BRANCH}')
        else:
            if GIT_BRANCH not in repo.heads:
                repo.git.checkout('-b', GIT_BRANCH)
            else:
                repo.git.checkout(GIT_BRANCH)

        return repo

    except Exception as e:
        print(f"Ошибка при настройке репозитория: {e}")
        raise


def push_changes(repo):
    """Пытается отправить изменения с обработкой ошибок"""
    try:
        origin = repo.remote(name=GIT_REMOTE)
        origin.push(refspec=f'{GIT_BRANCH}:{GIT_BRANCH}')
        return True
    except exc.GitCommandError as e:
        print(f"Ошибка при push: {e}")
        try:
            repo.git.push('--set-upstream', GIT_REMOTE, GIT_BRANCH)
            return True
        except exc.GitCommandError as e:
            print(f"Не удалось создать ветку на удаленном репозитории: {e}")
            return False


def generate_with_mistral(prompt, max_tokens=1000):
    """Генерирует текст с помощью Mistral AI"""
    try:
        headers = {
            'Authorization': f'Bearer {MISTRAL_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            "model": "mistral-small",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens
        }

        response = requests.post(
            'https://api.mistral.ai/v1/chat/completions',
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            print(f"Ошибка Mistral API: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Ошибка при обращении к Mistral AI: {e}")
        return None


def generate_python_program():
    """Генерирует случайную программу на Python"""
    program_types = [
        "Калькулятор матричных операций с NumPy",
        "Генератор фракталов с визуализацией",
        "Парсер логов с анализом и графиками",
        "Система учета задач с SQLite базой",
        "Чат-сервер на сокетах",
        "Анализатор текста с NLP (NLTK)",
        "Генератор музыкальных мелодий",
        "Визуализатор графов (NetworkX)",
        "Шифратор файлов с AES",
        "Имитатор физических процессов",
        "Распознавание рукописных цифр (MNIST)",
        "Оптимизатор портфеля инвестиций",
        "Генератор 3D-моделей (OpenSCAD)",
        "Анализатор сетевого трафика",
        "Система рекомендаций на основе коллаборативной фильтрации",
        "Генератор QR-кодов с настройками",
        "Плагин для Blender на Python",
        "Анализатор сложности паролей",
        "Генератор тестовых данных",
        "Конвертер изображений в ASCII-арт",
        "Анализатор CSV/XLSX файлов",
        "Генератор облака тегов",
        "Система учета расходов с категориями",
        "Планировщик задач с уведомлениями",
        "Генератор случайных графов",
        "Анализатор тональности текста",
        "Генератор лабиринтов с алгоритмами поиска пути",
        "Визуализатор математических функций",
        "Парсер веб-страниц с BeautifulSoup",
        "Генератор документов по шаблону",
        "Анализатор аудиофайлов (спектрограммы)",
        "Система тестирования знаний",
        "Генератор анимаций с matplotlib",
        "Конвертер между системами счисления",
        "Анализатор социального графа",
        "Генератор кроссвордов",
        "Визуализатор данных с Dash",
        "Парсер API Twitter/Reddit",
        "Генератор SVG-графики",
        "Анализатор стихотворных размеров"
    ]

    selected_type = random.choice(program_types)
    prompt = (
        f"Напиши работающую программу на Python по теме: '{selected_type}'. "
        "Требования:\n"
        "1. Код должен быть 50-400 строк\n"
        "2. Должен содержать комментарии\n"
        "3. Должен быть полностью рабочим\n"
        "4. Не использовать внешние API (кроме случаев, когда это необходимо по заданию)\n"
        "5. Добавь описание программы в начале файла\n"
        "Формат вывода: только чистый Python код без Markdown обрамления"
    )

    program = generate_with_mistral(prompt)
    if not program:
        program = """# Простой калькулятор
def add(a, b): return a + b
def subtract(a, b): return a - b
def main():
    print("1. Сложение\n2. Вычитание")
    choice = input("Выберите операцию: ")
    a = float(input("Первое число: "))
    b = float(input("Второе число: "))
    if choice == '1': print(f"Результат: {add(a, b)}")
    elif choice == '2': print(f"Результат: {subtract(a, b)}")
    else: print("Неверный ввод")
if __name__ == "__main__": main()"""

    return program, selected_type


def generate_readme(program_type):
    """Генерирует README файл"""
    prompt = (
        f"Создай подробный README.md для Python проекта '{program_type}'. "
        "Включи:\n"
        "1. Описание проекта\n"
        "2. Требования (Python версия, зависимости)\n"
        "3. Инструкции по установке\n"
        "4. Примеры использования\n"
        "5. Лицензия (MIT)\n"
        "Формат: Markdown без обрамления кода"
    )
    readme = generate_with_mistral(prompt, max_tokens=1500)
    return readme if readme else f"# {program_type}\n\nАвтоматически сгенерированный проект"


def generate_commit_message(program_type):
    """Генерирует сообщение для коммита"""
    prompt = f"Придумай краткое описание (1 короткое описание) коммита для программы: '{program_type}'. Формат: Добавлен: [описание]"
    message = generate_with_mistral(prompt, max_tokens=50)
    return message if message else f"Добавлен: {program_type}"


def commit_and_push():
    """Создаёт коммит и пушит изменения"""
    try:
        repo_url = setup_git_environment()
        repo = setup_repository(repo_url)

        program, program_type = generate_python_program()
        readme = generate_readme(program_type)

        # Сохраняем программу (всегда перезаписываем)
        with open(os.path.join(REPO_PATH, PYTHON_FILE), 'w') as f:
            f.write(program)

        # Сохраняем README
        with open(os.path.join(REPO_PATH, 'README.md'), 'w') as f:
            f.write(readme)

        # Добавляем файлы в индекс
        repo.index.add([PYTHON_FILE, 'README.md'])

        # Коммитим
        commit_message = generate_commit_message(program_type)
        repo.index.commit(commit_message)

        # Пушим
        if not push_changes(repo):
            raise Exception("Не удалось отправить изменения")

        print(f"Успешно обновлены: {PYTHON_FILE} и README.md")
        return True

    except exc.GitCommandError as e:
        print(f"Git ошибка: {e}")
        return False
    except Exception as e:
        print(f"Общая ошибка: {e}")
        return False


def calculate_sleep_time():
    """Вычисляет случайное время ожидания от 12 до 23 часов (в секундах)"""
    return random.uniform(12 * 3600, 23 * 3600)


def main():
    print("Скрипт генерации программ запущен...")
    while True:
        success = commit_and_push()
        if success:
            print(f"Коммит создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            sleep_time = calculate_sleep_time()
            print(f"Ожидание до следующей генерации: {sleep_time / 3600:.2f} часов")
            time.sleep(sleep_time)
        else:
            print("Проблема с созданием коммита. Повторная попытка через 1 час...")
            time.sleep(3600)


if __name__ == "__main__":
    main()