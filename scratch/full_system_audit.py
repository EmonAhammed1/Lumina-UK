import os, re, sys

romanian_patterns = [
    r'\bdespre\b', r'\bechipa\b', r'\btermeni\b', r'\bconditii\b', r'\bretururi?\b',
    r'\bintrebari\b', r'\bfrecvente\b', r'\bajutor\b', r'\bacasa\b', r'\bproduse\b',
    r'\bcolectii\b', r'\britualuri\b', r'\bdimineata\b', r'\bseara\b', r'\bcontacteaza\b',
    r'\burmareste\b', r'\bsinergii\b', r'\bcomenzile\b', r'\bcontul\b', r'\bconfidentialitate\b',
    r'\blivrare\b', r'\bprotectia\b', r'\bconsumatorului\b', r'\bstiri\b', r'\bsustenabilitate\b',
    r'\bbaza stiintifica\b', r'\bce sunt\b', r'\bsprayuri\b', r'\badauga\b', r'\bcumpara\b',
    r'\bvezi\b', r'\btoate produsele\b', r'\bcosul tau\b', r'\bcos de cumparaturi\b',
    r'\bin stoc\b', r'\bepuizat\b', r'\breducere\b', r'\brecenzii\b', r'\bevaluare\b',
    r'\bbeneficii\b', r'\bde ce\b', r'\bpentru membrii\b', r'\bnoastra\b', r'\bnostru\b'
]

diacritics = ['ă', 'â', 'î', 'ș', 'ț', 'Ă', 'Â', 'Î', 'Ș', 'Ț']

ignore_paths = ['.git', 'node_modules', 'scratch', 'locales/ro.json', 'locales/de.json', '.shopify']

suspicious_lines = []

for root, dirs, files in os.walk('.'):
    # filter ignored directories
    dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'scratch', '.shopify']]
    for f in files:
        if f.endswith(('.liquid', '.json')):
            p = os.path.join(root, f)
            rel_p = p.replace('\\', '/')
            if rel_p in ['./locales/ro.json', './locales/de.json', './.shopify/metafields.json', './metafields-backup.json', './extracted_images.json']:
                continue
            
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()
                for idx, line in enumerate(lines):
                    # Check if line contains Romanian words or diacritics
                    # Exclude processMenuTitle dictionary definitions (they need Romanian when cases)
                    if 'snippets/processMenuTitle.liquid' in rel_p or 'snippets/menu-mobile.liquid' in rel_p:
                        continue
                    # Exclude URL handles
                    clean = re.sub(r'shopify://[^\"]+', '', line)
                    clean = re.sub(r'/pages/[^\"]+', '', clean)
                    clean = re.sub(r'/collections/[^\"]+', '', clean)
                    clean = re.sub(r'/products/[^\"]+', '', clean)
                    clean = re.sub(r'/blogs/[^\"]+', '', clean)
                    clean = re.sub(r'news/de-ce-[^\"]+', '', clean)
                    clean = re.sub(r'\"custom\.[^\"]+\"', '', clean)
                    clean = re.sub(r'filter\.[^\"]+', '', clean)
                    clean = re.sub(r'\.descriere-[^\s]+', '', clean)
                    clean = re.sub(r'Beneficii(-m)?\.png', '', clean)
                    
                    for pat in romanian_patterns:
                        if re.search(pat, clean, re.IGNORECASE):
                            suspicious_lines.append((rel_p, idx + 1, line.strip()))
                            break
                    
                    for d in diacritics:
                        if d in clean:
                            suspicious_lines.append((rel_p, idx + 1, f'[DIACRITIC {d}] ' + line.strip()))
                            break

print(f"Total suspicious lines found: {len(suspicious_lines)}")
for p, lno, text in suspicious_lines:
    print(f"  {p}:{lno} -> {text[:100]}")
