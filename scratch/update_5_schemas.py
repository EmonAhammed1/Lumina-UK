import os

# 1. sections/experience-benefits.liquid
p = 'd:/Lumina/sections/experience-benefits.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"title": "INGREDIENTE ACTIVE"', '"title": "ACTIVE INGREDIENTS"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

# 2. sections/footer-lumina.liquid
p = 'd:/Lumina/sections/footer-lumina.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"default": "Ingrediente Active"', '"default": "Active Ingredients"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

# 3. sections/lumina-faq.liquid
p = 'd:/Lumina/sections/lumina-faq.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"value": "Mod de Utilizare"', '"value": "How to Use & Rituals"')
c = c.replace('"label": "Mod de Utilizare"', '"label": "How to Use & Rituals"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

# 4. sections/product-content.liquid
p = 'd:/Lumina/sections/product-content.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"default": "Perfect pentru toate tipurile de ten, inclusiv cel sensibil"',
              '"default": "Perfect for all skin types, including sensitive skin"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

# 5. sections/return-form.liquid
p = 'd:/Lumina/sections/return-form.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"default": "FORMULAR DE RETUR / RETRAGERE"',
              '"default": "RETURN & WITHDRAWAL FORM"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated 5 files!')
