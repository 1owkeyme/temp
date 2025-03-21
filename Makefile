all: run

DOCKER_IMAGE = antora/antora
PLAYBOOK = antora-playbook.yml
WORKDIR = .

# Команда для активации VENV и консоли исходя из ОС.
ifeq ($(OS),Windows_NT)
    ACTIVATE_VENV=venv\Scripts\activate
    RUN_CMD=powershell -Command
else
    ACTIVATE_VENV=source ./venv/bin/activate
    RUN_CMD=bash -c
endif


# Установка python зависимостей
workspace-build:
	@echo "Installing requirements"
	@$(RUN_CMD) "cp .env.example .env"
	@$(RUN_CMD) "python3.12 -m venv venv"
	@$(RUN_CMD) "$(ACTIVATE_VENV); unset all_proxy; unset ALL_PROXY; pip install --no-cache-dir -e . --root-user-action=ignore"

# Установка python зависимостей для разработки
workspace-build-dev:
	@echo "Installing development requirements"
	@$(RUN_CMD) "python3.12 -m venv venv"
	@$(RUN_CMD) "$(ACTIVATE_VENV); unset all_proxy; unset ALL_PROXY; pip install --no-cache-dir -e .[tests,migrations,lint,git] --root-user-action=ignore"
	@echo "Starting pre-commit"
	@$(RUN_CMD) "$(ACTIVATE_VENV); pre-commit install -t pre-push"

# Запуск локальной инфраструктуры
workspace-up:
	@echo "Up development infrastructure"
	@$(RUN_CMD) "docker-compose -f docker-compose-dev.yml up --build -d"

# Выключение локальной инфраструктуры
workspace-down:
	@echo "Up development infrastructure"
	@$(RUN_CMD) "docker-compose -f docker-compose-dev.yml down --remove-orphans"

# Применение миграций до актуальной ревизии
migrate:
	@echo "Migrating database to head"
	@$(RUN_CMD) "$(ACTIVATE_VENV); alembic upgrade head"

# Создание новой миграции
create-migration:
	@echo "Creating migration"
	@$(RUN_CMD) "$(ACTIVATE_VENV); alembic revision --autogenerate -m '$(m)'"

# Локальный запуск тестов
tests:
	@echo "Running tests"
	@$(RUN_CMD) "$(ACTIVATE_VENV); python -m pytest -c ./tests/pytest-config.ini --failed-first --showlocals ./tests"

# Локальный запуск приложения
run:
	@echo "Starting the application"
	@$(RUN_CMD) "$(ACTIVATE_VENV); uvicorn --app-dir src/edm presentation.api.main:app --reload --workers 1 --host 0.0.0.0 --port 8080"

# Запуск проверок pre-commit
pre-commit:
	@echo "Starting pre-commit"
	@$(RUN_CMD) "$(ACTIVATE_VENV); pre-commit run --all-files --show-diff-on-failure"

# Сборка документации
docs-build:
	docker run -v $(WORKDIR):/antora --rm -t $(DOCKER_IMAGE) $(PLAYBOOK)

# Очистки результата сборки (опционально)
clean:
	@echo "Cleaning build artifacts..."
	@rm -rf build

.PHONY: install run dev workspace-up migrate tests create-migration pre-commit clean docs-build
