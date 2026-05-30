import re

# Список запрещённых слов (только основы)
BAD_WORDS = [
    'хуй', 'пизд', 'бля', 'залуп', 'пидор', 'мудак', 'гандон',
    'сук', 'еб', 'еба', 'ёб', 'хер', 'шлюх', 'лох', 'чмо',
    'дебил', 'идиот', 'кретин', 'даун', 'редиск', 'гнид', 'твар'
]

# Преобразования для нормализации
def normalize_text(text):
    """Приводит текст к «чистому» виду для поиска"""
    if not text:
        return ''
    text = text.lower()
    # Латиница → кириллица
    mapping = str.maketrans({
        'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с',
        'y': 'у', 'x': 'х', 'k': 'к', 'm': 'м', 't': 'т',
        'h': 'н', 'b': 'в', 'i': 'и', 'j': 'й'
    })
    text = text.translate(mapping)
    # Цифры → буквы
    digits = {'0': 'о', '1': 'и', '3': 'з', '4': 'ч', '6': 'б', '7': 'т', '8': 'в'}
    for d, letter in digits.items():
        text = text.replace(d, letter)
    # Убираем всё, кроме букв
    text = re.sub(r'[^а-яё]', '', text)
    return text

def has_profanity(text):
    """Проверяет, содержит ли текст нецензурную лексику"""
    if not text:
        return False
    normalized = normalize_text(text)
    for word in BAD_WORDS:
        if word in normalized:
            return True
    return False

def censor_text(text, replacement='***'):
    """Заменяет нецензурные слова на звёздочки"""
    if not text:
        return text
    result = text
    for word in BAD_WORDS:
        # Ищем слово с возможными разделителями между буквами
        pattern = r'\b' + r'[\W_]*'.join(word) + r'\b'
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result