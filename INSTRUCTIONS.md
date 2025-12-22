# Инструкция по исправлению деплоя

Если сайт не работает на GitHub Pages, выполните следующие шаги:

## 1. Убедитесь, что вы в правильной директории

Откройте терминал в папке проекта:
```
C:\Users\Максим\Desktop\bots_tg_ref — копия\test_miniapp
```

## 2. Запустите скрипт исправления

```bash
python fix-deploy.py
```

Или выполните команды вручную:

```bash
# Убедитесь, что git репозиторий в правильной директории
git init
git branch -M main

# Добавьте все файлы (включая 1.png!)
git add .

# Создайте коммит
git commit -m "Fix: Add all files for deployment"

# Отправьте на GitHub
git push origin main
```

## 3. Проверьте настройки GitHub Pages

1. Перейдите на https://github.com/Kifir0001/tgrass-subscription/settings/pages
2. Убедитесь, что в разделе "Source" выбран **"GitHub Actions"** (не "Deploy from a branch")
3. Сохраните изменения

## 4. Проверьте, что все файлы загружены

Убедитесь, что в репозитории есть:
- ✅ index.html
- ✅ style.css
- ✅ script.js
- ✅ 1.png (ВАЖНО! Изображение должно быть в репозитории)
- ✅ .github/workflows/deploy.yml

## 5. Проверьте статус деплоя

1. Перейдите в раздел **Actions** вашего репозитория
2. Убедитесь, что workflow "Deploy to GitHub Pages" выполнился успешно
3. Если есть ошибки - проверьте логи

## 6. Проверьте URL сайта

После успешного деплоя сайт должен быть доступен по адресу:
https://Kifir0001.github.io/tgrass-subscription/

**Важно:** Деплой может занять несколько минут после push.

