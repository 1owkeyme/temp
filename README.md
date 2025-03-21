# EDM (Electronic Document Management)

Сервис для доставки документов контрагентам через системы ЭДО. Автоматически проверяет доступность контрагентов, при необходимости отправляет приглашения и отслеживает их принятие. Обеспечивает передачу документов и, если требуется, дожидается подписания со стороны контрагента, сохраняя подписанный экземпляр.

## Локальная разработка

### Установка

Установка необходимых пакетов в Ubuntu

1. Установка необходимых пакетов (Ubuntu 20.04)

```shell
sudo apt update && sudo apt upgrade -y
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.12
sudo apt install -y python3.12-distutils
sudo apt install -y python-socks
sudo apt install -y python3.12-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.12 get-pip.py
sudo apt install -y python3.12-venv
rm get-pip.py
```

2. Установка зависимостей проекта

```shell
make workspace-build
```

3. Установка зависимостей для разработки

```shell
make workspace-build-dev
```

### Миграция базы данных

1. Создание новой миграции

```shell
make create-migration m="Migration message"
```

2. Применение миграции (до актуальной ревизии)

```shell
make migrate
```

### Локальный запуск тестов

1. Запуск локальной инфраструктуры

```shell
make workspace-up
```

2. Запускаем тесты и считаем coverage

```shell
make tests
```

3. Выключение локальной инфраструктуры

```shell
make workspace-down
```

### Запуск проверок pre-commit

```shell
make pre-commit
```

## Установка и ведение документации

### Ведение документации
Документация сопровождается с помощью [Antora](https://docs.antora.org/antora/latest/) в формате [asciidocs](https://docs.asciidoctor.org/asciidoc/latest/).<br>
Antora документация проекта находится в `/docs`, antora playbook - `./antora-playbook.yml`.
#### Добавление страницы
Страницы документации содержатся в папке `/docs/modules/ROOT/pages`. Чтобы добавить новую страницу в навигации, нужно в файле `/docs/modules/ROOT/nav.adoc`
указать ссылку перехода на файл страницы с помощью команды:
```asciidoc
xref:путь_к_странице.adoc[alt text]
```
> **Пример** <br>
> Файл содержится по пути `/docs/modules/ROOT/pages/my_categories/category1.adoc`. Подключаем файл по следующему принципу:
> ```asciidoc
> xref:my_categories/category1.adoc[]
> ```
#### Добавление изображений
1) Изображения добавить в каталог `/docs/modules/ROOT/assets/images`.
2) В файле страницы импортировать изображение командой:
```asciidoc
image::ROOT:имя_изображения[alt text]
```
> **Пример** <br>
> Для импорта изображения который располагается по пути `/docs/modules/ROOT/assets/images/diagram_1.png` команда будет выглядить следующим образом:
> ```asciidoc
> image::ROOT:diagram_1.png[]
> ```
### Сборка документации
#### Вариант 1 (самостоятельный билд через NPM)
Сборка документации Antora вручную с помощью `npm` указана [в документации](https://docs.antora.org/antora/latest/install-and-run-quickstart/).
#### Вариант 2 (через docker)
1) Запустить docker на локальной машине.
2) Перейти в терминале в корень проекта.
3) Выполнить команду:
```commandline
make docs
```
или
```commandline
docker run -v .:/antora --rm -t antora/antora antora-playbook.yml
```

После сборки, работу сайта можно проверить открыв файл в браузере `./build/site/index.html`.
