import os, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update templates/page.faq.json and templates/page.faqs.json bottom settings
def fix_faq_templates():
    for fpath in ['d:/Lumina/templates/page.faq.json', 'd:/Lumina/templates/page.faqs.json']:
        if not os.path.exists(fpath): continue
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        m = re.match(r'^(/\*.*?\*/\s*)', content, flags=re.DOTALL)
        comment = m.group(1) if m else ''
        data = json.loads(content[len(comment):])
        
        faq_sec = data.get('sections', {}).get('lumina_faq', {}).get('settings', {})
        faq_sec['title'] = 'Frequently Asked Questions'
        faq_sec['subtitle'] = 'How can we help you today?'
        faq_sec['search_placeholder'] = 'Search by keywords or topics...'
        faq_sec['view_more_label'] = 'VIEW MORE QUESTIONS'
        faq_sec['help_title'] = 'Still need assistance?'
        faq_sec['help_desc'] = 'Our dedicated skincare concierge is here to assist you.'
        faq_sec['help_btn_label'] = 'CONTACT CONCIERGE'
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(comment + json.dumps(data, indent=2, ensure_ascii=False) + '\n')
        print(f'[FIXED] {os.path.basename(fpath)}')

# 2. Update sections/lumina-faq.liquid
def fix_lumina_faq():
    p = 'd:/Lumina/sections/lumina-faq.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Produse și Tehnologie|Mod de Utilizare|Piele, Ingrediente și Siguranță|Comenzi și Livrare|Retururi și Rambursări|Utilizare Profesională|Autenticitate|Cont și Confidențialitate|Despre Lumina Europa',
                      'Products & Technology|How to Use & Rituals|Skin, Ingredients & Safety|Orders & Shipping|Returns & Refunds|Professional & Spa Use|Authenticity & Guarantee|Account & Privacy|About Lumina Europa')
        c = c.replace('Nu au fost găsite întrebări care să corespundă căutării dumneavoastră.',
                      'No questions found matching your search.')
        c = c.replace('CĂUTAȚI', 'SEARCH')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] lumina-faq.liquid')

# 3. Update sections/return-form.liquid
def fix_return_form():
    p = 'd:/Lumina/sections/return-form.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Cerere de retur nouă', 'New Return Request')
        c = c.replace('Name și prenume', 'Full Name')
        c = c.replace('Nume și prenume', 'Full Name')
        c = c.replace('ex. Mască Nanofibers Hydrate', 'e.g. Hydrating Nanofiber Mask')
        c = c.replace('ex. Mască Nanofibre Hydrate', 'e.g. Hydrating Nanofiber Mask')
        c = c.replace('Enumerați alte produse pe care doriți să le returnați (Denumire + Cantitate)...', 'List additional items you wish to return (Product Name + Quantity)...')
        c = c.replace('Sector 1, București, Cod poștal 010325, România', 'Sector 1, Bucharest, Postal Code 010325, Romania')
        c = c.replace('FOTOGRAFII ATAȘATE', 'ATTACHED PHOTOGRAPHS')
        c = c.replace('poze încărcate cu succes', 'photos successfully uploaded')
        c = c.replace('fișiere selectate', 'files selected')
        c = c.replace('Nicio fotografie atașată', 'No photographs attached')
        c = c.replace('DETALII COMANDĂ:', 'ORDER DETAILS:')
        c = c.replace('Număr Comandă:', 'Order Number:')
        c = c.replace('Data Plasării:', 'Order Date:')
        c = c.replace('Nespecificat', 'Not specified')
        c = c.replace('Altă Situație:', 'Other Condition:')
        c = c.replace('SOLUȚIA SOLICITATĂ:', 'REQUESTED RESOLUTION:')
        c = c.replace('Soluție Solicitată:', 'Requested Resolution:')
        c = c.replace('Altă Soluție:', 'Other Resolution:')
        c = c.replace('DECLARAȚIE RETRAGERE:', 'WITHDRAWAL DECLARATION:')
        c = c.replace('Statut: Declarat și acceptat (Bifat)', 'Status: Declared and accepted (Checked)')
        c = c.replace('M-am răzgândit', 'Changed my mind')
        c = c.replace('Am comandat produsul greșit', 'Ordered wrong product')
        c = c.replace('Produsul primit nu este cel comandat', 'Received incorrect product')
        c = c.replace('Produsul a ajuns deteriorat', 'Product arrived damaged')
        c = c.replace('Produsul pare defect / neconform', 'Product appears defective / non-compliant')
        c = c.replace('Ambalajul a fost deteriorat', 'Packaging was damaged')
        c = c.replace('Produsul este sigilat / nedesigilat', 'Product is sealed / unopened')
        c = c.replace('Ambalajul exterior deschis, sigiliu igienic intact', 'Outer packaging opened, hygiene seal intact')
        c = c.replace('Sigiliul igienic a fost deschis', 'Hygiene seal has been opened')
        c = c.replace('Produsul este deteriorat / neconform', 'Product is damaged / non-compliant')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] return-form.liquid')

