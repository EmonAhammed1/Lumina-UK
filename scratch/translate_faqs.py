import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

CAT_MAP = {
    "Produse și Tehnologie": "Products & Technology",
    "Piele, Ingrediente și Siguranță": "Skin, Ingredients & Safety",
    "Mod de Utilizare": "How to Use & Rituals",
    "Comenzi și Livrare": "Orders & Shipping",
    "Retururi și Rambursări": "Returns & Refunds",
    "Utilizare Profesională": "Professional & Spa Use",
    "Autenticitate": "Authenticity & Guarantee",
    "Cont și Confidențialitate": "Account & Privacy",
    "Despre Lumina Europa": "About Lumina Europa",
    "Toate": "All",
    "TOATE": "ALL"
}

# Key term dictionary for replacement in text
TERMS = [
    ("Lumina Europa este un brand european de îngrijire a pielii axat pe tehnologia avansată a nanofibrelor, formulare atentă și ideea că îngrijirea pielii poate fi atât eficientă, cât și un adevărat ritual. Produsele noastre sunt concepute pentru a aduce ingrediente atent selecționate în contact strâns și uniform cu pielea.",
     "Lumina Europa is a European luxury skincare brand focused on advanced nanofiber biotechnology, precise formulation, and the philosophy that skincare should be both clinically transformative and a mindful ritual. Our formulations deliver pure encapsulated actives in intimate contact with the skin."),
    ("Ce este Lumina Europa?", "What is Lumina Europa?"),
    ("Prin ce se diferențiază Lumina Europa de o mască șervețel tradițională?", "How does Lumina Europa differ from a traditional sheet mask?"),
    ("Măștile șervețel tradiționale sunt de obicei fabricate din țesătură sau hidrogel îmbibat în ser. Măștile cu nanofibre Lumina folosesc o structură extrem de fină de fibre, concepută pentru a se mula perfect pe conturul natural al feței. Acest lucru creează o experiență de aplicare complet diferită și permite livrarea formulei active fără senzația grea și umedă a unei măști convenționale.",
     "Traditional sheet masks are typically woven fabrics or hydrogels soaked in liquid serum. Lumina nanofiber masks utilize an ultra-fine dry fiber matrix that seamlessly conforms to facial contours like a second skin, dissolving upon contact with moisture to deliver concentrated actives without wet dripping or heavy residue."),
    ("Ce sunt nanofibrele?", "What are nanofibers?"),
    ("Nanofibrele sunt fibre excepțional de fine, create folosind tehnologii specializate de fabricație. Diametrul lor redus le permite să formeze o structură ușoară și extrem de adaptabilă, care se așază perfect pe suprafața pielii.",
     "Nanofibers are exceptionally fine fibers engineered through precision electrospinning technology. Their microscopic diameter creates an ultra-light, second-skin matrix that adheres flawlessly to the skin for targeted nutrient transfer."),
    ("Înseamnă „nanofibră” că produsul conține nanoparticule?", "Does \"nanofiber\" mean the product contains nanoparticles?"),
    ("Nu neapărat. „Nanofibră” descrie structura fizică a materialului din fibre. Nu trebuie interpretat ca însemnând că fiecare ingredient din formulare este un nanomaterial sau o nanoparticulă.",
     "No. \"Nanofiber\" describes the physical structural matrix of the woven fiber scaffold, not the molecular size of individual active ingredients."),
    ("Unde sunt fabricate produsele Lumina Europa?", "Where are Lumina Europa products crafted?"),
    ("Produsele noastre sunt dezvoltate și fabricate în Europa, în colaborare cu parteneri științifici și unități de producție specializate.",
     "Our formulations and nanofiber matrices are developed and manufactured in the European Union in collaboration with leading biotechnology laboratories and clinical specialists."),
    ("Sunt produsele Lumina Europa potrivite pentru toate tipurile de piele?", "Are Lumina Europa products suitable for all skin types?"),
    ("Formulele noastre sunt create cu accent pe compatibilitatea cu pielea și toleranță ridicată. Cu toate acestea, recomandăm întotdeauna consultarea listei complete de ingrediente și efectuarea unui test pe o porțiune mică de piele dacă aveți sensibilități cunoscute.",
     "Our formulations are crafted for high biocompatibility and gentle skin tolerance. However, we always recommend reviewing the ingredient list and performing a patch test if you have specific dermatological sensitivities."),
    ("Cum integrez masca în rutina mea existentă?", "How do I incorporate the mask into my existing skincare ritual?"),
    ("Aplicați pe tenul proaspăt curățat și ușor umed. Lăsați masca să acționeze timpul recomandat, apoi masați delicat excesul de formulă până la absorbția completă. Continuați cu crema hidratantă preferată dacă este necesar.",
     "Apply to freshly cleansed, moist skin. Allow the mask to rest for the recommended 15–20 minutes, then gently press any remaining essence into the skin. Follow with your preferred moisturizer if desired."),
    ("Cât de des ar trebui să folosesc masca?", "How often should I use the mask?"),
    ("Pentru majoritatea tipurilor de ten, utilizarea de 2–3 ori pe săptămână oferă rezultate optime. Pentru protocoale intensive de recuperare sau înainte de evenimente importante, poate fi utilizată conform nevoilor pielii.",
     "For most skin types, 2–3 times weekly provides optimal radiance and hydration. For intensive recovery protocols or special occasions, use as desired according to your skin's needs."),
    ("Care este politica de retur?", "What is your return policy?"),
    ("Oferim retur gratuit în termen de 30 de zile pentru produsele nedesfăcute și aflate în ambalajul original.",
     "We offer complimentary returns within 30 days for unopened products in their original luxury packaging."),
    ("Cum pot urmări comanda mea?", "How can I track my order?"),
    ("Odată expediată comanda, veți primi un e-mail de confirmare cu numărul de urmărire și linkul direct către serviciul de curierat.",
     "Once your order ships, you will automatically receive an email confirmation with a tracking number and direct courier tracking link."),
    ("Livrările internaționale sunt disponibile?", "Is international shipping available?"),
    ("Da, livrăm în întreaga Uniune Europeană, Marea Britanie și internațional prin servicii de curierat premium.",
     "Yes, we ship across the European Union, the United Kingdom, and internationally via premium express couriers.")
]

