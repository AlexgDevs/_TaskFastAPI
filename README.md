# \_TaskFastAPI

1. Проектирование архитектуры
    Выбор моих основных технологий:

   # Архитектура проекта: Клиент-Серверное приложение (Монолит)

## 1. Проектирование архитектуры
### Выбор технологического стека

#### Безопасность конфигурации
- **`Dotenv`** (.env файлы)
  - 📌 Безопасное хранение чувствительных данных
  - 🔒 Примеры использования:
    ```ini
    SECRET_KEY=your-flask-secret
    DATABASE_URL=postgresql://user:pass@localhost/db
    GMAIL_PWD=XXX-XXX-XXX
    ```

#### Серверная часть (API)
- **`FastAPI`**
  - 🚀 Высокопроизводительные API-эндпоинты
  - 🛡️ Параноидальная валидация через Pydantic
  - 💡 Пример:
    ```python
    @app.patch("/tasks/{user_id}/{id}")
    async def update_task(task: TaskUpdate):
        """Частичное обновление задачи"""
    ```

#### Клиентская часть (Frontend)
- **`Flask`**
  - 🖥️ Рендеринг страниц через Jinja2
  - 🗺️ Маршрутизация интерфейсов
  - 💡 Пример:
    ```python
    @app.route("/projects")
    @login_required
    def projects():
        """Список проектов пользователя"""
    ```

#### Аутентификация
- **`Flask-Login`**
  - 🔐 Система сессий пользователей
  - 🛡️ Защитные декораторы:
    ```python
    @admin_required  # Только для админов
    @required_not_authenticated  # Только для гостей
    ```

#### Формы
- **`Flask-WTF + WTForms`**
  - 📝 Генерация и валидация форм
  - 🔒 Пример формы:
    ```python
    class LoginForm(FlaskForm):
        email = StringField(validators=[DataRequired(), Email()])
        password = PasswordField(validators=[DataRequired()])
    ```

## 2. Серверная реализация

### Работа с данными
- **`SQLAlchemy`** (ORM)
  - 🛡️ Защита от SQL-инъекций
  - 🗃️ Модели:
    ```python
    class Task(Base):
        __tablename__ = 'tasks'
        id = Column(Integer, primary_key=True)
        title = Column(String(100), nullable=False)
        status = Column(String(20), default='not_started')
    ```

### Валидация
- **`Pydantic`**
  - 📋 Схемы данных:
    ```python
    class TaskCreate(BaseModel):
        title: str = Field(min_length=3, max_length=100)
        status: Literal['not_started', 'in_progress', 'done']
    ```

### Запуск
- **`Uvicorn`** (ASGI-сервер)
  - ⚡ Асинхронная обработка запросов
  - ⚙️ Конфигурация:
    ```bash
    uvicorn run_server:app --reload --port=8000
    ```

## 3. Клиентская реализация

### Шаблоны
- **`Jinja2`**
  - 🧩 Пример интеграции:
    ```html
    {% for project in user.projects %}
    <div class="project">{{ project.name }}</div>
    {% endfor %}
    ```

### Визуализация
- **`Matplotlib + NumPy`**
  - 📊 Круговая диаграмма статусов:
    ```python
    plt.pie(task_counts, labels=statuses, autopct='%1.1f%%')
    ```

### API-взаимодействие
- **`Requests`**
  - 🔄 Пример запроса:
    ```python
    requests.patch(
        f"{API_URL}/tasks/{task_id}",
        json={"status": "done"},
        headers={"Authorization": f"Bearer {token}"}
    )
    ```

## 4. Безопасность

### Хеширование
- **`Werkzeug`**
  - 🔐 Методы:
    ```python
    hash_pwd = generate_password_hash('secret')
    check_password_hash(hash_pwd, 'input')  # → True/False
    ```

### Защита форм
- **CSRF-токены**
  ```html
  <form method="post">
    {{ form.hidden_tag() }}
    <!-- Поля формы -->
  </form>


# Сервер (API)
uvicorn run_server:app --reload --port=8000

# Клиент (Frontend)
flask run --port=5000



# Этапы разработки проекта

## 1. Проектирование архитектуры Сервер + Клиент

project/
├── server/ # Серверная часть (FastAPI)
│ ├── db/ # Модели и настройки БД
│ ├── routers/ # API-эндпоинты
│ ├── schemas/ # Pydantic-схемы
│ └── utils/ # Вспомогательные утилиты
│
├── client/ # Клиентская часть (Flask)
│ ├── db/ # Локальные модели
│ ├── routers/ # Маршруты Flask
│ ├── static/ # CSS/JS/Изображения
│ ├── templates/ # HTML-шаблоны (Jinja2)
│ └── utils/ # Вспомогательные утилиты
│
├── run_server.py # Запуск: uvicorn run_server:app --reload --port=8000
├── run_client.py # Запуск: flask run --port=5000
├── .env # Конфигурация окружения
├── .gitignore # Игнорируемые файлы
└── treker.db # SQLite база данных


## 2. Серверная часть

### Модели базы данных
```python
# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str]
    email_confirmation: Mapped[bool] = mapped_column(default=False)
    verifi_code: Mapped[str] = mapped_column(nullable=True)
    joined: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    role: Mapped[Literal['user', 'admin', 'moderator']] = mapped_column(default='user')

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='user', cascade='all, delete-orphan')
    projects: Mapped[List['Project']] = relationship('Project', back_populates='user', cascade='all, delete-orphan')

# Модель Задачи
class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    status: Mapped[Literal['not_started', 'in_progress', 'in_review', 'done', 'burned_down']] = mapped_column(default='not_started')
    dead_line: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    photo: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='tasks', uselist=False)

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    project: Mapped['Project'] = relationship('Project', back_populates='tasks', uselist=False)


# Модель Проекта
class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(2048))
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship('User', back_populates='projects', uselist=False)

    tasks: Mapped[List['Task']] = relationship('Task', back_populates='project', cascade='all, delete-orphan')
```
## 3. Клиектская часть
### Создание АПИ на серверной части.

🌐 API Endpoints
Метод	Путь	Действие
GET	/users/{id}	Получить пользователя
POST	/projects Создать проект
PATCH	/tasks/{user_id}/{id}	Частично обновить задачу
DELETE	/projects/{user_id}/{id}	Удалить проект


### 📦 Pydantic-схемы
4. Создание моделей для входных/выходных данных на Pydantic


### Страницы Сайта
5. создание страниц и их структура в templates | html + jinja
- регистрации
- входа
- выхода
- доска статистики задач
- доска проектов пользователя
- профиль


### 6. стилизация этих страниц с помощью css + js | static/styles/...
### 7. Создание маршрутов для перенаправления, обработки форм и валидации в routers/ с помощью Flask
### 8. Настройка авторизации спомощью Flsk-login в utils/secure
### 9. Создание функций для генерации истекающего кода и отправки сообщения с кодом на почту в utils/email_send
### 10. Создание форм для страниц с помощью FlaskWTF + WTforms schemas/






