import os, sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. sections/lumina-world-journal-grid.liquid
p = 'd:/Lumina/sections/lumina-world-journal-grid.liquid'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('Contribuția ta a fost recepționată cu succes. Echipa noastră editorială va analiza materialul trimis și te va contacta pe e-mail sau pe profilul de social media furnizat.',
              'Your story submission has been received with appreciation. Our editorial team will review your piece and reach out via email.')
c = c.replace('Back la Jurnal', 'Back to Journal')
c = c.replace('FII PARTE DIN JURNAL', 'JOIN THE JOURNAL')
c = c.replace('Trimite Povestea Ta', 'Submit Your Story')
c = c.replace('Jurnalul Lumina', 'Lumina Journal')
c = c.replace('placeholder="ex. Maria Ionescu"', 'placeholder="e.g. Maria Vance"')
c = c.replace('placeholder="ex. maria@exemplu.com"', 'placeholder="e.g. maria@example.com"')
c = c.replace('Profil Social Media (Instagram / Facebook etc.)', 'Social Media Profile (Instagram / LinkedIn etc.)')
c = c.replace('placeholder="ex. @maria.ionescu sau link https://instagram.com/..."', 'placeholder="e.g. @maria.vance or https://instagram.com/..."')
c = c.replace('Titlul Jurnalului / Articolului', 'Journal / Article Title')
c = c.replace('placeholder="Despre ce este povestea ta?"', 'placeholder="What is your story about?"')
c = c.replace('Scrie povestea ta pentru jurnal', 'Share your story for the journal')
c = c.replace('placeholder="Scrie aici povestea ta, reflecțiile sau articolul pe care dorești să îl împărtășești în Jurnal..."',
              'placeholder="Write your reflection, skincare ritual, or perspective you wish to share in the Journal..."')
c = c.replace('TRIMITE JURNALUL', 'SUBMIT STORY')
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

# 2. sections/lumina-gallery-full.liquid & sections/lumina-gallery.liquid
for fn in ['sections/lumina-gallery-full.liquid', 'sections/lumina-gallery.liquid']:
    p = 'd:/Lumina/' + fn
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('Linkul Fotografiei (URL ImgBB sau link direct)', 'Photo Link (ImgBB URL or Direct Image Link)')
    c = c.replace('placeholder="ex. https://i.ibb.co/abcdef/fotografia-mea.jpg"', 'placeholder="e.g. https://i.ibb.co/abcdef/my-photo.jpg"')
    c = c.replace('placeholder="ex. Florence, Italy — capturat în lumina caldă a apusului..."', 'placeholder="e.g. Florence, Italy — golden hour afternoon glow..."')
    c = c.replace('TRIMITE FOTOGRAFIA', 'SUBMIT PHOTO')
    c = c.replace('Trimite Fotografia Ta', 'Submit Your Photo')
    c = c.replace('Trimite fotografia', 'Submit photo')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

print('Updated last few files!')
