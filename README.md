# \_TaskFastAPI

1. Проектирование архитектуры
    Выбор моих основных технологий:

   # Архитектура проекта: Клиент-Серверное приложение

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

<!-- 

    Разделение на клиент-серверную архитектуру
    Проектирование моделей БД (3 основные сущности: Пользователь/Проект/Задача)
    Схемы взаимодействия между компонентами
    Результат: Схема архитектуры в draw.io/диаграмма классов


2. Серверная разработка (Backend)
    2.1. Базовая настройка
    Инициализяция Flask-приложения
    Подключение и конфигурация БД (SQLAlchemy)
    Создание базовых моделей

    2.2. Реализация API
    Роуты CRUD для всех сущностей
    PATCH-эндпоинты для частичного обновления
    Валидация через Pydantic (DTO для ввода/вывода)

    2.3. Дополнительные механизмы
    Сессии и транзакции БД
    Обработка ошибок (HTTP-статусы)
    Логирование ключевых операций
    Результат: Postman-коллекция с примерами запросов


3. Клиентская разработка (Frontend)
    3.1. Базовый каркас
    Настройка Flask-шаблонов (Jinja2)
    Система роутинга страниц
    Интеграция статических файлов (CSS/JS)

    3.2. Функциональные модули
    Система аутентификации (Flask-Login)
    Email-верификация с TTL-кодами
    Валидация форм на клиенте

    3.3. Визуализация данных
    Диаграммы задач (Matplotlib → base64)
    Адаптивный интерфейс
    Результат: Скриншоты ключевых интерфейсов


4. Интеграция и тестирование
    Настройка клиент-серверного взаимодействия
    Тестирование 边界-условий (например: удаление проекта с задачами)
    Проверка безопасности (SQL-инъекции, XSS)
    Результат: Чек-лист протестированных сценариев -->
