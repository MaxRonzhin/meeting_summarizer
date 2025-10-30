"""
Утилита загрузки моделей.

Предоставляет функции для автоматической загрузки
и настройки моделей Whisper и LLM.
"""

import os
import urllib.request
import whisper
from tqdm import tqdm
from config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class DownloadProgressBar(tqdm):
    """
    Прогресс-бар для загрузки файлов.
    
    Расширяет tqdm для отображения прогресса загрузки файлов.
    """
    
    def update_to(self, b=1, bsize=1, tsize=None):
        """
        Обновляет прогресс-бар при загрузке.
        
        Args:
            b: Количество блоков переданных
            bsize: Размер блока
            tsize: Общий размер
        """
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_llm_model():
    """
    Скачивает LLM модель если она отсутствует.
    
    Проверяет наличие модели в папке models и скачивает
    при необходимости с отображением прогресса.
    
    Returns:
        str: Путь к загруженной модели
        
    Raises:
        Exception: Если загрузка не удалась
    """
    models_dir = "models"
    model_path = os.path.join(models_dir, settings.LLM_MODEL_NAME)
    
    # Создаем папку для моделей
    os.makedirs(models_dir, exist_ok=True)
    
    if os.path.exists(model_path):
        logger.info(f"LLM модель уже существует: {model_path}")
        return model_path
    
    logger.info(f"Скачивание LLM модели: {settings.LLM_MODEL_NAME}")
    logger.info("Это может занять несколько минут...")
    
    try:
        with DownloadProgressBar(unit='B', unit_scale=True,
                               miniters=1, desc=settings.LLM_MODEL_NAME) as t:
            urllib.request.urlretrieve(
                settings.LLM_MODEL_URL,
                filename=model_path,
                reporthook=t.update_to
            )
        logger.info(f"LLM модель успешно скачана: {model_path}")
        return model_path
    except Exception as e:
        logger.error(f"Ошибка скачивания LLM модели: {e}")
        raise

def ensure_whisper_model():
    """
    Проверяет и загружает Whisper модель при необходимости.
    
    Returns:
        whisper.Model: Загруженная модель Whisper
        
    Raises:
        Exception: Если загрузка не удалась
    """
    try:
        logger.info(f"Проверка Whisper модели: {settings.WHISPER_MODEL}")
        model = whisper.load_model(settings.WHISPER_MODEL)
        logger.info(f"Whisper модель '{settings.WHISPER_MODEL}' готова")
        return model
    except Exception as e:
        logger.error(f"Ошибка загрузки Whisper модели: {e}")
        raise

def setup_models():
    """
    Настраивает все модели перед запуском.
    
    Выполняет проверку и загрузку всех необходимых моделей.
    
    Returns:
        tuple: Кортеж (whisper_model, llm_model_path)
    """
    logger.info("=== Настройка моделей ===")
    
    # Загружаем Whisper
    whisper_model = ensure_whisper_model()
    
    # Скачиваем LLM
    llm_model_path = download_llm_model()
    
    logger.info("✅ Все модели настроены")
    return whisper_model, llm_model_path
