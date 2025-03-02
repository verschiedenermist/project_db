# -*- coding: utf-8 -*-
"""main

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kEtai5u0x1Ly8GqYIMDW78VcSrdld7yx
"""

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
from typing import List
from elasticsearch_utils import search_movie
from models import SearchRequest, SearchResult
import sqlite3
import argparse
import sys
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
async def startup():
    # создание таблиц в базе данных, если они не существуют
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # создание таблицы фильмов (если она еще не существует)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        overview TEXT
    );
    """)
    
    # создание таблицы пользователей (если она еще не существует)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        email TEXT
    );
    """)
    
    # создание таблицы комментариев (если она еще не существует)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_id INTEGER,
        user_id INTEGER,
        comment TEXT,
        created_at DATETIME,
        FOREIGN KEY(movie_id) REFERENCES movies(movie_id),
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    );
    """)
    
    conn.commit()
    conn.close()

# главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# страница поиска
@app.post("/search", response_class=HTMLResponse)
async def search(request: Request):
    form_data = await request.form()
    search_request = SearchRequest(query=form_data.get("query"), index_type=form_data.get("index_type"))
    
    try:
        results = search_movie(search_request.query, search_request.index_type)
        return templates.TemplateResponse("search.html", {
            "request": request,
            "results": results,
            "query": search_request.query,
            "index_type": search_request.index_type,
            "search_time": 0  
        })
    except Exception as e:
        print(f"Error during search: {e}")
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})

# Пример функции поиска 
#def search_movie(query: str, index_type: str):
#    return ["Movie 1", "Movie 2"]  # Пример возвращаемых результатов

# главная страница
#@app.get("/", response_class=HTMLResponse)
#async def read_root(request: Request):
#    return templates.TemplateResponse("index.html", {"request": request})

# страница поиска
#@app.post("/search", response_class=HTMLResponse)
#async def search(request: SearchRequest):
#    results = search_movie(request.query, request.index_type)
#    return templates.TemplateResponse("search.html", {
#        "request": request,
#        "results": results
#    })

# модели для запросов
class SearchRequest(BaseModel):
    query: str
    index_type: str  # tfidf или embeddings

class SearchResult(BaseModel):
    title: str
    overview: str
    score: float

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # argparse для обработки команд
    parser = argparse.ArgumentParser(description="CLI для управления приложением")
    
    parser.add_argument(
        "command", 
        choices=["start", "init_db"], 
        help="Команда для выполнения: 'start' для запуска сервера, 'init_db' для инициализации базы данных"
    )
    
    args = parser.parse_args()

    if args.command == "start":
        print("Запуск сервера...")
        run_server()
    elif args.command == "init_db":
        print("Инициализация базы данных...")
        startup()
        print("База данных инициализирована.")