# Микросервис для визуализации данных о землетрясениях
## Описание
С помощью сервиса можно обрабатывать данные о землетрясениях, загруженные пользователем, хранить их и визуализировать в виде графиков.
Основные библиотеки:
- **FastAPI** для создания программного интерфейса
- **loguru** для логирования
- **pytest** для автоматизации модульного тестирования
- **conda** для создания виртуального окружения и управления зависимостями
- [turkey_eq_monitor](https://github.com/dzhoshua/turkey_eq_monitor.git) для построения графиков.

## Инструкция по установке
Активируйте виртуальное окружение(на примере Anaconda).
```
conda deactivate
conda create -n turkey_eq python=3.10
conda activate turkey_eq
```
Установите cartopy.
```
conda install cartopy
```
Клонируйте репозиторий и перейдите в папку с микросервисом.
```
git clone https://github.com/piccolo-gatto/eq_microservice.git
cd */eq_microservice
```
Установите необходимые зависимости.
```
poetry install
```
Запустите микросервис.
```
uvicorn app.main:api --reload --port 8083
```

## Лицензия
MIT
