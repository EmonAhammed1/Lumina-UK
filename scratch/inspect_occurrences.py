import os, re

files = [
  'sections/continua-ritualul.liquid',
  'sections/experience-alchemy.liquid',
  'sections/experience-features.liquid',
  'sections/experience-product.liquid',
  'sections/experience-under-microscope.liquid',
  'sections/find-your-ritual.liquid',
  'sections/footer-group.json',
  'sections/footer-lumina.liquid',
  'sections/golden-hour-benefits.liquid',
  'sections/golden-hour-moments.liquid',
  'sections/lumina-faq.liquid',
  'sections/lumina-gallery-full.liquid',
  'sections/lumina-gallery.liquid',
  'sections/lumina-world-articles-grid.liquid',
  'sections/lumina-world-journal-grid.liquid',
  'sections/product-content.liquid',
  'sections/product-recommendations.liquid',
  'sections/return-form.liquid',
  'sections/s_team_member_premium.liquid',
  'sections/tech-mockup-ingredients.liquid',
  'snippets/megamenu-product.liquid'
]

keywords = ['ritualul', 'ingrediente', 'tehnologie', 'livrare', 'pentru', 'despre', 'produse', 'descopera', 'stiinta', 'utilizare', 'retur', 'noastre', 'produsul']

for p in files:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            lines = fl.readlines()
            matches = []
            for idx, line in enumerate(lines):
                for kw in keywords:
                    if kw in line.lower():
                        matches.append((idx+1, line.strip()))
                        break
            if matches:
                print(f'=== {p} ===')
                for lno, l in matches:
                    print(f'  L{lno}: {l[:110]}')
