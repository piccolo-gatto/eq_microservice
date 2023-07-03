# Микросервис для визуализации данных о землетрясениях
## Описание
С помощью сервиса можно обрабатывать данные о землетрясениях, загруженные пользователем, хранить их и визуализировать в виде графиков.

## Endpoints
### create_user
`POST /create_user` создаёт нового пользователя в базе данных. Пользователь идентифицируется по электронной почте.
На вход принимаются аргументы email и db (сеанс базы данных, полученный с помощью зависимости get_db).
### upload_file
`POST /upload_file` позволяет пользователю загрузить файл с данными о землетрясении. Данные будут загруженны на диск, а пути до них будут храниться в базе данных.
Функция принимает на вход:
- email: для идентификации пользователя
- file: файл с данными о землетрясении
- type: тип данных файла
- datetime_start: начальная дата для файла
- datetime_end: конечная дата для файла
- db: сеанс базы данных, полученный с помощью зависимости get_db
### last_uploaded_files
`GET /last_uploaded_files/` возвращает последний загруженный файл для определённого пользователя. На вход принимаются аргументы email и db (сеанс базы данных, полученный с помощью зависимости get_db). 
### files_by_date
`GET /files_by_date/` возвращает данные о землетрясении для определённой даты. Принимает в качестве аргументов email, date (дата для которой запрашиваются данные) и db (сеанс базы данных, полученный с помощью зависимости get_db).
## drow_map
`POST /drow_map` создает график на основе данных об землетрясении и предоставляет его пользователю. График сохраняется и возвращается пользователю в виде изображения. Аргументы функции:
- file_id: айди файла
- plot_params: некоторые параметры для построения (dates, markers, lon_limits, lat_limits, clims)
- db: сеанс базы данных, полученный с помощью зависимости get_db
### drow_distance_time
`POST /drow_distance_time` создает график расстояния-времени на основе данных об землетрясении и предоставляет его пользователю. График сохраняется и возвращается пользователю в виде изображения. Аргументы функции:
- file_id: айди файла
- plot_params: некоторые параметры для построения (epcs, clims)
- db: сеанс базы данных, полученный с помощью зависимости get_db

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
pip install poetry
poetry install
```
Запустите микросервис.
```
uvicorn app.main:api --reload --port 8083
```
## Дополнительная информация
Микросервис использует:
- **FastAPI** для создания программного интерфейса
- **loguru** для логирования
- **pytest** для автоматизации модульного тестирования
- **conda** для создания виртуального окружения и управления зависимостями
- [turkey_eq_monitor](https://github.com/dzhoshua/turkey_eq_monitor.git) для построения графиков.

## Лицензия
MIT
