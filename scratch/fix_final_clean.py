import os, re, json, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. sections/product-content.liquid
p = 'd:/Lumina/sections/product-content.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r"\{\%- assign default_txt = '<p>Curățați delicat tenul.*?' -\%\}",
           r"{%- assign default_txt = '<p>Gently cleanse your face before application. Ensure skin is clean and lightly misted with Hydro Mist or lukewarm water.</p>' -%}",
           c)
c = re.sub(r"\{\%- assign default_txt = '<p>1\. Desfaceți masca uscată.*?' -\%\}",
           r"{%- assign default_txt = '<p>1. Open the dry mask and smooth onto misted skin.<br/>2. Allow the nanofibers to dissolve and release pure encapsulated actives.<br/>3. Gently press the remaining essence into the skin.</p>' -%}",
           c)
c = re.sub(r"\{\%- assign default_txt = '<p><strong>Hyaluronic Acid:</strong> Hidratare profundă.*?' -\%\}",
           r"{%- assign default_txt = '<p><strong>Hyaluronic Acid:</strong> Multi-depth cellular hydration.<br/><strong>Niacinamide (Vitamin B3):</strong> Evens skin tone and strengthens lipid barrier.<br/><strong>Panthenol:</strong> Calms and accelerates cellular recovery.</p>' -%}",
           c)
c = re.sub(r"\{\%- assign default_txt = '<p>✦ <strong>98%</strong> dintre participante.*?' -\%\}",
           r"{%- assign default_txt = '<p>✦ <strong>98%</strong> of participants noted immediate hydration after first application.<br/>✦ <strong>94%</strong> reported refined texture and enhanced elasticity after 14 days.<br/>✦ <strong>91%</strong> saw visibly luminous, rejuvenated skin.</p>' -%}",
           c)

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] product-content.liquid')

# 2. sections/lumina-gallery-full.liquid & lumina-gallery.liquid
for fn in ['sections/lumina-gallery-full.liquid', 'sections/lumina-gallery.liquid']:
    p = os.path.join('d:/Lumina', fn)
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('Se încarcă mai multe fotografii...', 'Loading more photographs...')
    c = c.replace('Nu există fotografii adăugate momentan în această galerie.', 'No photographs added yet to this gallery.')
    c = c.replace('Îți mulțumim pentru fotografie!', 'Thank you for your photograph!')
    c = c.replace('Fotografia ta a fost transmisă cu succes echipei noastre. O vom analiza și o vom include în galeria Lumina dacă se potrivește esteticii comunității.',
                  'Your photograph has been successfully submitted to our team. We will review it for inclusion in the Lumina Europa gallery.')
    c = c.replace('Împărtășește momentele tale din Europa. Lumina pe care o vezi, locurile pe care le explorezi.',
                  'Share your moments across Europe. The light you experience, the places you explore.')
    c = c.replace('Name și prenume', 'Full Name')
    c = c.replace('Nume și prenume', 'Full Name')
    c = c.replace('name="contact[Name și First Name]"', 'name="contact[name]"')
    c = c.replace('name="contact[Nume și Prenume]"', 'name="contact[name]"')
    c = c.replace('Încarcă gratuit imaginea ta pe ImgBB pentru a obține linkul direct:', 'Upload your image for free to obtain a direct link:')
    c = c.replace('Fă clic pe butonul <strong>„Deschide ImgBB.com”</strong> de mai sus (se deschide în filă nouă).', 'Click the <strong>"Open ImgBB.com"</strong> button above (opens in new tab).')
    c = c.replace('Apasă <strong>„Start Uploading”</strong>, alege fotografia și setează <strong>„Don\'t autodelete”</strong>.', 'Click <strong>"Start Uploading"</strong>, choose your photo and select <strong>"Don\'t autodelete"</strong>.')
    c = c.replace('Apasă <strong>„Upload”</strong> și copiază linkul imaginii (Direct Link sau Viewer Link).', 'Click <strong>"Upload"</strong> and copy the image link (Direct Link or Viewer Link).')
    c = c.replace('Lipește linkul copiat în câmpul de mai jos 👇', 'Paste the copied image link into the field below 👇')
    c = c.replace('Oraș, țară sau o scurtă poveste despre imagine', 'City, country or a short reflection on this moment')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'[FIXED] {fn}')

