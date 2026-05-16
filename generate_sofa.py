from PIL import Image, ImageDraw, ImageFilter
import os

W, H = 1920, 1080

img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Цвета
C_BASE = (225, 215, 205)      # Светло-бежевый матовый
C_BASE_DARK = (205, 195, 185) # Темнее для теней
C_BASE_LIGHT = (238, 230, 220)# Блик
C_BROWN = (130, 110, 95)      # Коричневые подушки
C_PLaid = (165, 150, 135)     # Тёмно-бежевый плед
C_WOOD = (50, 38, 30)         # Ножки
C_WOOD_L = (70, 55, 45)       # Блик на дереве

def rrect(d, box, r, fill):
    d.rounded_rectangle(box, radius=r, fill=fill)

def soft_rect(d, box, fill_base, fill_shadow, blur=8):
    base = Image.new('RGBA', (W, H), (0,0,0,0))
    bd = ImageDraw.Draw(base)
    rrect(bd, box, 15, fill_base)
    base = base.filter(ImageFilter.GaussianBlur(blur))
    return base

# === ОТТОМАНКА (ЛЕВАЯ ЧАСТЬ) ===
ottoman_x, ottoman_y = 280, 550
ottoman_w, ottoman_h = 520, 280

# Основа оттоманки
rrect(draw, [ottoman_x, ottoman_y, ottoman_x+ottoman_w, ottoman_y+ottoman_h], 22, C_BASE)

# Тень на оттоманке
soft = Image.new('RGBA', (W, H), (0,0,0,0))
sd = ImageDraw.Draw(soft)
sd.rounded_rectangle([ottoman_x+10, ottoman_y+ottoman_h-45, ottoman_x+ottoman_w-10, ottoman_y+ottoman_h-15], radius=12, fill=(0,0,0,50))
img = Image.alpha_composite(img, soft.filter(ImageFilter.GaussianBlur(10)))
draw = ImageDraw.Draw(img)

# === ОСНОВНАЯ ЧАСТЬ ДИВАНА (ПРАВАЯ) ===
main_x, main_y = 780, 530
main_w, main_h = 1050, 320

# Основа
rrect(draw, [main_x, main_y, main_x+main_w, main_y+main_h], 22, C_BASE)

# Разделитель между оттоманкой и основой
draw.line([(780, ottoman_y+15), (780, ottoman_y+ottoman_h-15)], fill=C_BASE_DARK, width=3)

# === БОКОВЫЕ ПОДЛОКОТНИКИ ===
# Левый подлокотник (оттоманки)
arm1_w, arm1_h = 85, 165
rrect(draw, [220, ottoman_y+65, 220+arm1_w, ottoman_y+65+arm1_h], 20, C_BASE)
rrect(draw, [228, ottoman_y+105, 220+arm1_w-8, ottoman_y+65+arm1_h-8], 15, C_BASE_DARK)
rrect(draw, [230, ottoman_y+75, 242, ottoman_y+130], 6, C_BASE_LIGHT)

# Правый подлокотник
arm2_w, arm2_h = 85, 165
rrect(draw, [main_x+main_w-85, main_y+60, main_x+main_w, main_y+60+arm2_h], 20, C_BASE)
rrect(draw, [main_x+main_w-77, main_y+100, main_x+main_w-8, main_y+60+arm2_h-8], 15, C_BASE_DARK)
rrect(draw, [main_x+main_w-42, main_y+70, main_x+main_w-30, main_y+125], 6, C_BASE_LIGHT)

# === СПИНКА ДИВАНА ===
back_y = 400
back_h = 160

# Основная спинка
rrect(draw, [main_x+30, back_y, main_x+main_w-30, back_y+back_h], 22, C_BASE)

# === СЕДЕНЬЕ ===
seat_y = 560
seat_h = 55
rrect(draw, [main_x+50, seat_y, main_x+main_w-50, seat_y+seat_h], 18, C_BASE)

