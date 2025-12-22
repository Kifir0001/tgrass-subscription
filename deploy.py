#!/usr/bin/env python3
"""
Скрипт для автоматического деплоя на GitHub Pages
Создает репозиторий, настраивает GitHub Actions и деплоит сайт
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
            print(f"❌ Ошибка при выполнении команды: {command}")
            print(f"   {e.stderr if hasattr(e, 'stderr') else str(e)}")
            sys.exit(1)
        return None

def check_git_installed():
    """Проверяет, установлен ли git"""
    try:
        run_command("git --version", check=False)
        return True
    except:
        print("❌ Git не установлен. Установите Git и попробуйте снова.")
        return False

def check_gh_installed():
    """Проверяет, установлен ли GitHub CLI"""
    try:
        run_command("gh --version", check=False)
        return True
    except:
        return False

def init_git_repo():
    """Инициализирует git репозиторий"""
    if not Path(".git").exists():
        print("📦 Инициализация git репозитория...")
        run_command("git init")
        run_command("git branch -M main")
        print("✅ Git репозиторий инициализирован")
    else:
        print("✅ Git репозиторий уже инициализирован")

def commit_changes():
    """Добавляет и коммитит изменения"""
    print("📝 Добавление файлов...")
    run_command("git add .")
    
    # Проверяем, есть ли изменения
    status = run_command("git status --porcelain", capture_output=True)
    
    if not status:
        # Проверяем, есть ли хотя бы один коммит
        try:
            run_command("git log -1 --oneline", check=False)
            print("✅ Нет изменений для коммита")
            return False
        except:
            # Нет коммитов, создаем первый
            print("💾 Создание начального коммита...")
            run_command('git commit -m "Initial commit: Tgrass sponsor subscription page"')
            print("✅ Коммит создан")
            return True
    else:
        print("💾 Создание коммита...")
        run_command('git commit -m "Initial commit: Tgrass sponsor subscription page"')
        print("✅ Коммит создан")
        return True

def check_gh_auth():
    """Проверяет авторизацию в GitHub CLI"""
    try:
        run_command("gh auth status", check=False)
        return True
    except:
        return False

def create_github_repo(repo_name, is_public=True):
    """Создает репозиторий на GitHub через GitHub CLI"""
    visibility = "--public" if is_public else "--private"
    
    print(f"🔨 Создание репозитория '{repo_name}' на GitHub...")
    
    try:
        run_command(f'gh repo create {repo_name} {visibility} --source=. --remote=origin --push')
        print("✅ Репозиторий создан и код отправлен!")
        return True
    except:
        print("❌ Ошибка при создании репозитория")
        return False

def push_to_github():
    """Отправляет изменения на GitHub"""
    print("🔄 Отправка изменений на GitHub...")
    try:
        run_command("git push origin main")
        print("✅ Изменения отправлены!")
        return True
    except:
        print("❌ Ошибка при отправке изменений")
        return False

def get_github_username():
    """Получает имя пользователя GitHub"""
    try:
        username = run_command("gh api user --jq .login", capture_output=True)
        return username
    except:
        return None

def main():
    print("🚀 Настройка автоматического деплоя на GitHub Pages...")
    print()
    
    # Проверяем установку git
    if not check_git_installed():
        sys.exit(1)
    
    # Инициализируем git репозиторий
    init_git_repo()
    print()
    
    # Коммитим изменения
    has_commits = commit_changes()
    print()
    
    # Проверяем наличие remote
    try:
        remotes = run_command("git remote", capture_output=True)
        has_origin = "origin" in remotes
    except:
        has_origin = False
    
    if not has_origin:
        print("🔍 Проверка авторизации GitHub CLI...")
        
        if not check_gh_installed():
            print("⚠️  GitHub CLI не установлен")
            print()
            show_manual_instructions()
            return
        
        if not check_gh_auth():
            print("⚠️  GitHub CLI не авторизован")
            print("   Выполните: gh auth login")
            print()
            show_manual_instructions()
            return
        
        print("✅ GitHub CLI авторизован")
        print()
        
        # Запрашиваем имя репозитория
        repo_name = input("Введите имя репозитория (или нажмите Enter для 'tgrass-subscription'): ").strip()
        if not repo_name:
            repo_name = "tgrass-subscription"
        
        # Запрашиваем видимость
        visibility_input = input("Сделать репозиторий публичным? (y/n, по умолчанию: y): ").strip().lower()
        is_public = visibility_input != "n"
        
        print()
        
        # Создаем репозиторий
        if create_github_repo(repo_name, is_public):
            print()
            print("📋 Следующие шаги:")
            print("   1. Перейдите в Settings > Pages вашего репозитория")
            print("   2. В разделе 'Source' выберите 'GitHub Actions'")
            print("   3. Сохраните изменения")
            print()
            
            username = get_github_username()
            if username:
                print("🌐 После настройки Pages сайт будет доступен по адресу:")
                print(f"   https://{username}.github.io/{repo_name}/")
                print()
            
            print("🚀 GitHub Actions автоматически задеплоит сайт после первого push!")
        else:
            print()
            show_manual_instructions()
    else:
        # Remote уже существует, просто пушим
        if push_to_github():
            print()
            print("✅ GitHub Actions автоматически задеплоит сайт.")
            print("   Проверьте статус деплоя в разделе Actions вашего репозитория")

def show_manual_instructions():
    """Показывает инструкции для ручной настройки"""
    print("📋 Для завершения настройки выполните следующие шаги:")
    print()
    print("1. Авторизуйтесь в GitHub CLI (если еще не авторизованы):")
    print("   gh auth login")
    print()
    print("2. Создайте репозиторий на GitHub:")
    print("   - Перейдите на https://github.com/new")
    print("   - Создайте новый репозиторий (например, 'tgrass-subscription')")
    print()
    print("3. Подключите remote и отправьте код:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git")
    print("   git push -u origin main")
    print()
    print("4. Включите GitHub Pages:")
    print("   - Перейдите в Settings > Pages вашего репозитория")
    print("   - В разделе 'Source' выберите 'GitHub Actions'")
    print("   - Сохраните изменения")
    print()
    print("После этого GitHub Actions автоматически задеплоит сайт на GitHub Pages!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Операция отменена пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        sys.exit(1)