# 3. sections/lumina-world-journal-grid.liquid
p = 'd:/Lumina/sections/lumina-world-journal-grid.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Contribuția ta a fost recepționată cu succes. Echipa noastră editorială va analiza materialul trimis și te va contacta pe e-mail sau pe profilul social indicat.',
              'Your submission has been received. Our editorial team will review your story and reach out via email.')
c = c.replace('name="contact[Name și First Name]"', 'name="contact[name]"')
c = c.replace('Scrie aici povestea ta, reflecțiile sau articolul propus...', 'Write your story, reflections, or article proposal here...')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] lumina-world-journal-grid.liquid')

# 4. snippets/processMenuTitle.liquid & snippets/menu-mobile.liquid
p = 'd:/Lumina/snippets/processMenuTitle.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('tehnologie și formulă', 'tehnologie si formula')
c = c.replace('bază științifică și premii', 'baza stiintifica si premii')
c = c.replace('conversații', 'conversatii')
c = c.replace('urmărește lumina', 'urmareste lumina')
c = c.replace('echipa noastră', 'echipa noastra')
c = c.replace('contactează-ne', 'contacteaza-ne')
c = c.replace('întrebări frecvente', 'intrebari frecvente')
c = c.replace('termeni și condiții', 'termeni si conditii')
c = c.replace('politica de confidențialitate', 'politica de confidentialitate')
c = c.replace('acasă', 'acasa')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] processMenuTitle.liquid')

p = 'd:/Lumina/snippets/menu-mobile.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace("or link_title_dn == 'colecție'", "")
c = c.replace("'conversații'", "'conversatii'")
c = c.replace("'urmărește lumina'", "'urmareste lumina'")
c = c.replace("'tehnologie și formulă'", "'tehnologie si formula'")
c = c.replace("'bază științifică și premii'", "'baza stiintifica si premii'")
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] menu-mobile.liquid')

# 5. sections/lumina-faq.liquid
p = 'd:/Lumina/sections/lumina-faq.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Produse și Tehnologie|Mod de Utilizare|Piele, Ingrediente și Siguranță|Comenzi și Livrare|Retururi și Rambursări|Despre Lumina Europa',
              'Products & Technology|How to Use & Rituals|Skin, Ingredients & Safety|Orders & Shipping|Returns & Refunds|About Lumina Europa')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] lumina-faq.liquid')

# 6. sections/return-form.liquid
p = 'd:/Lumina/sections/return-form.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('placeholder="Enumerați alte produse pe care doriți să le returnați (Denumire + Quantity)..."',
              'placeholder="List additional items you wish to return (Product Name + Quantity)..."')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] return-form.liquid')

# 7. sections/lumina-social-inspiration.liquid
p = 'd:/Lumina/sections/lumina-social-inspiration.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"default": "Inspirație aleasă\\ndin universul nostru."', '"default": "Curated inspiration\\nfrom our universe."')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] lumina-social-inspiration.liquid')

# 8. sections/continua-ritualul.liquid & sections/product-recommendations.liquid
p = 'd:/Lumina/sections/continua-ritualul.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('"Continuă ritualul"', '"Continue the Ritual"')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] continua-ritualul.liquid')

p = 'd:/Lumina/sections/product-recommendations.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Continuă ritualul', 'Continue the Ritual')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] product-recommendations.liquid')

# 9. sections/lumina-world-conversations-slider.liquid
p = 'd:/Lumina/sections/lumina-world-conversations-slider.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Andrei Margăritescu', 'Andrei Margaritescu')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('[FIXED] lumina-world-conversations-slider.liquid')
