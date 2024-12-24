# LLM API
API для работы с LLM (Large Language Models), позволяющий фильтровать, добавлять и получать информацию о моделях.

## Установка
1. Клонируйте репозиторий:
   git clone https://github.com/Olyaste/llm-api.git
   cd llm-api
2. Создайте и активируйте виртуальное окружение:
   python -m venv venv
   .\venv\Scripts\activate  # Для Windows
   source venv/bin/activate  # Для Linux/MacOS
3. Установите зависимости:
   pip install -r requirements.txt
4. Убедитесь, что у вас установлен PostgreSQL и база данных `LLM` настроена.

## Запуск
Запустите сервер:
uvicorn main:app --reload
API будет доступен по адресу: http://127.0.0.1:8000

## Эндпоинты
### 1. `/llm_filtered`
Получить список моделей с фильтрами.
Метод: `GET`
Параметры (опционально):
- `price` (int): Цена
- `vpn` (bool): Статус доступности VPN
- `tag` (str): Тег модели
- `description_contains` (str): Подстрока в описании модели
- `page` (int): Страница (по умолчанию 1)
- `limit` (int): Лимит (по умолчанию 10)

### 2. `/request`
Получить данные из базы в виде потока.
Метод: `GET`
Параметры:
- `data` (str): Данные для запроса.

### 3. `/llm_info`
Добавить новые данные о моделях.
Метод: `POST`
Тело запроса:
[
  {
    "id": 1,
    "name": "Model 1",
    "description": "Description of model 1"
  }
]

## Логирование
Логирование ошибок настроено через `uvicorn`, ошибки будут записываться в консоль.

## Примечания
- Для работы API необходим PostgreSQL.
- Данные о моделях должны быть загружены в таблицы `llm`, `tariff`, `availability`, `tag`.