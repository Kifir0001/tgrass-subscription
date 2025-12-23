#!/usr/bin/env python3
"""
Быстрый скрипт для отправки изменений на GitHub
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, check=True):
    """Выполняет команду"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.stdout.strip() if result.stdout else ""
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка: {e.stderr if e.stderr else str(e)}")
        return None

def main():
    # Переходим в директорию скрипта
    script_dir = Path(__file__).parent.absolute()
    try:
        os.chdir(script_dir)
    except:
        # Если не получилось, пробуем через полный путь
        pass
    
    print("🔄 Отправка изменений на GitHub...")
    print()
    
    # Проверяем git
    if not Path(".git").exists():
        print("📦 Инициализация git репозитория...")
        run_command("git init")
        run_command("git branch -M main")
    
    # Добавляем все файлы
    print("📝 Добавление файлов...")
    run_command("git add .")
    
    # Проверяем статус
    status = run_command("git status --porcelain", check=False)
    
    if status:
        print("💾 Создание коммита...")
        run_command('git commit -m "Update: Change Telegram link"')
        print("✅ Коммит создан")
    else:
        print("⚠️  Нет изменений для коммита")
        # Проверяем, есть ли коммиты
        try:
            run_command("git log -1 --oneline", check=False)
        except:
            print("💾 Создание начального коммита...")
            run_command('git commit -m "Initial commit"')
    
    print()
    
    # Проверяем remote
    remotes = run_command("git remote", check=False)
    
    if remotes and "origin" in remotes:
        print("🚀 Отправка на GitHub...")
        run_command("git push origin main")
        print()
        print("✅ Изменения отправлены!")
        print("   GitHub Actions автоматически задеплоит сайт через несколько минут")
    else:
        print("⚠️  Remote 'origin' не найден")
        print("   Выполните: git remote add origin https://github.com/Kifir0001/tgrass-subscription.git")
        print("   Затем: git push -u origin main")

if __name__ == "__main__":
    main()

