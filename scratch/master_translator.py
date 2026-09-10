import os, json, re, time, sys, glob
from deep_translator import GoogleTranslator

sys.stdout.reconfigure(encoding='utf-8')
translator = GoogleTranslator(source='ro', target='en')

# Cache translations to avoid redundant network calls and ensure consistency
TRANSLATION_CACHE = {
    # Brand Terms
    "Știință. Ritual. Lumină.": "Science. Ritual. Light.",
    "Ştiinţă. Ritual. Lumină.": "Science. Ritual. Light.",
    "UNDE ȘTIINȚA DEVINE RITUAL": "WHERE SCIENCE BECOMES RITUAL",
    "Unde știința devine ritual": "Where science becomes ritual",
    "Unde Știința Devine Ritual": "Where Science Becomes Ritual",
    "UNDE ȘTIINȚA\nDEVINE\nRITUAL": "WHERE SCIENCE\nBECOMES\nRITUAL",
    "UNDE ȘTIINȚA <br>DEVINE RITUAL": "WHERE SCIENCE <br>BECOMES RITUAL",
    "PĂSTREAZĂ LUMINA APROAPE DE TINE": "KEEP THE LIGHT CLOSE TO YOU",
    "Păstrează lumina aproape de tine": "Keep the light close to you",
    "DESCOPERĂ LUMINA": "DISCOVER LUMINA",
    "DESCOPERĂ LUMINA EUROPA": "DISCOVER LUMINA EUROPA",
    "Descoperă Lumina Europa": "Discover Lumina Europa",
    "Descoperă acum": "Discover Now",
    "DESCOPERĂ ACUM": "DISCOVER NOW",
    "Descoperă": "Discover",
    "DESCOPERĂ": "DISCOVER",
    "Cumpără acum": "Shop Now",
    "cumpără acum": "shop now",
    "CUMPĂRĂ ACUM": "SHOP NOW",
    "Cumpără Cadouri după Preț": "Shop Gifts by Price",
    "Cele Mai Vândute": "Bestsellers",
    "Cele mai vândute": "Bestsellers",
    "Vezi toate": "View All",
    "VEZI TOATE": "VIEW ALL",
    "Vezi Toate": "View All",
    "Vezi colecția": "View Collection",
    "Vezi Colecția": "View Collection",
    "EXPLOREAZĂ COLECȚIA": "EXPLORE THE COLLECTION",
    "Explorează Colecția": "Explore the Collection",
    "EXPLOREAZĂ TEHNOLOGIA": "EXPLORE THE TECHNOLOGY",
    "EXPLOREAZĂ TEHNOLOGIA →": "EXPLORE THE TECHNOLOGY →",
    "AFLĂ MAI MULTE": "LEARN MORE",
    "Află mai multe": "Learn more",
    "Află Mai Multe": "Learn More",
    "DESCOPERĂ MAI MULT": "DISCOVER MORE",
    "Descoperă mai mult": "Discover more",
    "VEZI GHIDUL VIDEO": "WATCH VIDEO GUIDE",
    "VEZI TOATE INGREDIENTELE": "VIEW ALL INGREDIENTS",
    "EXPLOREAZĂ CERCETAREA": "EXPLORE RESEARCH",
    "DESCOPERĂ PACHETELE DE RITUAL": "DISCOVER RITUAL BUNDLES",
    "DESCOPERĂ COLECȚIA LUMINA": "DISCOVER THE LUMINA COLLECTION",
    "INTRĂ ÎN LUMINA WORLD →": "ENTER LUMINA WORLD →",
    "DESCOPERĂ LUMINA WORLD": "DISCOVER LUMINA WORLD",
    "VIZIONEAZĂ FILMUL DE PREZENTARE": "WATCH THE BRAND FILM",
    "EXPLOREAZĂ MANIFESTUL": "EXPLORE THE MANIFESTO",
    "URMĂREȘTE CONVERSAȚIA": "WATCH CONVERSATION",
    "CITEȘTE TRANSCRIPTUL": "READ TRANSCRIPT",
    "TOATE CONVERSAȚIILE": "ALL CONVERSATIONS",
    "ULTIMELE CONVERSAȚII": "LATEST CONVERSATIONS",
    "EXPLOREAZĂ JURNALUL": "EXPLORE THE JOURNAL",
    "TRIMITE JURNALUL TĂU": "SUBMIT YOUR STORY",
    "TOATE ARTICOLELE": "ALL ARTICLES",
    "VEZI GALERIA ->": "VIEW GALLERY ->",
    "VEZI TOATĂ GALERIA": "VIEW FULL GALLERY",
    "TRIMITE FOTOGRAFIA TA": "SUBMIT YOUR PHOTO",
    "TRIMITE FOTOGRAFIA TA ->": "SUBMIT YOUR PHOTO ->",
    "VEZI TOATE PLATFORMELE ->": "VIEW ALL CHANNELS ->",
    "Devino membru LUMINA GOLDEN HOUR": "Become a LUMINA GOLDEN HOUR Member",
    "DESCOPERĂ GOLDEN REWARDS": "DISCOVER GOLDEN REWARDS",
    "ÎNSCRIE-TE ÎN COMUNITATE": "JOIN THE COMMUNITY",
    "DESCOPERĂ LUMINA GOLDEN HOUR →": "DISCOVER LUMINA GOLDEN HOUR →",
    "CONTACTEAZĂ-NE →": "CONTACT US →",
    "CONTACTEAZĂ-NE": "CONTACT US",
    "Contactează-ne": "Contact Us",
    "Găsește Ritualul Perfect": "Find Your Perfect Ritual",
    "GĂSEȘTE RITUALUL TĂU": "FIND YOUR RITUAL",
    "Găsește ritualul": "Find your ritual",
    "Înapoi": "Back",
    "Înainte": "Next",
    "Finalizează": "Complete",
    "Restart": "Restart",
    "Pasul": "Step",
    "Ten (Față)": "Face",
    "Față": "Face",
    "Gât": "Neck",
    "Decolteu": "Décolleté",
    "Zona ochilor": "Eye Area",
    "Ochi": "Eyes",
    "Toate zonele": "All Zones",
    "Electrofilare": "Electrospinning",
    "Nanofibre": "Nanofibers",
    "Acid Hialuronic": "Hyaluronic Acid",
    "Colagen": "Collagen",
    "Vitamina C": "Vitamin C",
    "Niacinamidă": "Niacinamide",
    "Acasa": "Home",
    "Acasă": "Home",
    "Despre Noi": "About Us",
    "Despre noi": "About Us",
    "DESPRE NOI": "ABOUT US",
    "Termeni și Condiții": "Terms and Conditions",
    "Politica de Confidențialitate": "Privacy Policy",
    "Politica de Retur": "Return Policy",
    "Politica de Livrare": "Shipping Policy",
    "Întrebări Frecvente": "Frequently Asked Questions",
    "Formular de Retur": "Return Form",
    "Trimite formularul": "Submit form",
    "Trimite mesajul": "Send message",
    "Nume": "Name",
    "Prenume": "First Name",
    "Nume de familie": "Last Name",
    "Email": "Email",
    "Telefon": "Phone",
    "Număr comandă": "Order Number",
    "Motivul returului": "Reason for Return",
    "Mesaj": "Message",
    "Descriere": "Description"
}

