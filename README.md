# Elasticsearch Project Documentation

## **Описание проекта**
Этот проект представляет собой веб-приложение для поиска фильмов, использующее **Elasticsearch** для индексации и поиска данных. Приложение также взаимодействует с базой данных SQLite для хранения информации о фильмах, пользователях и комментариях.

---

## **Структура проекта**

```
project/
├── main.py                 # Основной файл приложения (FastAPI)
├── elasticsearch_utils.py  # Утилиты для работы с Elasticsearch
├── transformer_utils.py    # Генерация эмбеддингов с помощью модели Transformers
├── models.py               # Модели данных Pydantic
├── templates/              # HTML-шаблоны для интерфейса
│   ├── index.html          # Главная страница
│   ├── search.html         # Страница результатов поиска
├── data/                   # Данные для индексации
│   └── movies_metadata.csv.zip # CSV-файл с информацией о фильмах
├── config/                 # Конфигурационные файлы
│   └── elasticsearch.yml   # Настройки Elasticsearch
└── movies.db               # SQLite база данных
```

---

## **Как запустить проект**

### **1. Установка зависимостей**

1. Убедитесь, что установлен Python 3.9+
2. Установите зависимости из файла `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

### **2. Установка и запуск Elasticsearch**

1. Скачайте Elasticsearch.
2. Распакуйте архив.
3. Запустите Elasticsearch командой:
   ```bash
   bin\elasticsearch.bat
   ```
4. Проверьте, что Elasticsearch работает, открыв в браузере:
   ```
   http://localhost:9200
   ```

### **3. Инициализация базы данных**

Для создания структуры базы данных выполните команду:
```bash
python main.py init_db
```

### **4. Запуск сервера**

Для запуска приложения выполните:
```bash
python main.py start
```

Приложение будет доступно по адресу:
```
http://127.0.0.1:8000
```

---

## **Как использовать**

1. Откройте главную страницу приложения:
   ```
   http://127.0.0.1:8000
   ```
2. Используйте строку поиска для ввода запроса. Выберите тип индексации:
   - **tfidf**: поиск по TF-IDF вектору.
   - **embeddings**: поиск по эмбеддингам, созданным с помощью модели Transformers.
3. Нажмите кнопку поиска, чтобы увидеть результаты.

---

## **Параметры команды**

Скрипт `main.py` поддерживает следующие команды:

- **start**: Запуск веб-сервера.
  ```bash
  python main.py start
  ```

- **init_db**: Инициализация базы данных SQLite.
  ```bash
  python main.py init_db
  ```

---

## **Схема базы данных**

```plaintext
users:
  - user_id (INTEGER, PK)
  - username (TEXT)
  - password (TEXT)
  - email (TEXT)

movies:
  - movie_id (INTEGER, PK)
  - title (TEXT)
  - overview (TEXT)
  - release_date (TEXT)
  - embedding (TEXT)

comments:
  - comment_id (INTEGER, PK)
  - movie_id (INTEGER, FK -> movies.movie_id)
  - user_id (INTEGER, FK -> users.user_id)
  - comment (TEXT)
  - created_at (DATETIME)
```

---

## **Описание ключевых компонентов**

### **1. main.py**
Основной файл приложения. Реализует следующие функции:
- Запуск веб-сервера с использованием FastAPI.
- Маршруты:
  - `GET /`: Главная страница.
  - `POST /search`: Обработка запросов на поиск.
- Инициализация базы данных SQLite (таблицы для фильмов, пользователей, комментариев).

### **2. elasticsearch_utils.py**
- Создание клиента Elasticsearch.
- Индексация данных о фильмах в Elasticsearch (TF-IDF и эмбеддинги).
- Реализация функции поиска по двум индексам:
  - **movies_tfidf**
  - **movies_embeddings**

### **3. transformer_utils.py**
- Использование модели `sentence-transformers/all-MiniLM-L6-v2` для генерации эмбеддингов текста.
- Функция `get_embedding(text)` возвращает векторное представление строки текста.

### **4. models.py**
- Определяет модели данных с использованием Pydantic:
  - `SearchRequest`: запрос на поиск.
  - `SearchResult`: результат поиска.

### **5. HTML-шаблоны**
- **index.html**: Форма поиска.
- **search.html**: Вывод результатов поиска.

---

## **Как добавить данные**

### **1. Индексация фильмов**
Для загрузки данных из файла `movies_metadata.csv` в Elasticsearch используйте функцию `insert_data_to_elasticsearch()` из файла `elasticsearch_utils.py`.

Пример использования:
```python
from elasticsearch_utils import insert_data_to_elasticsearch
insert_data_to_elasticsearch()
```

### **2. Добавление фильмов в SQLite**
В таблицу `movies` можно добавлять данные вручную или через Python-скрипт, используя библиотеку `sqlite3`.

Пример:
```python
import sqlite3
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()
cursor.execute("INSERT INTO movies (title, overview) VALUES (?, ?)", ("Movie Title", "Movie Overview"))
conn.commit()
conn.close()
```

---

## **Примеры API-запросов**

### **Поиск фильмов (POST /search)**
Пример запроса с использованием Postman или cURL:

#### Запрос:
```json
{
  "query": "space adventure",
  "index_type": "tfidf"
}
```

#### Ответ:
```json
[
  {
    "title": "Interstellar",
    "overview": "A team of explorers travel through a wormhole in space.",
    "score": 1.23
  },
  {
    "title": "Gravity",
    "overview": "Two astronauts work together to survive after an accident.",
    "score": 1.12
  }
]
```