# === НОЖКИ ===
leg_w, leg_h = 20, 45
for x in [320, 680, main_x+120, main_x+main_w-140]:
    rrect(draw, [x, seat_y+seat_h, x+leg_w, seat_y+seat_h+leg_h], 4, C_WOOD)
    draw.rectangle([x+2, seat_y+seat_h+5, x+6, seat_y+seat_h+leg_h-5], fill=C_WOOD_L)

# === ПОДУШКИ СЕДЕНЬЯ (4 бежевых) ===
cushion_w = (main_w - 120) // 4
for i in range(4):
    x = main_x + 80 + i * (cushion_w + 12)
    # Основная подушка
    rrect(draw, [x, seat_y-12, x+cushion_w, seat_y+38], 20, C_BASE_LIGHT)
    # Тень
    rrect(draw, [x+6, seat_y+20, x+cushion_w-6, seat_y+38], 15, C_BASE_DARK)
    # Мягкие складки
    for j in range(2):
        offset = 25 + j*8
        draw.arc([x+12+j*15, seat_y-8, x+28+j*15, seat_y+20], start=210, end=330, fill=C_BASE_DARK, width=2)

# === ПОДУШКИ СПИНКИ (4 бежевых) ===
for i in range(4):
    x = main_x + 80 + i * (cushion_w + 12)
    rrect(draw, [x, back_y+12, x+cushion_w, back_y+back_h-15], 24, C_BASE_LIGHT)
    rrect(draw, [x+6, back_y+85, x+cushion_w-6, back_y+back_h-20], 18, C_BASE_DARK)

# === КОРИЧНЕВЫЕ ПОДУШКИ (2 штуки) ===
# Коричневая подушка 1 (на оттоманке)
pillow1_x, pillow1_y = 380, 520
rrect(draw, [pillow1_x, pillow1_y, pillow1_x+110, pillow1_y+90], 18, C_BROWN)
rrect(draw, [pillow1_x+8, pillow1_y+8, pillow1_x+102, pillow1_y+82], 14, (145, 125, 110))

# Коричневая подушка 2 (справа)
pillow2_x, pillow2_y = main_x+main_w-280, 540
rrect(draw, [pillow2_x, pillow2_y, pillow2_x+130, pillow2_y+100], 18, C_BROWN)
rrect(draw, [pillow2_x+10, pillow2_y+10, pillow2_x+120, pillow2_y+90], 14, (145, 125, 110))

# === ПЛЕД НА ОТТОМАНКЕ ===
# Основное полотно
px, py = 300, 580
draw.polygon([
    (px, py),
    (px+320, py+15),
    (px+340, py+180),
    (px+20, py+165)
], fill=C_PLaid)

# Складки пледа
for i in range(3):
    x = px + 40 + i*80
    y = py + 30 + i*25
    draw.line([(x, y), (x+30, y+40)], fill=(180, 165, 150), width=4)

# Тень от пледа
soft = Image.new('RGBA', (W, H), (0,0,0,0))
sd = ImageDraw.Draw(soft)
sd.polygon([
    (px+10, py+10),
    (px+310, py+25),
    (px+330, py+170),
    (px+30, py+155)
], fill=(0,0,0,35))
img = Image.alpha_composite(img, soft.filter(ImageFilter.GaussianBlur(8)))
draw = ImageDraw.Draw(img)

# === ОБЩИЕ ТЕНИ ===
# Тень под диваном
shadow = Image.new('RGBA', (W, H), (0,0,0,0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle([200, 820, main_x+main_w-50, 870], radius=40, fill=(0,0,0,90))
img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(25)))

# Сохранение
out = 'doublerings/interior-visualizer/images/sofa-l-shape.png'
img.save(out, 'PNG', optimize=True)
size = os.path.getsize(out)
print('Saved:', out)
print('Size:', W, 'x', H, 'px')
print('File size:', round(size/1024, 1), 'KB')
print('Resolution: 4K equivalent')
