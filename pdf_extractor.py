from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
import re
from typing import Optional, List, Tuple
import numpy as np

# Инициализация PaddleOCR - use_angle_cls=True включает классификатор угла
ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)

# Агрессивная нормализация для поиска
def normalize_for_search(s: str) -> str:
    """Удаляет все кроме букв и цифр для точного поиска"""
    s = s.lower()
    s = re.sub(r"[^a-z0-9]", "", s)
    return s

# Нормализация текста для вывода
def normalize(s: str) -> str:
    """Нормализует текст для читаемого вывода"""
    s = s.lower()
    s = re.sub(r"[^a-zа-я0-9 .,-]", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

# PDF -> PNG
def pdf_to_images(pdf_path: str, out_dir: str = "train", dpi: int = 300) -> List[Path]:
    """Конвертирует PDF в PNG изображения"""
    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)
    
    pages = convert_from_path(pdf_path, dpi=dpi)
    png_paths = []

    for i, page in enumerate(pages, start=1):
        png_file = out_dir_path / f"page_{i}.png"
        page.save(png_file, "PNG")
        png_paths.append(png_file)

    return png_paths

# Извлечение текста из изображения
def extract_text_from_image(image_path: Path) -> List[str]:
    """
    Извлекает текст из изображения с помощью PaddleOCR
    ИСПРАВЛЕНО: убрали параметр cls=True
    """
    # Вызываем ocr БЕЗ параметра cls
    result = ocr.ocr(str(image_path))
    
    # Проверка на пустой результат
    if not result or not result[0]:
        return []
    
    # Извлечение текста из результата
    lines = [line_info[1][0] for line_info in result[0]]
    return lines

# Извлечение страницы по фразе
def extract_target_page_paddle(
    pdf_path: str, 
    phrase: str, 
    out_dir: str = "train", 
    dpi: int = 300
) -> Tuple[Optional[Path], List[str]]:
    """
    Ищет фразу в PDF и возвращает страницу с текстом после фразы
    
    Args:
        pdf_path: путь к PDF файлу
        phrase: искомая фраза
        out_dir: директория для сохранения PNG
        dpi: разрешение для конвертации
    
    Returns:
        (путь к PNG файлу, список строк после фразы) или (None, [])
    """
    png_files = pdf_to_images(pdf_path, out_dir, dpi)
    phrase_norm = normalize_for_search(phrase)

    for png_file in png_files:
        lines = extract_text_from_image(png_file)
        
        # Поиск фразы
        for idx, line in enumerate(lines):
            if phrase_norm in normalize_for_search(line):
                # Возвращаем все строки ПОСЛЕ найденной фразы
                remaining_lines = lines[idx + 1:]
                return png_file, remaining_lines
    
    return None, []

# Функция для очистки временных файлов
def cleanup_temp_files(out_dir: str = "train"):
    """Удаляет временные PNG файлы"""
    out_dir_path = Path(out_dir)
    if out_dir_path.exists():
        for file in out_dir_path.glob("*.png"):
            file.unlink()
        try:
            out_dir_path.rmdir()
        except OSError:
            pass