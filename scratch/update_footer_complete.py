import os, json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update sections/footer-lumina.liquid
p_footer_lumina = 'd:/Lumina/sections/footer-lumina.liquid'
with open(p_footer_lumina, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace link rendering with processMenuTitle in all menus
c = c.replace('<li><a href="{{ link.url }}">{{ link.title }}</a></li>',
              '<li><a href="{{ link.url }}">{% render \'processMenuTitle\', itemName: link.title %}</a></li>')
c = c.replace('<a href="{{ link.url }}">{{ link.title }}</a>',
              '<a href="{{ link.url }}">{% render \'processMenuTitle\', itemName: link.title %}</a>')

# Fix default titles & headings
c = c.replace("{{ section.settings.col3_title | default: 'AJUTOR' }}",
              "{{ section.settings.col3_title | default: 'HELP & CONCIERGE' }}")
c = c.replace("{{ section.settings.col2_sub1_title | default: 'PRODUSE' }}",
              "{{ section.settings.col2_sub1_title | default: 'PRODUCTS' }}")
c = c.replace("{{ section.settings.col2_sub2_title | default: 'RITUALURI' }}",
              "{{ section.settings.col2_sub2_title | default: 'RITUALS' }}")

# Schema defaults update
schema_replacements = [
    ('"default": "PRODUSE"', '"default": "PRODUCTS"'),
    ('"default": "RITUALURI"', '"default": "RITUALS"'),
    ('"default": "AJUTOR"', '"default": "HELP & CONCIERGE"'),
    ('"default": "LEGAL"', '"default": "LEGAL"'),
    ('"default": "Masks with Nanofibers"', '"default": "Nanofiber Masks"'),
    ('"default": "Sprayuri pentru Face"', '"default": "Face Sprays"'),
    ('"default": "Seturi & Protocoale"', '"default": "Sets & Protocols"'),
    ('"default": "Toate Produsele"', '"default": "All Products"'),
    ('"default": "Ritual Rapid"', '"default": "Express Ritual"'),
    ('"default": "Contul Meu"', '"default": "My Account"'),
    ('"default": "Comenzile Mele"', '"default": "My Orders"'),
    ('"default": "Livrare"', '"default": "Shipping Policy"'),
    ('"default": "Retururi"', '"default": "Returns & Refunds"'),
    ('"default": "Politica Cookies"', '"default": "Cookie Policy"'),
    ('"default": "ANPC"', '"default": "Consumer Protection (ANPC)"')
]
for ro, en in schema_replacements:
    c = c.replace(ro, en)

with open(p_footer_lumina, 'w', encoding='utf-8') as f:
    f.write(c)
print('[UPDATED] footer-lumina.liquid')

# 2. Update sections/footer.liquid
p_footer = 'd:/Lumina/sections/footer.liquid'
if os.path.exists(p_footer):
    with open(p_footer, 'r', encoding='utf-8') as f:
        fc = f.read()
    fc = fc.replace('<h4 class="h5 site-footer__section-title">{{ linklists[block.settings.link_list].title }}</h4>',
                    '<h4 class="h5 site-footer__section-title">{% render \'processMenuTitle\', itemName: linklists[block.settings.link_list].title %}</h4>')
    fc = fc.replace('<li class="site-footer__list-item"><a href="{{ link.url }}">{{ link.title }}</a></li>',
                    '<li class="site-footer__list-item"><a href="{{ link.url }}">{% render \'processMenuTitle\', itemName: link.title %}</a></li>')
    fc = fc.replace('<li class=""><a href="{{ link.url }}">{{ link.title }}</a></li>',
                    '<li class=""><a href="{{ link.url }}">{% render \'processMenuTitle\', itemName: link.title %}</a></li>')
    with open(p_footer, 'w', encoding='utf-8') as f:
        f.write(fc)
    print('[UPDATED] footer.liquid')

# 3. Update sections/footer-group.json
p_fg = 'd:/Lumina/sections/footer-group.json'
with open(p_fg, 'r', encoding='utf-8') as f:
    fg_text = f.read()
m = re.match(r'^(/\*.*?\*/\s*)', fg_text, flags=re.DOTALL)
comment = m.group(1) if m else ''
fg_data = json.loads(fg_text[len(comment):])

s = fg_data['sections']['footer-lumina']['settings']
s['logo_title'] = 'LUMINA'
s['logo_subtitle'] = 'EUROPA'
s['tagline'] = 'Science.<br>Ritual.<br>Light.'
s['copyright'] = '© 2026 Lumina Europa.<br>All rights reserved.'
s['col1_title'] = 'DISCOVER LUMINA'
s['col1_link1_text'] = 'About Lumina Europa'
s['col1_link2_text'] = 'Nanofiber Technology'
s['col1_link3_text'] = 'How to Use'
s['col1_link4_text'] = 'Active Ingredients'
s['col1_link5_text'] = 'Lumina World'
s['col1_link6_text'] = 'Lumina Golden Hour'

s['col2_title'] = 'COLLECTIONS & RITUALS'
s['col2_sub1_title'] = 'PRODUCTS'
s['col2_sub1_link1_text'] = 'Nanofiber Masks'
s['col2_sub1_link2_text'] = 'Face Sprays'
s['col2_sub1_link3_text'] = 'Sets & Protocols'
s['col2_sub1_link4_text'] = 'All Products'

s['col2_sub2_title'] = 'RITUALS'
s['col2_sub2_link1_text'] = 'Morning Ritual'
s['col2_sub2_link2_text'] = 'Evening Ritual'
s['col2_sub2_link3_text'] = 'Express Ritual'

s['col3_title'] = 'HELP & CONCIERGE'
s['col3_link1_text'] = 'My Account'
s['col3_link2_text'] = 'My Orders'
s['col3_link3_text'] = ''
s['col3_link4_text'] = 'Returns & Refunds'
s['col3_link5_text'] = 'Frequently Asked Questions'
s['col3_link6_text'] = 'Contact Us'

s['col4_title'] = 'LEGAL'
s['col4_link1_text'] = 'Terms and Conditions'
s['col4_link2_text'] = 'Privacy Policy'
s['col4_link3_text'] = 'Cookie Policy'
s['col4_link4_text'] = 'Return Policy'
s['col4_link5_text'] = 'Shipping Policy'
s['col4_link6_text'] = 'Consumer Protection (ANPC)'

s['gh_title'] = 'LUMINA<br>GOLDEN HOUR'
s['gh_text1'] = 'A moment of the day when light becomes warmer, rarer, and closer to your skin.'
s['gh_text2'] = 'Here begins the rituals, stories, and gestures you discover before anyone else.'
s['newsletter_placeholder'] = 'Your email address'
s['newsletter_btn_text'] = 'ENTER GOLDEN HOUR'

s['feat1_title'] = 'COMPLIMENTARY SHIPPING'
s['feat1_text'] = 'On orders over €150'
s['feat2_title'] = '30-DAY RETURNS'
s['feat2_text'] = 'Effortless, insured,<br>and worry-free.'
s['feat3_title'] = 'SECURE PAYMENTS'
s['feat3_text'] = 'Visa • Mastercard • Apple Pay<br>Google Pay • PayPal • Klarna'
s['feat4_title'] = 'CONCIERGE & SUPPORT'
s['feat4_email'] = 'office@luminaeuropa.com'
s['feat5_title'] = 'CRAFTED WITH CARE IN EUROPE'
s['feat5_text'] = 'Quality, transparency<br>and responsibility.'

s['bm_link1_text'] = 'LUMINA EUROPA'
s['bm_link2_text'] = 'COLLECTION'
s['bm_link3_text'] = 'TECHNOLOGY'
s['bm_link4_text'] = 'LUMINA WORLD'
s['bm_link5_text'] = 'GOLDEN HOUR'
s['bm_link8_text'] = 'CONTACT'

with open(p_fg, 'w', encoding='utf-8') as f:
    f.write(comment + json.dumps(fg_data, indent=2, ensure_ascii=False) + '\n')
print('[UPDATED] footer-group.json')

print('All footer components updated to 100% English!')
