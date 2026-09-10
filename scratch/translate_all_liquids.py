import os, json, re, time, sys, glob
import urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

BRAND_TERMS = {
    "Știință. Ritual. Lumină.": "Science. Ritual. Light.",
    "Ştiinţă. Ritual. Lumină.": "Science. Ritual. Light.",
    "UNDE ȘTIINȚA DEVINE RITUAL": "WHERE SCIENCE BECOMES RITUAL",
    "Unde știința devine ritual": "Where science becomes ritual",
    "Unde Știința Devine Ritual": "Where Science Becomes Ritual",
    "UNDE ȘTIINȚA\nDEVINE\nRITUAL": "WHERE SCIENCE\nBECOMES\nRITUAL",
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
    "Acasă": "Home",
    "Acasa": "Home",
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
    "Trimite formularul de retur": "Submit Return Form",
    "Trimite mesajul": "Send message",
    "Nume": "Name",
    "Prenume": "First Name",
    "Nume de familie": "Last Name",
    "Email": "Email",
    "Telefon": "Phone",
    "Număr comandă": "Order Number",
    "Motivul returului": "Reason for Return",
    "Mesaj": "Message",
    "Descriere": "Description",
    "LIVRARE GRATUITĂ": "COMPLIMENTARY SHIPPING",
    "Livrare gratuită": "Complimentary shipping",
    "pentru comenzi<br>peste XXX lei": "On orders over €150",
    "RETUR ÎN 30 ZILE": "30-DAY RETURNS",
    "Simplu, rapid<br>și fără griji.": "Effortless, insured,<br>and worry-free.",
    "PLĂȚI SECURIZATE": "SECURE PAYMENTS",
    "ASISTENȚĂ": "CONCIERGE & SUPPORT",
    "DEZVOLTATĂ CU GRIJĂ ÎN EUROPA": "CRAFTED WITH CARE IN EUROPE",
    "Calitate, transparență<br>și responsabilitate.": "Quality, transparency<br>and responsibility.",
    "Un moment al zilei în care lumina devine mai caldă, mai rară, mai aproape de piele.": "A moment of the day when light becomes warmer, rarer, and closer to your skin.",
    "Aici încep ritualurile, poveștile și gesturile pe care le descoperi înaintea celorlalți.": "Here begins the rituals, stories, and gestures you discover before anyone else.",
    "Adresa ta de e-mail": "Your email address",
    "REGĂSEȘTE GOLDEN HOUR": "ENTER GOLDEN HOUR",
    "Toate drepturile rezervate.": "All rights reserved.",
    "&copy; 2026 Lumina Europa.<br>Toate drepturile rezervate.": "&copy; 2026 Lumina Europa.<br>All rights reserved.",
    "Vă mulțumim pentru solicitare!": "Thank you for your request!",
    "Formularul dumneavoastră de retur a fost recepționat și înregistrat cu succes.<br>\n        Echipa noastră va analiza detaliile furnizate și vă va transmite instrucțiunile complete de retur pe e-mail în cel mult <strong>24–48 de ore lucrătoare</strong>.": "Your return request has been successfully received and recorded.<br>\n        Our concierge team will review your details and send complete return shipping instructions via email within <strong>24–48 business hours</strong>.",
    "Înapoi la magazin": "Back to Store",
    "Datele clientului": "Customer Details",
    "Nume și prenume": "Full Name",
    "Adresă de email": "Email Address",
    "Număr de telefon": "Phone Number",
    "Detalii comandă": "Order Details",
    "Data plasării comenzii": "Order Date",
    "Data primirii comenzii": "Delivery Date",
    "Produsul / produsele returnate": "Returned Item(s)",
    "Denumirea produsului": "Product Name",
    "Cantitate": "Quantity",
    "Dacă returnați mai multe produse": "Additional Products to Return",
    "Enumerați alte produse pe care doriți să le returnați (Denumire + Cantitate)...": "List additional products to return (Name + Quantity)...",
    "Pentru exercitarea dreptului legal de retragere, nu sunteți obligat(ă) să indicați un motiv. Dacă doriți să ne ajutați să înțelegem mai bine experiența dumneavoastră, puteți selecta opțional:": "To exercise your legal right of withdrawal, you are not required to provide a reason. If you would like to help us improve your experience, you may optionally select:",
    "M-am răzgândit": "Changed my mind",
    "Am comandat produsul greșit": "Ordered the wrong item",
    "Produsul primit nu este cel comandat": "Received incorrect item",
    "Produsul a ajuns deteriorat": "Item arrived damaged",
    "Produsul pare defect / neconform": "Product appears defective / non-compliant",
    "Ambalajul a fost deteriorat": "Packaging was damaged",
    "Alt motiv / Mențiuni privind motivul": "Other Reason / Additional Notes",
    "Precizați dacă este cazul...": "Please specify if applicable...",
    "Starea produsului": "Product Condition",
    "Vă rugăm să selectați varianta aplicabilă:": "Please select the applicable status:",
    "Produsul este sigilat / nedesigilat": "Product is sealed / unopened",
    "Ambalajul exterior deschis, sigiliu igienic intact": "Outer packaging opened, hygiene seal intact",
    "Ambalajul exterior deschis, dar sigiliul igienic este intact": "Outer packaging opened, hygiene seal intact",
    "Sigiliul igienic a fost deschis": "Hygiene seal has been opened",
    "Produsul este deteriorat / neconform": "Product is damaged / non-compliant",
    "Altă situație privind starea produsului": "Other condition details",
    "Important — Protecția Sănătății și Igienă": "Important — Health & Hygiene Protection",
    "Pentru anumite produse sigilate care, din motive de protecție a sănătății sau de igienă, nu pot fi returnate după desigilare, dreptul legal de retragere poate să nu se aplice după deschiderea sigiliului igienic. Această limitare nu afectează drepturile dumneavoastră dacă produsul este defect, deteriorat, incorect sau neconform.": "For sealed skincare products that cannot be returned once unsealed for health or hygiene reasons, the right of withdrawal may not apply if the hygiene seal is broken. This limitation does not affect your rights if the product is defective, damaged, or incorrect.",
    "Soluția solicitată": "Requested Resolution",
    "Rambursare": "Refund",
    "Înlocuire (dacă este aplicabilă și disponibilă)": "Replacement (subject to availability)",
    "Altă soluție solicitată": "Other requested resolution",
    "Pentru un retur standard în baza dreptului de retragere, rambursarea se efectuează conform legislației aplicabile și Politicii de Livrare și Retur.": "For standard returns under withdrawal rights, refunds will be issued in accordance with applicable EU regulations and our Return Policy.",
    "Fotografii / documente (Opțional)": "Photographs / Documentation (Optional)",
    "În cazul unui produs <strong>deteriorat, defect, incorect, expirat, cu ambalaj compromis</strong> sau altfel neconform, vă rugăm să atașați fotografii mai jos sau să le trimiteți pe email la <strong>office@markeu.eu</strong> (fotografii ale produsului, ambalajului, numărului de lot/batch).": "For <strong>damaged, defective, incorrect, or non-compliant</strong> items, please attach photos below or email them to <strong>office@markeu.eu</strong> (photos of item, packaging, and batch number).",
    "Atașează fotografii sau documente": "Attach Photos or Documents",
    "Apasă aici sau trage pozele (JPG, PNG, WEBP, PDF)": "Click here or drag files (JPG, PNG, WEBP, PDF)",
    "Descriere fotografii / detalii lot batch": "Photo Description / Batch Code Details",
    "Introduceți numărul de lot / detalii poze atașate...": "Enter batch number / attached photo details...",
    "Declarație de retragere": "Declaration of Withdrawal",
    "Prin transmiterea acestui formular, vă informez cu privire la decizia mea de a mă retrage din contractul de vânzare pentru produsul/produsele indicate mai sus, atunci când dreptul legal de retragere este aplicabil.": "By submitting this form, I hereby notify you of my withdrawal from the purchase contract for the item(s) specified above, in accordance with applicable consumer law.",
    "Unde se transmite formularul & date companie": "Form Destination & Corporate Entity",
    "Contact operațional:": "Operational Contact:",
    "⚠️ <strong>Notă importantă:</strong> Vă rugăm să nu trimiteți produsele la sediul social înainte de a primi instrucțiunile de retur. Adresa operațională de retur poate fi diferită și poate aparține depozitului sau partenerului logistic care procesează retururile pentru MARKEU.": "⚠️ <strong>Important Note:</strong> Please do not ship return parcels to the registered headquarters prior to receiving return instructions. The operational return warehouse address will be provided in your return confirmation email.",
    "Fișiere selectate": "Selected files",
    "Se încarcă...": "Uploading...",
    "✓ Încărcat cu succes": "✓ Uploaded successfully",
    "⚠️ Încărcare eșuată": "⚠️ Upload failed",
    "Link direct:": "Direct link:",
    "Nicio fotografie încărcată": "No photos attached"
}

