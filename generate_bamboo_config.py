import csv
import json

materials = {}
current_category = None

with open('doublerings/store-10621549-202605151913.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    
    for row in reader:
        title = row.get('Title', '').strip()
        photo = row.get('Photo', '').strip()
        category = row.get('Category', '').strip()
        
        # Пропускаем пустые строки и заголовки
        if not title or not photo or title.startswith(';'):
            continue
            
        # Определяем категорию из заголовка
        if 'Cерия ткань' in title:
            current_category = 'Cерия ткань'
        elif 'Cерия дерево' in title:
            current_category = 'Cерия дерево'
        elif 'Cерия метал' in title:
            current_category = 'Cерия метал'
        elif 'Cерия мрамор' in title:
            current_category = 'Cерия мрамор'
        elif 'Cерия блеск кристала' in title:
            current_category = 'Cерия блеск кристала'
        elif 'Cерия кожа' in title:
            current_category = 'Cерия кожа'
        else:
            continue
        
        # Извлекаем название цвета/текстуры
        if ' - ' in title:
            name = title.split(' - ')[-1]
        else:
            name = title
        
        if current_category not in materials:
            materials[current_category] = []
        
        # Берём только первое изображение (если несколько)
        image_url = photo.split()[0] if photo else ''
        
        materials[current_category].append({
            'name': name,
            'url': image_url
        })

# Выводим JSON
config = {
    'Бамбуковые панели': {
        'id': 'bamboo-main',
        'categories': materials
    }
}

print(json.dumps(config, ensure_ascii=False, indent=4))

# Сохраняем в файл
with open('doublerings/interior-visualizer/bamboo_config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

print('\nConfig saved to bamboo_config.json')
