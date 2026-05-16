# -*- coding: utf-8 -*-
import sys

# Читаем файл
with open('index.html', 'rb') as f:
    content = f.read()

# Декодируем как Windows-1251, затем кодируем как UTF-8
try:
    text = content.decode('utf-8')
    # Проверяем, есть ли проблема с кодировкой
    if 'Р' in text[:100]:
        text = text.encode('utf-8').decode('latin-1')
        text = text.encode('latin-1').decode('utf-8')
except:
    text = content.decode('utf-8')

# Заменяем испорченные символы
text = text.replace('Р’РёР·СѓР°Р»РёР·Р°С‚РѕСЂ вЂ” DOUBLE RINGS', 'Визуализатор — DOUBLE RINGS')
text = text.replace('РџСЂРёРјРµСЂСЊС‚Рµ РѕС‚РґРµР»РѕС‡РЅС‹Рµ РјР°С‚РµСЂРёР°Р»С‹ РІ РёРЅС‚РµСЂСЊРµСЂРµ РѕРЅР»Р°Р№РЅ', 'Примерьте отделочные материалы в интерьере онлайн')

# Сохраняем как UTF-8 без BOM
with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(text)

print("File fixed!")