RO_PATTERN = re.compile(r'[ăâîșțĂÂÎȘȚşţŞŢ]')

def is_romanian(text):
    if not isinstance(text, str) or not text.strip():
        return False
    # If text is file path, URL, CSS, variable name, don't translate
    if re.match(r'^(https?://|/[a-zA-Z0-9_\-/]+\.(mp4|png|jpg|jpeg|svg|gif|css|js)|shopify://|\d+(\.\d+)?$)', text.strip()):
        return False
    if text.startswith('shopify-section') or text.startswith('template--') or text.startswith('icon-'):
        return False
    if RO_PATTERN.search(text):
        return True
    # Check common Romanian words
    lower = text.lower()
    common_ro = ['despre', 'pentru', 'nostru', 'noastra', 'cumpara', 'adaugă', 'adauga', 'cosul', 'coșul', 'acasa', 'contacteaza', 'filtreaza', 'inchide', 'inapoi', 'toate', 'produse', 'tehnologie', 'comanda', 'livrare', 'retur', 'intrebari', 'frecvente']
    words = set(re.findall(r'\b[a-zA-ZăâîșțĂÂÎȘȚşţŞŢ]+\b', lower))
    if any(w in words for w in common_ro):
        return True
    return False

def translate_string(s):
    if not isinstance(s, str) or not s.strip():
        return s
    
    clean_s = s.strip()
    if clean_s in TRANSLATION_CACHE:
        return s.replace(clean_s, TRANSLATION_CACHE[clean_s])
    
    if not is_romanian(s):
        return s
        
    # Preserve HTML tags
    html_tags = re.findall(r'<[^>]+>', s)
    temp_s = s
    for i, tag in enumerate(html_tags):
        temp_s = temp_s.replace(tag, f' ___TAG_{i}___ ', 1)
        
    # Preserve Liquid tags
    liquid_tags = re.findall(r'(\{\{.*?\}\}|\{%.*?%\})', temp_s)
    for i, ltag in enumerate(liquid_tags):
        temp_s = temp_s.replace(ltag, f' ___LIQ_{i}___ ', 1)
        
    try:
        translated = translator.translate(temp_s)
        
        # Restore Liquid tags
        for i, ltag in enumerate(liquid_tags):
            translated = re.sub(rf'___\s*LIQ_{i}\s*___', ltag, translated, flags=re.IGNORECASE)
            translated = translated.replace(f'___LIQ_{i}___', ltag)
            
        # Restore HTML tags
        for i, tag in enumerate(html_tags):
            translated = re.sub(rf'___\s*TAG_{i}\s*___', tag, translated, flags=re.IGNORECASE)
            translated = translated.replace(f'___TAG_{i}___', tag)
            
        TRANSLATION_CACHE[clean_s] = translated.strip()
        time.sleep(0.05) # Polite rate limiting
        return translated
    except Exception as e:
        print(f'Translation error on: {s[:30]}... ({e})')
        return s

