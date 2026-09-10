import glob, re, sys

keywords = [
    'despre', 'echipa', 'termeni', 'conditii', 'retur', 'intrebari', 'frecvente', 'ajutor', 
    'acasa', 'produse', 'colectii', 'ritualuri', 'dimineata', 'seara', 'rapid', 'contacteaza',
    'urmareste', 'sinergii', 'tehnologie', 'nanofibre', 'comenzile', 'contul', 'confidentialitate',
    'livrare', 'protectia', 'consumatorului', 'stiri', 'articole', 'galerie', 'sustenabilitate',
    'baza stiintifica', 'ce sunt', 'sprayuri', 'adauga', 'cumpara', 'vezi', 'toate produsele',
    'cosul tau', 'cos de cumparaturi', 'in stoc', 'epuizat', 'reducere', 'pret', 'descriere',
    'recenzii', 'evaluare', 'detalii', 'beneficii', 'ingrediente', 'utilizare', 'mod de',
    'de ce', 'pentru', 'nostru', 'noastra', 'cum se'
]

for f in sorted(glob.glob('templates/*.json')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
        matches = []
        for idx, line in enumerate(lines):
            clean_l = re.sub(r'\"type\":\s*\"[^\"]+\"', '', line)
            clean_l = re.sub(r'\"id\":\s*\"[^\"]+\"', '', clean_l)
            clean_l = re.sub(r'shopify://[^\"]+', '', clean_l)
            clean_l = re.sub(r'/pages/[^\"]+', '', clean_l)
            clean_l = re.sub(r'/collections/[^\"]+', '', clean_l)
            clean_l = re.sub(r'/products/[^\"]+', '', clean_l)
            clean_l = re.sub(r'/blogs/[^\"]+', '', clean_l)
            clean_l = re.sub(r'\"custom\.[^\"]+\"', '', clean_l)
            for kw in keywords:
                if re.search(rf'\b{kw}\b', clean_l, re.IGNORECASE):
                    matches.append((idx+1, line.strip()))
                    break
        if matches:
            sys.stdout.buffer.write(f'=== {f} ===\n'.encode('utf-8'))
            for lno, l in matches:
                sys.stdout.buffer.write(f'  L{lno}: {l[:100]}\n'.encode('utf-8'))
