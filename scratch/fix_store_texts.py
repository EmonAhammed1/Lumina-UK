import json, re, os, glob

def fix_all():
    # 1. page.about-us-v1.json
    p1 = 'templates/page.about-us-v1.json'
    if os.path.exists(p1):
        with open(p1, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"title": "Trimite-ne un e-mail"', '"title": "Send us an email"')
        with open(p1, 'w', encoding='utf-8') as f:
            f.write(c)

    # 2. page.about-us-v3.json
    p2 = 'templates/page.about-us-v3.json'
    if os.path.exists(p2):
        with open(p2, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"title": "Trimite-ne un e-mail"', '"title": "Send us an email"')
        with open(p2, 'w', encoding='utf-8') as f:
            f.write(c)

    # 3. page.golden-hour.json
    p3 = 'templates/page.golden-hour.json'
    if os.path.exists(p3):
        with open(p3, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"title": "Acces prioritar"', '"title": "Priority Access"')
        c = c.replace('"title": "Cadouri exclusive"', '"title": "Exclusive Gifts"')
        c = c.replace('"title": "Oferte dedicate"', '"title": "Curated Offers"')
        c = c.replace('"title": "Evenimente"', '"title": "Exclusive Events"')
        c = c.replace('"heading": "Fiecare ritual spune o poveste"', '"heading": "Every ritual tells a story"')
        with open(p3, 'w', encoding='utf-8') as f:
            f.write(c)

    # 4. page.lumina-world.json
    p4 = 'templates/page.lumina-world.json'
    if os.path.exists(p4):
        with open(p4, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"section_title": "JURNAL"', '"section_title": "JOURNAL"')
        c = c.replace('"modal_eyebrow": "FII PARTE DIN JURNAL"', '"modal_eyebrow": "BE PART OF THE JOURNAL"')
        c = c.replace('"modal_title": "Trimite Povestea Ta"', '"modal_title": "Submit Your Story"')
        c = c.replace('Jurnalul Lumina', 'Lumina Journal')
        c = c.replace('"eyebrow": "PROIECT EDITORIAL SPECIAL"', '"eyebrow": "SPECIAL EDITORIAL PROJECT"')
        c = c.replace('"title": "SURPRINDE"', '"title": "CAPTURE"')
        c = c.replace('"title": "SPUNE-NE UNDE"', '"title": "TELL US WHERE"')
        c = c.replace('"title": "TRIMITE"', '"title": "SUBMIT"')
        c = c.replace('"share_subheading": "FII PARTE DIN POVESTE"', '"share_subheading": "BE PART OF THE STORY"')
        with open(p4, 'w', encoding='utf-8') as f:
            f.write(c)

    # 5. All product templates
    for p in glob.glob('templates/product.*.json'):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"title": "Transport Gratuit"', '"title": "Complimentary Shipping"')
        c = c.replace('"text_circle": "Magazin de stil Fashion2"', '"text_circle": "Lumina Europa Luxury Care"')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)

    # 6. config/settings_data.json
    ps = 'config/settings_data.json'
    if os.path.exists(ps):
        with open(ps, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"label_text2": "Nou"', '"label_text2": "New"')
        c = c.replace('"title": "Transport Gratuit"', '"title": "Complimentary Shipping"')
        c = c.replace('"title": "Suport de calitate"', '"title": "Quality Support"')
        c = c.replace('"description": "Suport online 24/7"', '"description": "Online Support 24/7"')
        c = c.replace('"title": "Voucher Cadou"', '"title": "Gift Voucher"')
        with open(ps, 'w', encoding='utf-8') as f:
            f.write(c)

    # 7. snippets/block-cart.liquid
    p_cart = 'snippets/block-cart.liquid'
    if os.path.exists(p_cart):
        with open(p_cart, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('<span class="cart-title">COS</span>', '<span class="cart-title">CART</span>')
        with open(p_cart, 'w', encoding='utf-8') as f:
            f.write(c)

    # 8. sections/golden-hour-community.liquid
    p_ghc = 'sections/golden-hour-community.liquid'
    if os.path.exists(p_ghc):
        with open(p_ghc, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('<div class="gh-comm-heading-small">COMUNITATEA LUMINA</div>', '<div class="gh-comm-heading-small">LUMINA COMMUNITY</div>')
        c = c.replace('"default": "Fiecare ritual spune o poveste."', '"default": "Every ritual tells a story."')
        c = c.replace('"label": "Content (Romanian)"', '"label": "Content"')
        with open(p_ghc, 'w', encoding='utf-8') as f:
            f.write(c)

    # 9. sections/lumina-gallery.liquid
    p_lg = 'sections/lumina-gallery.liquid'
    if os.path.exists(p_lg):
        with open(p_lg, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"default": "FII PARTE DIN POVESTE"', '"default": "BE PART OF THE STORY"')
        with open(p_lg, 'w', encoding='utf-8') as f:
            f.write(c)

    # 10. sections/lumina-world-journal-grid.liquid
    p_lwj = 'sections/lumina-world-journal-grid.liquid'
    if os.path.exists(p_lwj):
        with open(p_lwj, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"default": "JURNAL"', '"default": "JOURNAL"')
        c = c.replace('value="Trimitere Articol / Poveste Jurnal - Lumina World"', 'value="Article Submission / Journal Story - Lumina World"')
        c = c.replace('name="contact[Titlu Jurnal]"', 'name="contact[Journal Title]"')
        with open(p_lwj, 'w', encoding='utf-8') as f:
            f.write(c)

    # 11. sections/return-form.liquid
    p_rf = 'sections/return-form.liquid'
    if os.path.exists(p_rf):
        with open(p_rf, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Back la magazin', 'Back to Shop')
        with open(p_rf, 'w', encoding='utf-8') as f:
            f.write(c)

    print('All files successfully updated!')

if __name__ == '__main__':
    fix_all()