def clean_ro_general(text):
    if not text:
        return text
    
    # Specific term replacements
    for ro, en in TERMS:
        text = text.replace(ro, en)
        
    for ro_cat, en_cat in CAT_MAP.items():
        text = text.replace(ro_cat, en_cat)
        
    # Common phrase patterns in Romanian
    replacements = [
        (r'îngrijire a pielii', 'skincare'),
        (r'îngrijirea pielii', 'skincare'),
        (r'îngrijire', 'skincare'),
        (r'tehnologia nanofibrelor', 'nanofiber technology'),
        (r'tehnologie avansată', 'advanced technology'),
        (r'ingrediente active', 'active ingredients'),
        (r'ingrediente atent selecționate', 'thoughtfully selected ingredients'),
        (r'acid hialuronic', 'hyaluronic acid'),
        (r'Acid Hialuronic', 'Hyaluronic Acid'),
        (r'niacinamidă', 'niacinamide'),
        (r'Niacinamidă', 'Niacinamide'),
        (r'ten sensibil', 'sensitive skin'),
        (r'ten uscat', 'dry skin'),
        (r'ten gras', 'oily skin'),
        (r'ten mixt', 'combination skin'),
        (r'livrare gratuită', 'complimentary shipping'),
        (r'Livrare gratuită', 'Complimentary shipping'),
        (r'Livrare Gratuită', 'Complimentary Shipping'),
        (r'în termen de (\d+) zile', r'within \1 days'),
        (r'fără parabeni', 'paraben-free'),
        (r'fără parfum', 'fragrance-free'),
        (r'fără conservanți', 'preservative-free'),
        (r'Uniunea Europeană', 'European Union'),
        (r'Marea Britanie', 'United Kingdom'),
        (r'Statele Unite', 'United States'),
        (r'România', 'Romania'),
        (r'Florența, Italia', 'Florence, Italy'),
        (r'Paris, Franța', 'Paris, France'),
        (r'Brașov, România', 'Brașov, Romania'),
        (r'Veneția, Italia', 'Venice, Italy'),
        (r'Sibiu, România', 'Sibiu, Romania'),
        (r'München, Germania', 'Munich, Germany'),
        (r'Budapesta, Ungaria', 'Budapest, Hungary'),
        (r'Nisa, Franța', 'Nice, France'),
        (r'Cluj-Napoca, România', 'Cluj-Napoca, Romania'),
        (r'Stockholm, Suedia', 'Stockholm, Sweden'),
        (r'Lisabona, Portugalia', 'Lisbon, Portugal'),
        (r'Roma, Italia', 'Rome, Italy')
    ]
    for pat, rep in replacements:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)
        
    return text

for file_name in ['page.faq.json', 'page.faqs.json']:
    path = f'd:/Lumina/templates/{file_name}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    clean_content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL).strip()
    data = json.loads(clean_content)
    
    faq_sec = data.get('sections', {}).get('lumina_faq', {})
    if 'settings' in faq_sec:
        st = faq_sec['settings']
        if st.get('title') == "Întrebări Frecvente":
            st['title'] = "Frequently Asked Questions"
        if st.get('subtitle') == "Găsește răspunsuri la întrebările tale despre Lumina Europa":
            st['subtitle'] = "Find answers to your questions about Lumina Europa, our science, and rituals."
        if st.get('search_placeholder') == "Caută o întrebare...":
            st['search_placeholder'] = "Search questions..."
            
    blocks = faq_sec.get('blocks', {})
    for k, b in blocks.items():
        st = b.get('settings', {})
        cat = st.get('category', '')
        if cat in CAT_MAP:
            st['category'] = CAT_MAP[cat]
        q = st.get('question', '')
        a = st.get('answer', '')
        st['question'] = clean_ro_general(q)
        st['answer'] = clean_ro_general(a)
        
    new_json = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w', encoding='utf-8') as f:
        f.write('/* Auto-generated */\n' + new_json + '\n')
    print(f'Processed FAQs in {file_name}')
