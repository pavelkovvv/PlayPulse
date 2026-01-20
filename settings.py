import os
import yaml

from typing import Union, Dict, Any


def load_config() -> Dict[str, Any]:
    """
    Загружает конфигурацию из файлов:
        1. config.default.yaml - базовые настройки
        2. config.yaml - пользовательские (перекрывают базовые)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_config_path = os.path.join(base_dir, 'config', 'config.default.yaml')
    custom_config_path = os.path.join(base_dir, 'config', 'config.yaml')

    def _load_yaml(path: str = None) -> Dict[str, Any]:
        if not os.path.exists(path):
            return {}
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    config = _load_yaml(default_config_path)
    config.update(_load_yaml(custom_config_path))

    return config


CONFIG = load_config()


def config_loader(key: str, default: Any = None) -> Union[str, list, dict, None]:
    """
    Возвращает значение по ключу из конфигурации.
    Поддерживает вложенные ключи через точку, например:
        config.loader('database.host')

    :param key: ключ или путь через точку
    :param default: значение по умолчанию, если ключ не найден
    """
    value = CONFIG
    for part in key.split('.'):
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]

    return value