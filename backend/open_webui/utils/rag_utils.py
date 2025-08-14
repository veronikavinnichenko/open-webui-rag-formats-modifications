import logging
from typing import Optional, Dict, Any
from open_webui.env import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["RAG"])


def get_rag_output_format(
    chat_params: Optional[Dict[str, Any]] = None,
    user_settings: Optional[Dict[str, Any]] = None,
    global_config: Optional[Dict[str, Any]] = None
) -> str:
    """
    Определяет формат вывода RAG с учетом приоритетов:
    1. Per-Chat (высший приоритет)
    2. Per-User
    3. Global (по умолчанию)
    
    Args:
        chat_params: Параметры чата (из chat.params)
        user_settings: Настройки пользователя (из user.settings)
        global_config: Глобальная конфигурация
        
    Returns:
        str: Название формата вывода
    """
    # 1. Per-Chat (высший приоритет)
    if chat_params and isinstance(chat_params, dict):
        rag_settings = chat_params.get("rag", {})
        if isinstance(rag_settings, dict) and rag_settings.get("output_format"):
            format_type = rag_settings["output_format"]
            log.debug(f"Using per-chat RAG output format: {format_type}")
            return format_type
    
    # 2. Per-User
    if user_settings and isinstance(user_settings, dict):
        rag_settings = user_settings.get("rag", {})
        if isinstance(rag_settings, dict) and rag_settings.get("output_format"):
            format_type = rag_settings["output_format"]
            log.debug(f"Using per-user RAG output format: {format_type}")
            return format_type
    
    # 3. Global (по умолчанию)
    default_format = "detailed"
    if global_config and isinstance(global_config, dict):
        default_format = global_config.get("RAG_OUTPUT_FORMAT_DEFAULT", "detailed")
    
    log.debug(f"Using global RAG output format: {default_format}")
    return default_format


def get_rag_template_by_format(format_type: str, global_config: Optional[Dict[str, Any]] = None) -> str:
    """
    Получает шаблон RAG для указанного формата
    
    Args:
        format_type: Тип формата (compact, detailed, academic, table, list)
        global_config: Глобальная конфигурация с шаблонами
        
    Returns:
        str: Шаблон для указанного формата
    """
    if not global_config:
        # Fallback к встроенным шаблонам
        from open_webui.config import RAG_FORMAT_TEMPLATES, RAG_TEMPLATE
        
        if format_type in RAG_FORMAT_TEMPLATES:
            return RAG_FORMAT_TEMPLATES[format_type]
        else:
            log.warning(f"Unknown RAG output format: {format_type}, using default")
            return RAG_TEMPLATE
    
    # Используем шаблоны из конфигурации
    templates = global_config.get("RAG_FORMAT_TEMPLATES", {})
    if format_type in templates:
        return templates[format_type]
    else:
        log.warning(f"Unknown RAG output format: {format_type}, using default")
        return global_config.get("RAG_TEMPLATE", "")


def validate_rag_format(format_type: str, available_formats: Optional[list] = None) -> bool:
    """
    Проверяет, является ли формат допустимым
    
    Args:
        format_type: Проверяемый формат
        available_formats: Список доступных форматов
        
    Returns:
        bool: True если формат допустим
    """
    if not available_formats:
        from open_webui.config import RAG_OUTPUT_FORMATS
        available_formats = RAG_OUTPUT_FORMATS
    
    return format_type in available_formats


def apply_rag_format_settings(
    chat_params: Optional[Dict[str, Any]] = None,
    user_settings: Optional[Dict[str, Any]] = None,
    global_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Применяет настройки RAG формата и возвращает конфигурацию для генерации
    
    Args:
        chat_params: Параметры чата
        user_settings: Настройки пользователя
        global_config: Глобальная конфигурация
        
    Returns:
        Dict: Конфигурация RAG с примененными настройками
    """
    # Определяем формат вывода
    output_format = get_rag_output_format(chat_params, user_settings, global_config)
    
    # Получаем соответствующий шаблон
    template = get_rag_template_by_format(output_format, global_config)
    
    # Собираем дополнительные настройки формата
    format_settings = {}
    
    # Настройки для таблиц
    if output_format == "table":
        if chat_params and isinstance(chat_params, dict):
            rag_settings = chat_params.get("rag", {})
            if isinstance(rag_settings, dict):
                format_settings.update({
                    "include_headers": rag_settings.get("table_include_headers", True),
                    "max_columns": rag_settings.get("table_max_columns", 5)
                })
        elif user_settings and isinstance(user_settings, dict):
            rag_settings = user_settings.get("rag", {})
            if isinstance(rag_settings, dict):
                format_settings.update({
                    "include_headers": rag_settings.get("table_include_headers", True),
                    "max_columns": rag_settings.get("table_max_columns", 5)
                })
    
    # Настройки для списков
    elif output_format == "list":
        if chat_params and isinstance(chat_params, dict):
            rag_settings = chat_params.get("rag", {})
            if isinstance(rag_settings, dict):
                format_settings["list_style"] = rag_settings.get("list_style", "bullet")
        elif user_settings and isinstance(user_settings, dict):
            rag_settings = user_settings.get("rag", {})
            if isinstance(rag_settings, dict):
                format_settings["list_style"] = rag_settings.get("list_style", "bullet")
    
    return {
        "output_format": output_format,
        "template": template,
        "format_settings": format_settings
    }


def log_rag_format_usage(
    format_type: str,
    source: str,
    chat_id: Optional[str] = None,
    user_id: Optional[str] = None
):
    """
    Логирует использование RAG формата для аналитики
    
    Args:
        format_type: Используемый формат
        source: Источник настройки (chat, user, global)
        chat_id: ID чата (если применимо)
        user_id: ID пользователя (если применимо)
    """
    log.info(
        f"RAG output format used: {format_type} (source: {source}, "
        f"chat_id: {chat_id}, user_id: {user_id})"
    )
