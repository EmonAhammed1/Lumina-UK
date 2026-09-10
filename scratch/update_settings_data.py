import re

with open('config/settings_data.json', 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    '"sale_label_text": "Reducere"': '"sale_label_text": "Sale"',
    '"title": "Ultimele articole de pe blog"': '"title": "Latest Journal Articles"',
    '"menu_banner_heading_1": "Minim 65% reducere"': '"menu_banner_heading_1": "Exclusive Protocols"'
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open('config/settings_data.json', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated config/settings_data.json successfully")
