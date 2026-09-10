import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

ro_words = [
    'despre noi', 'contacteaza-ne', 'cumpara acum', 'adauga in cos', 
    'termeni si conditii', 'politica de retur', 'politica de livrare', 'intrebari frecvente',
    'vezi toate', 'exploreaza colectia', 'toate drepturile rezervate', 'formular de retur',
    'mod de utilizare', 'ingrediente active', 'pentru toate tipurile'
]

ignore_dirs = ['.git', 'node_modules', 'scratch', '.shopify']
ignore_files = ['ro.json', 'page.tehnologie.backup.json', 'locales/fr.json', 'metafields-backup.json']

found = []
for root, dirs, files in os.walk('d:/Lumina'):
    if any(x in root for x in ignore_dirs):
        continue
    for f in files:
        if f.endswith(('.json', '.liquid')):
            if f in ignore_files: continue
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fh:
                c_low = fh.read().lower()
            for w in ro_words:
                if w in c_low:
                    # Ignore when matching case statements in snippets/processMenuTitle.liquid or snippets/menu-mobile.liquid
                    if f in ['processMenuTitle.liquid', 'menu-mobile.liquid']:
                        continue
                    found.append((os.path.relpath(p, 'd:/Lumina'), w))

print(f'Total word matches found: {len(found)}')
for rel, w in found:
    print(f'  {rel}: "{w}"')
