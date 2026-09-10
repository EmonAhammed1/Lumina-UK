import glob, os, re

translations = {
    '"why_love_title": "De ce o vei iubi"': '"why_love_title": "Why you will love it"',
    '"nano_title": "Tehnologia Nanofibre"': '"nano_title": "Nanofiber Technology"',
    '"title_tab": "Descriere"': '"title_tab": "Description"',
    '"heading": "Ritualuri complete"': '"heading": "Complete Rituals"',
    '"heading_1": "Tehnologia cu nanofibre care"': '"heading_1": "Nanofiber technology that"',
    '"code": "Look-uri decadente cu 20% reducere"': '"code": "Decadent looks with 20% off"',
    '"category": "SUSTENABILITATE"': '"category": "SUSTAINABILITY"',
    '"title": "ARTICOLE"': '"title": "ARTICLES"',
    '"title": "Ritualuri sezoniere"': '"title": "Seasonal Rituals"',
    '"heading": "Beneficii"': '"heading": "Benefits"',
    '"eyebrow": "GALERIE LUMINA"': '"eyebrow": "LUMINA GALLERY"',
    '"subtitle": "DE CE NANOFIBRE"': '"subtitle": "WHY NANOFIBERS"',
    '"subtitle": "SINERGII DE RITUAL"': '"subtitle": "RITUAL SYNERGIES"'
}

modified_files = []
for p in glob.glob('templates/*.json'):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig = content
    for k, v in translations.items():
        content = content.replace(k, v)
    
    if content != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        modified_files.append(p)

print(f"Updated {len(modified_files)} template files:")
for m in modified_files:
    print(f"  - {m}")