# 4. Update sections/lumina-gallery-full.liquid & lumina-gallery.liquid
def fix_galleries():
    for fn in ['sections/lumina-gallery-full.liquid', 'sections/lumina-gallery.liquid']:
        p = os.path.join('d:/Lumina', fn)
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        replacements = [
            ('TRIMITE FOTOGRAFIA TA', 'SUBMIT YOUR PHOTO'),
            ('Trimite fotografia ta', 'Submit your photo'),
            ('Împărtășește momentul tău', 'Share your moment'),
            ('Formularul a fost trimis', 'Form submitted successfully'),
            ('Fotografia ta a fost recepționată cu succes', 'Your photograph has been received with appreciation'),
            ('Nume complet', 'Full Name'),
            ('Adresă de e-mail', 'Email Address'),
            ('Oraș / Țară', 'City / Country'),
            ('Descrierea fotografiei', 'Photo Description'),
            ('Închide', 'Close'),
            ('Trimite', 'Submit'),
            ('Florența, Italia', 'Florence, Italy'),
            ('Paris, Franța', 'Paris, France'),
            ('Brașov, România', 'Brașov, Romania'),
            ('Veneția, Italia', 'Venice, Italy'),
            ('Sibiu, România', 'Sibiu, Romania'),
            ('München, Germania', 'Munich, Germany'),
            ('Budapesta, Ungaria', 'Budapest, Hungary'),
            ('București, România', 'Bucharest, Romania'),
            ('Milano, Italia', 'Milan, Italy'),
            ('Viena, Austria', 'Vienna, Austria'),
            ('Madrid, Spania', 'Madrid, Spain'),
            ('Barcelona, Spania', 'Barcelona, Spain'),
            ('Afișează mai multe fotografii', 'Show More Photographs'),
            ('AFIȘEAZĂ MAI MULT', 'SHOW MORE')
        ]
        for ro, en in replacements:
            c = c.replace(ro, en)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'[FIXED] {fn}')

