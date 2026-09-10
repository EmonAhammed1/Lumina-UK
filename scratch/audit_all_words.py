import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

ro_check = [
    'despre', 'pentru', 'nostru', 'noastra', 'noastre', 'cumpara', 'adaugă', 'adauga', 
    'cosul', 'coșul', 'acasa', 'contacteaza', 'filtreaza', 'inchide', 'inapoi', 
    'produse', 'tehnologie', 'comanda', 'livrare', 'retur', 'intrebari', 'frecvente',
    'termeni', 'conditii', 'garantie', 'solicitare', 'rambursare', 'comenzii', 'produsul',
    'ingrijire', 'matrice', 'ingrediente', 'utilizare', 'descopera', 'stiinta', 'ritualul'
]

ignore_dirs = ['.git', 'node_modules', 'scratch', '.shopify']
ignore_files = ['ro.json', 'page.tehnologie.backup.json', 'locales/fr.json', 'metafields-backup.json', 'processMenuTitle.liquid', 'menu-mobile.liquid']

found = []
for root, dirs, files in os.walk('d:/Lumina'):
    if any(x in root for x in ignore_dirs): continue
    for f in files:
        if f.endswith(('.json', '.liquid')):
            if f in ignore_files: continue
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c = fh.read()
            c_low = c.lower()
            for w in ro_check:
                # Match whole word
                m = re.findall(rf'\b{w}\b', c_low)
                if m:
                    rel = os.path.relpath(p, 'd:/Lumina')
                    found.append((rel, w, len(m)))

print(f'Total suspicious word matches: {len(found)}')
for rel, w, count in found:
    print(f'  {rel}: "{w}" ({count}x)')