CACHE = dict(BRAND_TERMS)
RO_PATTERN = re.compile(r'[ăâîșțĂÂÎȘȚşţŞŢ]')

def gtrans(text):
    if not text or not text.strip(): return text
    clean = text.strip()
    if clean in CACHE:
        return text.replace(clean, CACHE[clean])
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=ro&tl=en&dt=t&q=' + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode('utf-8'))
            res = ''.join([item[0] for item in data[0] if item and item[0]])
            CACHE[clean] = res.strip()
            return res
        except Exception:
            time.sleep(0.2)
    return text

def translate_schema_dict(data):
    if isinstance(data, dict):
        new_d = {}
        for k, v in data.items():
            if k in ['type', 'id', 'default', 'label', 'info', 'content']:
                if isinstance(v, str) and (RO_PATTERN.search(v) or v in BRAND_TERMS):
                    new_d[k] = BRAND_TERMS.get(v, gtrans(v))
                else:
                    new_d[k] = translate_schema_dict(v)
            else:
                new_d[k] = translate_schema_dict(v)
        return new_d
    elif isinstance(data, list):
        return [translate_schema_dict(i) for i in data]
    elif isinstance(data, str) and (RO_PATTERN.search(data) or data in BRAND_TERMS):
        return BRAND_TERMS.get(data, gtrans(data))
    return data

