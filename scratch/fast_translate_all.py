import os, json, re, time, sys, glob
import urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

# Luxury brand vocabulary & specific client translations
BRAND_TERMS = {
    # Core tagline & brand headers
    "Știință. Ritual. Lumină.": "Science. Ritual. Light.",
    "Ştiinţă. Ritual. Lumină.": "Science. Ritual. Light.",
    "UNDE ȘTIINȚA DEVINE RITUAL": "WHERE SCIENCE BECOMES RITUAL",
    "Unde știința devine ritual": "Where science becomes ritual",
    "Unde Știința Devine Ritual": "Where Science Becomes Ritual",
    "UNDE ȘTIINȚA\nDEVINE\nRITUAL": "WHERE SCIENCE\nBECOMES\nRITUAL",
    "PĂSTREAZĂ LUMINA APROAPE DE TINE": "KEEP THE LIGHT CLOSE TO YOU",
    "Păstrează lumina aproape de tine": "Keep the light close to you",
    
    # CTAs
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

    # Quiz & Steps
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
    "Format uscat": "Preservative-free dry matrix",

    # FAQ Categories
    "Produse și Tehnologie": "Products & Technology",
    "Produse si Tehnologie": "Products & Technology",
    "Piele, Ingrediente și Siguranță": "Skin, Ingredients & Safety",
    "Piele, Ingrediente si Siguranta": "Skin, Ingredients & Safety",
    "Mod de Utilizare": "How to Use & Rituals",
    "Comenzi și Livrare": "Orders & Shipping",
    "Comenzi si Livrare": "Orders & Shipping",
    "Retururi și Rambursări": "Returns & Refunds",
    "Retururi si Rambursari": "Returns & Refunds",
    "Utilizare Profesională": "Professional & Spa Use",
    "Utilizare Profesionala": "Professional & Spa Use",
    "Autenticitate": "Authenticity & Guarantee",
    "Cont și Confidențialitate": "Account & Privacy",
    "Cont si Confidentialitate": "Account & Privacy",
    "Despre Lumina Europa": "About Lumina Europa",
    "Toate": "All",
    "TOATE": "ALL",
    
    # Common Menu & Navigation
    "Acasă": "Home",
    "Acasa": "Home",
    "Produse": "Products",
    "Colecții": "Collections",
    "Colecție": "Collection",
    "Tehnologie": "Technology",
    "Despre Noi": "About Us",
    "Despre noi": "About Us",
    "DESPRE NOI": "ABOUT US",
    "Termeni și Condiții": "Terms and Conditions",
    "Politica de Confidențialitate": "Privacy Policy",
    "Politica de Retur": "Return Policy",
    "Politica de Livrare": "Shipping Policy",
    "Întrebări Frecvente": "Frequently Asked Questions",
    "Formular de Retur": "Return Form",
    "Toate drepturile rezervate.": "All rights reserved.",
    "&copy; 2026 Lumina Europa.<br>Toate drepturile rezervate.": "&copy; 2026 Lumina Europa.<br>All rights reserved."
}

CACHE = dict(BRAND_TERMS)
RO_PATTERN = re.compile(r'[ăâîșțĂÂÎȘȚşţŞŢ]')

def gtrans_direct(text):
    if not text or not text.strip():
        return text
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=ro&tl=en&dt=t&q=' + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    for attempt in range(4):
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode('utf-8'))
            return ''.join([item[0] for item in data[0] if item and item[0]])
        except Exception as e:
            time.sleep(0.3 * (attempt + 1))
    return text

def is_text_romanian(text):
    if not isinstance(text, str) or not text.strip():
        return False
    # If text is file path, URL, CSS, variable name, don't translate
    s = text.strip()
    if re.match(r'^(https?://|/[a-zA-Z0-9_\-/]+\.(mp4|png|jpg|jpeg|svg|gif|css|js)|shopify://|\d+(\.\d+)?$)', s):
        return False
    if s.startswith('shopify-section') or s.startswith('template--') or s.startswith('icon-') or s.startswith('var(') or s.startswith('#'):
        return False
    if RO_PATTERN.search(s):
        return True
    
    # Check common Romanian words
    lower = s.lower()
    common_ro = [
        'despre', 'pentru', 'nostru', 'noastra', 'noastre', 'cumpara', 'adaugă', 'adauga', 
        'cosul', 'coșul', 'acasa', 'contacteaza', 'filtreaza', 'inchide', 'inapoi', 'toate', 
        'produse', 'tehnologie', 'comanda', 'livrare', 'retur', 'intrebari', 'frecvente',
        'termeni', 'conditii', 'garantie', 'solicitare', 'rambursare', 'comenzii', 'produsul',
        'ingrijire', 'matrice', 'ingrediente', 'utilizare', 'descopera', 'stiinta', 'ritualul'
    ]
    words = set(re.findall(r'\b[a-zA-ZăâîșțĂÂÎȘȚşţŞŢ]+\b', lower))
    if any(w in words for w in common_ro):
        return True
    return False