# 5. Update sections/lumina-world-journal-grid.liquid & lumina-world-articles-grid.liquid
def fix_journal_articles():
    for fn in ['sections/lumina-world-journal-grid.liquid', 'sections/lumina-world-articles-grid.liquid']:
        p = os.path.join('d:/Lumina', fn)
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        replacements = [
            ('CITEȘTE ARTICOLUL', 'READ ARTICLE'),
            ('Citește articolul', 'Read article'),
            ('aria-label="Închide"', 'aria-label="Close"'),
            ('Îți mulțumim pentru poveste!', 'Thank you for sharing your story!'),
            ('Contribuția ta a fost recepționată cu succes. Echipa noastră editorială va analiza materialul trimis și te va contacta pe e-mail.',
             'Your contribution has been successfully received. Our editorial team will review your submission and contact you via email.'),
            ('Name și prenume', 'Full Name'),
            ('Adresă de e-mail', 'Email Address'),
            ('Scrie aici povestea ta, reflecțiile despre ritualuri sau experiența ta cu Lumina...',
             'Write your reflections, rituals, or story with Lumina here...'),
            ("filterLuminaArticles('știință', this)\">ȘTIINȚĂ", "filterLuminaArticles('science', this)\">SCIENCE"),
            ("filterLuminaArticles('cultură', this)\">CULTURĂ", "filterLuminaArticles('culture', this)\">CULTURE"),
            ("filterLuminaArticles('călătorii', this)\">CĂLĂTORII", "filterLuminaArticles('travel', this)\">TRAVEL"),
            ("filterLuminaArticles('bunăstare', this)\">BUNĂSTARE", "filterLuminaArticles('wellness', this)\">WELLNESS"),
            ('assign card_category = "ȘTIINȚĂ"', 'assign card_category = "SCIENCE"'),
            ('assign card_category = "CULTURĂ"', 'assign card_category = "CULTURE"'),
            ('assign card_category = "CĂLĂTORII"', 'assign card_category = "TRAVEL"'),
            ('assign card_category = "BUNĂSTARE"', 'assign card_category = "WELLNESS"'),
            ('ȘTIINȚĂ', 'SCIENCE'),
            ('CULTURĂ', 'CULTURE'),
            ('CĂLĂTORII', 'TRAVEL'),
            ('BUNĂSTARE', 'WELLNESS'),
            ('RITUALURI', 'RITUALS'),
            ('FILOZOFIE', 'PHILOSOPHY')
        ]
        for ro, en in replacements:
            c = c.replace(ro, en)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'[FIXED] {fn}')

# 6. Update sections/product-content.liquid
def fix_product_content():
    p = 'd:/Lumina/sections/product-content.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        replacements = [
            ('Descriere', 'Description'),
            ('Ingrediente', 'Ingredients'),
            ('Mod de utilizare', 'How to Use'),
            ('Cum se folosește', 'How to Use'),
            ('Întrebări frecvente', 'Frequently Asked Questions'),
            ('Ghid video', 'Video Guide'),
            ('Livrare și retur', 'Shipping & Returns'),
            ('Recenzii', 'Reviews'),
            ('De ce o vei iubi', 'Why You Will Love It'),
            ('Tehnologia Nanofibre', 'Nanofiber Technology'),
            ('Ingrediente Cheie', 'Key Ingredients'),
            ('Beneficii cheie', 'Key Benefits'),
            ('Rezultate clinice', 'Clinical Results')
        ]
        for ro, en in replacements:
            c = c.replace(ro, en)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] product-content.liquid')

# 7. Update sections/s_team_member_premium.liquid
def fix_team_member():
    p = 'd:/Lumina/sections/s_team_member_premium.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        replacements = [
            ('Specialiștii din spatele <span class="text-gold">Lumina Europa</span>',
             'The specialists behind <span class="text-gold">Lumina Europa</span>'),
            ('<h2 class="steam-premium__cta-title">Frumusețe susținută de <span class="text-gold">știință</span></h2>',
             '<h2 class="steam-premium__cta-title">Beauty underpinned by <span class="text-gold">science</span></h2>'),
            ('Întâlnește echipa de experți care redefinește îngrijirea pielii prin tehnologia avansată a nanofibrelor.',
             'Meet the multidisciplinary team of experts pioneering advanced nanofiber skincare biotechnology.'),
            ('Despre echipă', 'About the Team'),
            ('Echipa Noastră', 'Our Team')
        ]
        for ro, en in replacements:
            c = c.replace(ro, en)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] s_team_member_premium.liquid')

# 8. Update snippets/shipping-calc.liquid & shipping-calculator.liquid
def fix_shipping_calc():
    for fn in ['snippets/shipping-calc.liquid', 'snippets/shipping-calculator.liquid']:
        p = os.path.join('d:/Lumina', fn)
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        replacements = [
            ('<label for="address_country">Țară</label>', '<label for="address_country">Country</label>'),
            ('<label for="address_province" id="address_province_label">Județ / Regiune</label>', '<label for="address_province" id="address_province_label">Province / State</label>'),
            ('<label for="address_zip">Cod poștal</label>', '<label for="address_zip">Postal / Zip Code</label>'),
            ('Prețurile încep de la {{price}}.', 'Rates start at {{price}}.'),
            ('Nu livrăm la această destinație.', 'We do not currently ship to this destination.')
        ]
        for ro, en in replacements:
            c = c.replace(ro, en)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'[FIXED] {fn}')