def translate_liquid_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Step A: Apply dictionary replacements
    for ro, en in BRAND_TERMS.items():
        if ro in content:
            content = content.replace(ro, en)

    # Step B: Translate schema JSON if present
    schema_match = re.search(r'(\{%\s*schema\s*%\})(.*?)(\{%\s*endschema\s*%\})', content, flags=re.DOTALL)
    if schema_match:
        prefix = content[:schema_match.start(1)]
        s_tag_open = schema_match.group(1)
        s_body = schema_match.group(2)
        s_tag_close = schema_match.group(3)
        suffix = content[schema_match.end(3):]
        
        try:
            s_data = json.loads(s_body)
            s_trans = translate_schema_dict(s_data)
            s_json_str = json.dumps(s_trans, indent=2, ensure_ascii=False)
            content = prefix + s_tag_open + '\n' + s_json_str + '\n' + s_tag_close + suffix
        except Exception as e:
            print(f'Error translating schema in {os.path.basename(file_path)}: {e}')

    # Step C: Translate any remaining default: '...' strings
    def repl_default(m):
        q = m.group(1)
        val = m.group(2)
        if RO_PATTERN.search(val) or val in BRAND_TERMS:
            return f"default: {q}{BRAND_TERMS.get(val, gtrans(val))}{q}"
        return m.group(0)

    content = re.sub(r'default:\s*([\'"])(.*?)\1', repl_default, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Translated Liquid: {os.path.basename(file_path)}')

if __name__ == '__main__':
    sections = glob.glob('d:/Lumina/sections/*.liquid')
    snippets = glob.glob('d:/Lumina/snippets/*.liquid')
    all_files = sections + snippets
    print(f'Translating {len(all_files)} liquid files...')
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(translate_liquid_file, all_files))
    print('All Liquid files translated successfully!')
