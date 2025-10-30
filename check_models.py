from src.utils.model_downloader import setup_models
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    print("=== Автоматическая настройка моделей ===")
    try:
        whisper_model, llm_model_path = setup_models()
        print("\n🎉 Все модели успешно настроены!")
        print(f"📍 Whisper модель: {whisper_model}")
        print(f"📍 LLM модель: {llm_model_path}")
    except Exception as e:
        print(f"\n❌ Ошибка настройки моделей: {e}")
        return False
    return True

if __name__ == "__main__":
    main()
