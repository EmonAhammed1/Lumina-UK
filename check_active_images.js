const fs = require('fs');
const path = require('path');
const downloaded = new Set(fs.readdirSync('downloaded_images'));

const mainTemplates = [
  'config/settings_data.json',
  'templates/index.json',
  'templates/page.golden-hour.json',
  'templates/page.tehnologie.json',
  'templates/page.lumina-world.json',
  'templates/page.contact.json',
  'templates/collection.json',
  'templates/product.json',
  'templates/product.30-days-hydrating.json',
  'templates/product.anti-aging-protocol.json',
  'templates/product.autumn-glow.json',
  'templates/product.city-skin-revival.json',
  'templates/product.discovery-protocol.json',
  'templates/product.midsummer-nights-dream.json',
  'templates/product.monthly-skin-wardrobe.json',
  'templates/product.red-carpet.json',
  'templates/product.spring-awakening.json',
  'templates/product.summer-glow.json',
  'templates/product.take-me-to-church.json',
  'templates/product.weekend-getaway.json',
  'templates/product.winter-cocoon.json'
];

const regex = /shopify:\/\/shop_images\/([^"'\s?]+)/g;

let grandTotal = 0;
let grandFound = 0;
const allMissing = new Set();

mainTemplates.forEach(t => {
  if (!fs.existsSync(t)) return;
  const content = fs.readFileSync(t, 'utf8');
  let match;
  let total = 0, found = 0;
  const missing = [];
  while ((match = regex.exec(content)) !== null) {
    total++;
    grandTotal++;
    if (downloaded.has(match[1])) {
      found++;
      grandFound++;
    } else {
      missing.push(match[1]);
      allMissing.add(match[1]);
    }
  }
  console.log(`${t}: ${found}/${total} images available`);
});

console.log(`\nOVERALL ACTIVE TEMPLATES: ${grandFound}/${grandTotal} images available (${Math.round(grandFound/grandTotal*100)}%)`);
console.log('Unique missing in active templates:', allMissing.size);
console.log(Array.from(allMissing));
