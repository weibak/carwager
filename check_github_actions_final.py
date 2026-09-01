#!/usr/bin/env python3
"""
Финальная проверка конфигурации GitHub Actions
"""

import os
import sys

def check_workflow_files():
    """Проверяет наличие всех workflow файлов"""
    print("=== Проверка файлов GitHub Actions ===")
    
    workflow_files = [
        ".github/workflows/ruff.yml",
        ".github/workflows/test.yml", 
        ".github/workflows/security.yml",
        ".github/workflows/codeql.yml",
        ".github/workflows/ci.yml",
        ".github/dependabot.yml",
        ".github/codeql/codeql-config.yml",
        ".github/SECRETS_SETUP.md"
    ]
    
    all_ok = True
    for file in workflow_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"❌ {file} не найден")
            all_ok = False
    
    return all_ok

def check_workflow_content():
    """Проверяет содержание workflow файлов"""
    print("\n=== Проверка содержания workflow ===")
    
    checks = []
    
    # Проверяем ruff.yml
    with open(".github/workflows/ruff.yml", 'r') as f:
        ruff_content = f.read()
        checks.append(("Ruff workflow", "ruff check" in ruff_content))
        checks.append(("Ruff permissions", "permissions:" in ruff_content))
        checks.append(("Ruff changed files", "changed-files" in ruff_content))
    
    # Проверяем test.yml
    with open(".github/workflows/test.yml", 'r') as f:
        test_content = f.read()
        checks.append(("Test workflow", "pytest" in test_content))
        checks.append(("PostgreSQL service", "postgres:" in test_content))
        checks.append(("Redis service", "redis:" in test_content))
    
    # Проверяем security.yml
    with open(".github/workflows/security.yml", 'r') as f:
        security_content = f.read()
        checks.append(("Security workflow", "safety" in security_content))
        checks.append(("Bandit check", "bandit" in security_content))
        checks.append(("Trivy scanner", "trivy" in security_content))
    
    # Проверяем codeql.yml
    with open(".github/workflows/codeql.yml", 'r') as f:
        codeql_content = f.read()
        checks.append(("CodeQL workflow", "codeql" in codeql_content))
        checks.append(("CodeQL config", "codeql-config.yml" in codeql_content))
    
    # Проверяем dependabot.yml
    with open(".github/dependabot.yml", 'r') as f:
        dependabot_content = f.read()
        checks.append(("Dependabot config", "version: 2" in dependabot_content))
        checks.append(("Python updates", "pip" in dependabot_content))
        checks.append(("Docker updates", "docker" in dependabot_content))
    
    all_ok = True
    for check_name, check_result in checks:
        if check_result:
            print(f"✓ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_ok = False
    
    return all_ok

def check_project_requirements():
    """Проверяет требования проекта"""
    print("\n=== Проверка требований проекта ===")
    
    requirements = [
        ("requirements.txt", os.path.exists("requirements.txt")),
        ("docker-compose.yml", os.path.exists("docker-compose.yml")),
        ("Dockerfile", os.path.exists("Dockerfile")),
        (".env.example", os.path.exists(".env.example")),
        ("manage.py", os.path.exists("manage.py")),
    ]
    
    all_ok = True
    for req_name, req_exists in requirements:
        if req_exists:
            print(f"✓ {req_name}")
        else:
            print(f"❌ {req_name}")
            all_ok = False
    
    return all_ok

def print_summary():
    """Выводит итоговую сводку"""
    print("\n" + "=" * 60)
    print("ИТОГОВАЯ СВОДКА ПО GITHUB ACTIONS")
    print("=" * 60)
    
    print("\n✅ НАСТРОЕНО:")
    print("1. Ruff - линтер Python кода")
    print("2. Тестирование - Django tests с PostgreSQL и Redis")
    print("3. Безопасность - safety, bandit, trivy")
    print("4. CodeQL - статический анализ безопасности")
    print("5. Dependabot - автоматическое обновление зависимостей")
    print("6. Полный CI/CD пайплайн (ci.yml)")
    
    print("\n🔧 ЧТО ДЕЛАЕТ КАЖДЫЙ WORKFLOW:")
    print("• ruff.yml - проверка стиля кода, только измененные файлы")
    print("• test.yml - запуск тестов Django с БД и Redis")
    print("• security.yml - проверка уязвимостей в зависимостях")
    print("• codeql.yml - анализ безопасности исходного кода")
    print("• ci.yml - полный пайплайн (линт, тесты, сборка, деплой)")
    
    print("\n⚙️  СЕКРЕТЫ ДЛЯ НАСТРОЙКИ:")
    print("1. DOCKER_USERNAME / DOCKER_PASSWORD - для сборки образов")
    print("2. HEROKU_API_KEY / HEROKU_APP_NAME - для деплоя")
    print("3. SLACK_WEBHOOK_URL - для уведомлений")
    print("(см. .github/SECRETS_SETUP.md)")
    
    print("\n🚀 СЛЕДУЮЩИЕ ШАГИ:")
    print("1. Добавить секреты в GitHub репозиторий")
    print("2. Настроить тесты Django (если еще нет)")
    print("3. Проверить работу workflow через Pull Request")
    print("4. Настроить автоматический деплой при мерже в main")

def main():
    print("ПРОВЕРКА КОНФИГУРАЦИИ GITHUB ACTIONS")
    print("=" * 60)
    
    files_ok = check_workflow_files()
    content_ok = check_workflow_content()
    requirements_ok = check_project_requirements()
    
    print_summary()
    
    if files_ok and content_ok and requirements_ok:
        print("\n✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        return 0
    else:
        print("\n⚠️  ЕСТЬ ПРОБЛЕМЫ, ТРЕБУЕТСЯ ДОРАБОТКА")
        return 1

if __name__ == "__main__":
    sys.exit(main())