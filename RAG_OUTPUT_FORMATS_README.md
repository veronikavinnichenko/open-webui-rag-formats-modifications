# RAG Output Formats - Open WebUI

## Обзор

Система RAG Output Formats позволяет пользователям настраивать стиль и формат ответов при использовании Retrieval-Augmented Generation (RAG). Поддерживается три уровня настроек:

1. **Per-Chat** - настройки для конкретного чата (высший приоритет)
2. **Per-User** - настройки пользователя по умолчанию
3. **Global** - глобальные настройки системы

## Доступные форматы

### 1. Compact
- **Описание**: Краткий ответ с ключевой информацией
- **Характеристики**: 
  - До 100 слов
  - Использует маркированные списки
  - Только основные цитаты
  - Прямой и по существу

### 2. Detailed
- **Описание**: Подробный ответ с объяснениями
- **Характеристики**:
  - Тщательный анализ и контекст
  - Релевантные примеры и объяснения
  - Правильные цитаты [id]
  - Структурированный ответ с разделами

### 3. Academic
- **Описание**: Академический стиль с формальным языком
- **Характеристики**:
  - Формальный, академический язык
  - Правильные цитаты [id] с ссылками на источники
  - Структура: введение, основная часть, заключение
  - Критический анализ и обсуждение

### 4. Table
- **Описание**: Структурированный табличный формат
- **Характеристики**:
  - Четкая таблица с соответствующими столбцами
  - Заголовки для каждого столбца
  - Цитаты [id] для информации об источниках
  - Легко читаемая и понятная таблица

### 5. List
- **Описание**: Организованный список
- **Характеристики**:
  - Нумерованные или маркированные списки
  - Группировка связанных элементов
  - Цитаты [id] для информации об источниках
  - Логический поток и организация

## API Endpoints

### Получение доступных форматов
```http
GET /api/v1/retrieval/output-formats
```

### Обновление RAG параметров чата
```http
POST /api/v1/chats/{chat_id}/rag-params
Content-Type: application/json

{
  "rag": {
    "output_format": "compact",
    "table_include_headers": true,
    "table_max_columns": 5,
    "list_style": "bullet"
  }
}
```

### Обновление пользовательских настроек
```http
POST /api/v1/users/user/settings/update
Content-Type: application/json

{
  "rag": {
    "output_format": "detailed",
    "table_include_headers": true,
    "table_max_columns": 3,
    "list_style": "numbered"
  }
}
```

## Структура данных

### Параметры чата (chat.meta.rag)
```json
{
  "rag": {
    "output_format": "compact",
    "table_include_headers": true,
    "table_max_columns": 5,
    "list_style": "bullet"
  }
}
```

### Настройки пользователя (user.settings)
```json
{
  "rag": {
    "output_format": "detailed",
    "table_include_headers": true,
    "table_max_columns": 3,
    "list_style": "numbered"
  }
}
```

### Глобальная конфигурация
```python
# backend/open_webui/config.py
RAG_OUTPUT_FORMAT_DEFAULT = "detailed"
RAG_OUTPUT_FORMATS = ["compact", "detailed", "academic", "table", "list"]
```

## Приоритеты настроек

1. **Per-Chat** (высший приоритет)
   - Настройки применяются только к конкретному чату
   - Переопределяют пользовательские и глобальные настройки

2. **Per-User**
   - Настройки по умолчанию для пользователя
   - Применяются ко всем чатам пользователя
   - Переопределяют глобальные настройки

3. **Global** (низший приоритет)
   - Системные настройки по умолчанию
   - Применяются, если не указаны другие настройки

## Примеры использования

### Установка формата для чата
```javascript
// Frontend
const response = await fetch(`/api/v1/chats/${chatId}/rag-params`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    rag: {
      output_format: 'table',
      table_include_headers: true,
      table_max_columns: 4
    }
  }
});
```

### Установка пользовательского формата по умолчанию
```javascript
// Frontend
const response = await fetch('/api/v1/users/user/settings/update', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    rag: {
      output_format: 'academic'
    }
  }
});
```

## Конфигурация

### Переменные окружения
```bash
# Формат по умолчанию
RAG_OUTPUT_FORMAT_DEFAULT=detailed

# Доступные форматы
RAG_OUTPUT_FORMATS=compact,detailed,academic,table,list
```

### Кастомные шаблоны
Вы можете переопределить шаблоны, установив переменные окружения:
```bash
RAG_COMPACT_TEMPLATE="Ваш кастомный шаблон для compact формата"
RAG_DETAILED_TEMPLATE="Ваш кастомный шаблон для detailed формата"
# и т.д.
```

## Логирование

Система логирует использование RAG форматов для аналитики:
```
INFO: RAG output format used: compact (source: chat, chat_id: 123, user_id: 456)
INFO: RAG output format used: detailed (source: user, chat_id: 123, user_id: 456)
INFO: RAG output format used: detailed (source: global, chat_id: 123, user_id: 456)
```

## Миграции

Не требуются. Настройки RAG для чатов хранятся в существующем JSON-поле `chat.meta` под ключом `rag`.

## Тестирование

### Per-User настройки
1. Установите настройку в профиле пользователя
2. Создайте новый чат
3. Проверьте, что применяется выбранный формат

### Per-Chat настройки
1. Переопределите формат в конкретном чате
2. Убедитесь, что он имеет приоритет над пользовательскими настройками

### Глобальные настройки
1. Если ни у пользователя, ни в чате нет настроек
2. Должен применяться `RAG_OUTPUT_FORMAT_DEFAULT`

## Поддержка

При возникновении проблем:
1. Проверьте логи приложения
2. Миграции не требуются
3. Проверьте корректность JSON в параметрах
4. Убедитесь, что формат поддерживается системой
