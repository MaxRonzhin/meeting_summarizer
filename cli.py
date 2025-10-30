#!/usr/bin/env python3
"""
Командный интерфейс Meeting Summarizer.

Предоставляет команды для управления приложением:
- Запуск транскрибирования
- Удаление загруженных моделей
- Проверка состояния моделей
- Просмотр результатов
"""

import argparse
import os
import shutil
import glob
from src.utils.logger import get_logger
from src.utils.model_downloader import setup_models
from main import main as start_meeting

logger = get_logger(__name__)

def clean_models():
    """
    Удаляет все загруженные модели.
    
    Удаляет:
    - Модели Whisper из кэша
    - Локальные LLM модели из папки models/
    """
    logger.info("Удаление загруженных моделей...")
    
    # Удаление папки с LLM моделями
    models_dir = "models"
    if os.path.exists(models_dir):
        try:
            shutil.rmtree(models_dir)
            logger.info(f"Папка {models_dir} удалена")
        except Exception as e:
            logger.error(f"Ошибка удаления {models_dir}: {e}")
    
    # Удаление кэша Whisper (опционально)
    whisper_cache = os.path.expanduser("~/.cache/whisper")
    if os.path.exists(whisper_cache):
        try:
            shutil.rmtree(whisper_cache)
            logger.info("Кэш Whisper удален")
        except Exception as e:
            logger.error(f"Ошибка удаления кэша Whisper: {e}")
    
    logger.info("Удаление моделей завершено")

def clean_results():
    """
    Удаляет все результаты (транскрипции и саммари).
    
    Удаляет содержимое папки results/.
    """
    logger.info("Удаление результатов...")
    
    results_dir = "results"
    if os.path.exists(results_dir):
        try:
            shutil.rmtree(results_dir)
            logger.info(f"Папка {results_dir} удалена")
        except Exception as e:
            logger.error(f"Ошибка удаления {results_dir}: {e}")
    else:
        logger.info("Папка results не найдена")
    
    logger.info("Удаление результатов завершено")

def check_models():
    """
    Проверяет наличие и состояние моделей.
    
    Выводит информацию о:
    - Наличии Whisper модели
    - Наличии LLM модели
    - Размерах файлов
    """
    logger.info("Проверка моделей...")
    
    # Проверка Whisper
    import whisper
    from config.settings import settings
    
    whisper_model_path = os.path.expanduser(f"~/.cache/whisper/{settings.WHISPER_MODEL}.pt")
    if os.path.exists(whisper_model_path):
        size = os.path.getsize(whisper_model_path) / (1024*1024)  # MB
        logger.info(f"Whisper модель найдена: {whisper_model_path} ({size:.1f} MB)")
    else:
        logger.info("Whisper модель не найдена (будет загружена при необходимости)")
    
    # Проверка LLM
    models_dir = "models"
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith('.gguf'):
                file_path = os.path.join(models_dir, file)
                size = os.path.getsize(file_path) / (1024*1024*1024)  # GB
                logger.info(f"LLM модель найдена: {file} ({size:.1f} GB)")
    else:
        logger.info("LLM модели не найдены (будут загружены при необходимости)")

def list_results():
    """
    Выводит список сохраненных результатов.
    
    Показывает все транскрипции и саммари в папке results/.
    """
    results_dir = "results"
    if not os.path.exists(results_dir):
        logger.info("Папка results не найдена")
        return
    
    files = sorted(glob.glob(os.path.join(results_dir, "*.*")))
    if not files:
        logger.info("Результаты не найдены")
        return
    
    logger.info("Сохраненные результаты:")
    for file in files:
        size = os.path.getsize(file) / 1024  # KB
        mtime = os.path.getmtime(file)
        from datetime import datetime
        mod_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"  {os.path.basename(file)} ({size:.1f} KB) [{mod_time}]")

def show_result(filename: str):
    """
    Показывает содержимое указанного результата.
    
    Args:
        filename: Имя файла для отображения
    """
    filepath = os.path.join("results", filename)
    if not os.path.exists(filepath):
        logger.error(f"Файл не найден: {filepath}")
        return
    
    logger.info(f"Содержимое {filename}:")
    logger.info("=" * 40)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        logger.error(f"Ошибка чтения файла: {e}")

def main():
    """
    Основная функция командного интерфейса.
    
    Обрабатывает аргументы командной строки и выполняет
    соответствующие действия.
    """
    parser = argparse.ArgumentParser(
        description="Meeting Summarizer - AI ассистент для видеоконференций",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python cli.py start          # Запустить транскрибирование
  python cli.py clean          # Удалить все модели
  python cli.py clean-results  # Удалить только результаты
  python cli.py check          # Проверить состояние моделей
  python cli.py list           # Показать список результатов
  python cli.py show <file>    # Показать содержимое результата
        """
    )
    
    parser.add_argument(
        'command',
        choices=['start', 'clean', 'clean-results', 'check', 'list', 'show'],
        help='Команда для выполнения'
    )
    
    parser.add_argument(
        'argument',
        nargs='?',
        help='Аргумент команды (для show - имя файла)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Включить подробный вывод'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        if args.command == 'start':
            start_meeting()
        elif args.command == 'clean':
            clean_models()
        elif args.command == 'clean-results':
            clean_results()
        elif args.command == 'check':
            check_models()
        elif args.command == 'list':
            list_results()
        elif args.command == 'show':
            if args.argument:
                show_result(args.argument)
            else:
                logger.error("Укажите имя файла для отображения")
                return 1
    except KeyboardInterrupt:
        logger.info("Операция прервана пользователем")
    except Exception as e:
        logger.error(f"Ошибка выполнения команды: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