def translate_phrase(text):
    if not isinstance(text, str) or not text.strip():
        return text
    
    clean_text = text.strip()
    if clean_text in CACHE:
        return text.replace(clean_text, CACHE[clean_text])
    
    if not is_text_romanian(text):
        return text
        
    # Protect HTML tags
    html_tags = re.findall(r'<[^>]+>', text)
    temp_text = text
    for i, tag in enumerate(html_tags):
        temp_text = temp_text.replace(tag, f' ___TAG_{i}___ ', 1)
        
    # Protect Liquid tags
    liquid_tags = re.findall(r'(\{\{.*?\}\}|\{%.*?%\})', temp_text)
    for i, ltag in enumerate(liquid_tags):
        temp_text = temp_text.replace(ltag, f' ___LIQ_{i}___ ', 1)
        
    res = gtrans_direct(temp_text)
    
    # Restore Liquid tags
    for i, ltag in enumerate(liquid_tags):
        res = re.sub(rf'___\s*LIQ_{i}\s*___', ltag, res, flags=re.IGNORECASE)
        res = res.replace(f'___LIQ_{i}___', ltag)
        
    # Restore HTML tags
    for i, tag in enumerate(html_tags):
        res = re.sub(rf'___\s*TAG_{i}\s*___', tag, res, flags=re.IGNORECASE)
        res = res.replace(f'___TAG_{i}___', tag)
        
    # Fix spacing around HTML tags if needed
    res = re.sub(r'\s+(</?[a-z0-9]+[^>]*>)\s+', r'\1', res)
    
    CACHE[clean_text] = res.strip()
    return res

def translate_json_obj(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k in ['type', 'id', 'video_url', 'video_link', 'video_bg', 'image', 'icon', 'color', 'background', 'bg_color']:
                new_dict[k] = v
            elif isinstance(v, str) and (v.endswith(('.mp4', '.png', '.jpg', '.svg', '.jpeg')) or 'shopify://' in v or v.startswith('http')):
                new_dict[k] = v
            else:
                new_dict[k] = translate_json_obj(v)
        return new_dict
    elif isinstance(data, list):
        return [translate_json_obj(item) for item in data]
    elif isinstance(data, str):
        return translate_phrase(data)
    else:
        return data

def process_single_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        m = re.match(r'^(/\*.*?\*/\s*)', content, flags=re.DOTALL)
        comment = m.group(1) if m else ''
        json_content = content[len(comment):]
        
        data = json.loads(json_content)
        translated_data = translate_json_obj(data)
        
        new_json = json.dumps(translated_data, indent=2, ensure_ascii=False)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(comment + new_json + '\n')
        print(f'[JSON OK] {os.path.relpath(file_path, "d:/Lumina")}')
    except Exception as e:
        print(f'[JSON ERR] {file_path}: {e}')

def translate_liquid_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Check if schema exists
        schema_match = re.search(r'(\{%\s*schema\s*%\})(.*?)(\{%\s*endschema\s*%\})', content, flags=re.DOTALL)
        if schema_match:
            pre_schema = content[:schema_match.start(1)]
            schema_prefix = schema_match.group(1)
            schema_json_str = schema_match.group(2)
            schema_suffix = schema_match.group(3)
            post_schema = content[schema_match.end(3):]
            
            # Translate schema JSON
            try:
                schema_data = json.loads(schema_json_str)
                schema_translated = translate_json_obj(schema_data)
                schema_json_new = json.dumps(schema_translated, indent=2, ensure_ascii=False)
            except Exception as se:
                print(f'Schema parse error in {file_path}: {se}')
                schema_json_new = schema_json_str
                
            body = pre_schema
        else:
            body = content
            post_schema = ''
            schema_prefix = ''
            schema_json_new = ''
            schema_suffix = ''
            
        # Translate default text strings inside body: default: '...' or default: "..."
        def repl_default(m):
            q = m.group(1)
            val = m.group(2)
            if is_text_romanian(val):
                return f"default: {q}{translate_phrase(val)}{q}"
            return m.group(0)
            
        body = re.sub(r'default:\s*([\'"])(.*?)\1', repl_default, body)
        
        # Also apply known phrase replacements in body
        for ro, en in BRAND_TERMS.items():
            if ro in body:
                body = body.replace(ro, en)
                
        # Reassemble
        if schema_match:
            new_content = body + schema_prefix + '\n' + schema_json_new + '\n' + schema_suffix + post_schema
        else:
            new_content = body
            
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'[LIQUID OK] {os.path.relpath(file_path, "d:/Lumina")}')
    except Exception as e:
        print(f'[LIQUID ERR] {file_path}: {e}')

if __name__ == '__main__':
    t0 = time.time()
    print('--- Step 1: Translating All JSON Templates & Configs ---')
    all_json = glob.glob('d:/Lumina/templates/**/*.json', recursive=True) + glob.glob('d:/Lumina/templates/*.json', recursive=True)
    all_json.append('d:/Lumina/config/settings_data.json')
    all_json.append('d:/Lumina/sections/footer-group.json')
    all_json = sorted(list(set(all_json)))
    
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(process_single_json_file, all_json))
        
    print('\n--- Step 2: Translating Liquid Sections and Snippets ---')
    liquid_files = glob.glob('d:/Lumina/sections/*.liquid') + glob.glob('d:/Lumina/snippets/*.liquid')
    for lf in liquid_files:
        translate_liquid_file(lf)
        
    print(f'\n--- ALL TRANSLATIONS COMPLETED in {time.time() - t0:.2f}s ---')
