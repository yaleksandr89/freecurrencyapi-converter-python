import sys
from pathlib import Path

# Добавляем путь к директории `src` в sys.path
src_path = Path(__file__).parent / "src"
sys.path.append(str(src_path))

from src.main import start_converter

if __name__ == "__main__":
    start_converter()
