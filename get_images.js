const fs = require('fs');
const path = require('path');

function getFiles(dir) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const list = fs.readdirSync(dir);
  list.forEach(file => {
    file = path.join(dir, file);
    const stat = fs.statSync(file);
    if (stat && stat.isDirectory()) results = results.concat(getFiles(file));
    else if (file.endsWith('.json') || file.endsWith('.liquid')) results.push(file);
  });
  return results;
}

const allFiles = [...getFiles('templates'), ...getFiles('config'), ...getFiles('sections')];
const images = new Set();
const regex = /shopify:\/\/shop_images\/([^"'\s?]+)/g;

allFiles.forEach(f => {
  const content = fs.readFileSync(f, 'utf8');
  let match;
  while ((match = regex.exec(content)) !== null) {
    images.add(match[1]);
  }
});

console.log('Total unique images:', images.size);
const imgArr = Array.from(images).sort();
fs.writeFileSync('extracted_images.json', JSON.stringify(imgArr, null, 2));
console.log('Saved to extracted_images.json');
