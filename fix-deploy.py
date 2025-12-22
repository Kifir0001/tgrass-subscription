#!/usr/bin/env python3
"""
Скрипт для исправления деплоя - добавляет все файлы и пушит изменения
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, check=True, capture_output=False):
    """Выполняет команду и возвращает результат"""
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                check=check,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            return result.stdout.strip()
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=check
            )
            return None
    except subprocess.CalledProcessError as e:
        if check:
            print(f"❌ Ошибка: {e.stderr if hasattr(e, 'stderr') and e.stderr else str(e)}")
            return None
        return None

def main():
    print("🔧 Исправление деплоя...")
    print()
    
    # Переходим в директорию скрипта
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    # Проверяем, что мы в правильной директории
    current_dir = Path.cwd()
    print(f"📁 Рабочая директория: {current_dir}")
    
    # Проверяем наличие файлов проекта
    required_files = ['index.html', 'style.css', 'script.js', '1.png']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        sys.exit(1)
    
    print("✅ Все необходимые файлы на месте")
    print()
    
    # Проверяем git
    if not Path(".git").exists():
        print("📦 Инициализация git репозитория...")
        run_command("git init")
        run_command("git branch -M main")
        print("✅ Git репозиторий инициализирован")
    else:
        print("✅ Git репозиторий уже существует")
    
    print()
    print("📝 Добавление всех файлов...")
    run_command("git add .")
    
    # Проверяем статус
    status = run_command("git status --porcelain", capture_output=True)
    
    if status:
        print("💾 Создание коммита...")
        run_command('git commit -m "Fix: Update files for GitHub Pages deployment"')
        print("✅ Коммит создан")
    else:
        print("✅ Нет изменений для коммита")
    
    print()
    
    # Проверяем remote
    try:
        remotes = run_command("git remote", capture_output=True)
        if "origin" in remotes:
            print("🔄 Отправка изменений на GitHub...")
            run_command("git push origin main")
            print()
            print("✅ Изменения отправлены!")
            print()
            print("📋 Проверьте:")
            print("   1. Что в настройках репозитория (Settings > Pages) выбран 'GitHub Actions'")
            print("   2. Статус деплоя в разделе Actions")
            print("   3. Что файл 1.png загружен в репозиторий")
        else:
            print("⚠️  Remote 'origin' не найден")
            print("   Выполните: git remote add origin https://github.com/Kifir0001/tgrass-subscription.git")
    except:
        print("⚠️  Не удалось отправить изменения")

if __name__ == "__main__":
    main()