# 9. Update find-your-ritual.liquid, experience-product.liquid, etc.
def fix_other_sections():
    # find-your-ritual
    p = 'd:/Lumina/sections/find-your-ritual.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Ce zonă dorești să tratezi?', 'Which area would you like to treat?')
        c = c.replace('Care este obiectivul tău principal?', 'What is your primary skincare goal?')
        c = c.replace('Ritualul tău perfect:', 'Your Perfect Ritual:')
        c = c.replace('Refaceți testul', 'Retake Quiz')
        c = c.replace('← Înapoi', '← Back')
        c = c.replace('Cumpără acum', 'Shop Now')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] find-your-ritual.liquid')

    # experience-product
    p = 'd:/Lumina/sections/experience-product.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('ADAUGĂ ÎN RITUAL', 'ADD TO RITUAL')
        c = c.replace('DĂRUIEȘTE ACEST RITUAL', 'GIFT THIS RITUAL')
        c = c.replace('Cumpără acum', 'Shop Now')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] experience-product.liquid')

    # experience-transformation
    p = 'd:/Lumina/sections/experience-transformation.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('"Transformarea în 5 minute"', '"The 5-Minute Transformation"')
        c = c.replace('"5 minute care schimbă totul. 5 minute să redescoperi Lumina ta."', '"5 minutes that transform everything. 5 minutes to rediscover your light."')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] experience-transformation.liquid')

    # mask-menu-quick-trigger
    p = 'd:/Lumina/sections/mask-menu-quick-trigger.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Deschide meniul măștilor', 'Open Mask Menu')
        c = c.replace('Selectați un meniu din setările secțiunii.', 'Please select a menu in section settings.')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] mask-menu-quick-trigger.liquid')

    # popup-compare
    p = 'd:/Lumina/snippets/popup-compare.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Selectează un produs', 'Select a product')
        c = c.replace('Alege produsul pe care dorești să îl adaugi la lista de comparare.', 'Choose a product to add to the comparison list.')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] popup-compare.liquid')

    # lumina-social-inspiration
    p = 'd:/Lumina/sections/lumina-social-inspiration.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('URMĂREȘTE LUMINA', 'FOLLOW LUMINA')
        c = c.replace('Inspirație aleasă\ndin universul nostru.', 'Curated inspiration\nfrom our universe.')
        c = c.replace('Conținut selectat cu grijă. Nu un flux automat.', 'Carefully curated content. Never an automated feed.')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] lumina-social-inspiration.liquid')

    # golden-hour-moments
    p = 'd:/Lumina/sections/golden-hour-moments.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('MOMENTE PE CARE NU LE POȚI CUMPĂRA', 'MOMENTS MONEY CANNOT BUY')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] golden-hour-moments.liquid')

    # continua-ritualul & protocoale-complete
    for fn in ['sections/continua-ritualul.liquid', 'sections/protocoale-complete.liquid']:
        p = os.path.join('d:/Lumina', fn)
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Selectează un produs pentru acest card.', 'Select a product for this card.')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'[FIXED] {fn}')

    # advanced-content, featured-collections-4, product-list-small
    for fn in ['sections/advanced-content.liquid', 'sections/product-list-small.liquid']:
        p = os.path.join('d:/Lumina', fn)
        if not os.path.exists(p): continue
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Titlu colecție', 'Collection Title')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'[FIXED] {fn}')

    p = 'd:/Lumina/sections/featured-collections-4.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('+ vezi colecția', '+ view collection')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] featured-collections-4.liquid')

    p = 'd:/Lumina/assets/theme.css.liquid'
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace("content: 'Adăugare...';", "content: 'Adding...';")
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        print('[FIXED] theme.css.liquid')

if __name__ == '__main__':
    print('Applying exact fixes to remaining files...')
    fix_faq_templates()
    fix_lumina_faq()
    fix_return_form()
    fix_galleries()
    fix_journal_articles()
    fix_product_content()
    fix_team_member()
    fix_shipping_calc()
    fix_other_sections()
    print('All exact fixes applied!')
