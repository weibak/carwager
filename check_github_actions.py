#!/usr/bin/env python3
"""
Скрипт для проверки конфигурации GitHub Actions
"""

import os
import yaml
import sys

def check_ruff_workflow():
    """Проверяет конфигурацию Ruff workflow"""
    ruff_file = ".github/workflows/ruff.yml"
    
    if not os.path.exists(ruff_file):
        print("❌ Файл ruff.yml не найден")
        return False
    
    try:
        with open(ruff_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print("=== Проверка Ruff workflow ===")
        
        # Проверяем основные секции
        checks = {
            "name": "Ruff" in content,
            "on: pull_request": "pull_request:" in content,
            "on: workflow_dispatch": "workflow_dispatch:" in content,
            "permissions": "permissions:" in content,
            "jobs: ruff": "jobs:" in content and "ruff:" in content,
            "runs-on: ubuntu-latest": "runs-on: ubuntu-latest" in content,
            "actions/checkout": "actions/checkout" in content,
            "changed-files action": "tj-actions/changed-files" in content,
            "ruff-action": "astral-sh/ruff-action" in content,
            "command-output": "mathiasvr/command-output" in content,
            "find-comment": "peter-evans/find-comment" in content,
            "create-or-update-comment": "peter-evans/create-or-update-comment" in content
        }
        
        all_ok = True
        for check_name, check_result in checks.items():
            if check_result:
                print(f"✓ {check_name}")
            else:
                print(f"❌ {check_name}")
                all_ok = False
        
        # Проверяем requirements.txt для Ruff
        req_file = ".github/workflows/requirements.txt"
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                req_content = f.read().strip()
            if "ruff" in req_content:
                print("✓ requirements.txt содержит ruff")
            else:
                print("❌ requirements.txt не содержит ruff")
                all_ok = False
        else:
            print("❌ Файл requirements.txt не найден")
            all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return False

def check_project_structure():
    """Проверяет структуру проекта для CI/CD"""
    print("\n=== Проверка структуры проекта ===")
    
    required_files = [
        "requirements.txt",
        "manage.py",
        "docker-compose.yml",
        ".env.example",
        "README.md",
        "README_LOCAL_DOCKER.md"
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} не найден")
            all_ok = False
    
    # Проверяем структуру Django
    django_dirs = [
        "carwager/",
        "carwager/static/",
        "carwager/templates/",
        "general/",
        "showbill/",
        "auction/",
        "chat/",
        "news/"
    ]
    
    for directory in django_dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}")
        else:
            print(f"⚠️  {directory} не найден")
    
    return all_ok

def check_ci_cd_recommendations():
    """Предлагает улучшения для CI/CD"""
    print("\n=== Рекомендации по улучшению CI/CD ===")
    
    recommendations = [
        "1. Добавить workflow для тестирования (pytest)",
        "2. Добавить workflow для сборки Docker образов",
        "3. Добавить workflow для деплоя",
        "4. Добавить проверку безопасности (dependabot, codeql)",
        "5. Добавить проверку миграций Django",
        "6. Добавить проверку статических файлов (collectstatic)",
        "7. Добавить проверку WebSocket соединений",
        "8. Добавить проверку базы данных (migrate --check)",
        "9. Добавить лимиты времени выполнения jobs",
        "10. Добавить кэширование зависимостей"
    ]
    
    for rec in recommendations:
        print(f"💡 {rec}")

def main():
    print("Проверка конфигурации GitHub Actions для CarWager")
    print("=" * 60)
    
    # Проверяем текущую конфигурацию
    ruff_ok = check_ruff_workflow()
    
    # Проверяем структуру проекта
    structure_ok = check_project_structure()
    
    # Выводим рекомендации
    check_ci_cd_recommendations()
    
    print("\n" + "=" * 60)
    
    if ruff_ok and structure_ok:
        print("✅ Базовая конфигурация GitHub Actions в порядке")
        print("\nЧто уже настроено:")
        print("  - Ruff линтер для Python кода")
        print("  - Автоматические комментарии в PR")
        print("  - Проверка только измененных файлов")
        print("  - Временная зона Moscow для логов")
    else:
        print("⚠️  Есть проблемы с конфигурацией")
        
    print("\nСледующие шаги:")
    print("1. Добавить больше workflow для полного CI/CD пайплайна")
    print("2. Настроить тестирование и деплой")
    print("3. Добавить проверки безопасности")
    print("4. Настроить автоматическое обновление зависимостей")

if __name__ == "__main__":
    main()