def translate_data_structure(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            # Don't translate schema IDs, types, assets, video filenames
            if k in ['type', 'id', 'video_url', 'video_link', 'video_bg', 'image', 'icon', 'color', 'background', 'bg_color']:
                new_dict[k] = v
            elif isinstance(v, str) and (v.endswith(('.mp4', '.png', '.jpg', '.svg', '.jpeg')) or 'shopify://' in v or v.startswith('http')):
                new_dict[k] = v
            else:
                new_dict[k] = translate_data_structure(v)
        return new_dict
    elif isinstance(data, list):
        return [translate_data_structure(item) for item in data]
    elif isinstance(data, str):
        return translate_string(data)
    else:
        return data

def translate_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        m = re.match(r'^(/\*.*?\*/\s*)', content, flags=re.DOTALL)
        comment = m.group(1) if m else ''
        json_content = content[len(comment):]
        
        data = json.loads(json_content)
        translated_data = translate_data_structure(data)
        
        new_json = json.dumps(translated_data, indent=2, ensure_ascii=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(comment + new_json + '\n')
        print(f'[JSON OK] {os.path.relpath(file_path, "d:/Lumina")}')
    except Exception as e:
        print(f'[JSON ERR] {file_path}: {e}')

if __name__ == '__main__':
    print('Starting translation of JSON templates and settings...')
    json_files = glob.glob('d:/Lumina/templates/**/*.json', recursive=True) + glob.glob('d:/Lumina/templates/*.json', recursive=True)
    json_files.append('d:/Lumina/config/settings_data.json')
    json_files.append('d:/Lumina/sections/footer-group.json')
    
    unique_files = sorted(list(set(json_files)))
    for p in unique_files:
        # Skip faq files if already handled
        if 'page.faq.json' in p or 'page.faqs.json' in p:
            continue
        translate_json_file(p)
    print('All JSON files translated!')
