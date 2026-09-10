const fs = require('fs');
const path = require('path');

const rootDir = 'd:\\Lumina';
const templatesDir = path.join(rootDir, 'templates');
const sectionsDir = path.join(rootDir, 'sections');
const configDir = path.join(rootDir, 'config');

const allJsonFiles = [];

function findJsonFiles(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory() && !['.git', 'node_modules', 'videos'].includes(entry.name)) {
      findJsonFiles(fullPath);
    } else if (entry.isFile() && entry.name.endsWith('.json')) {
      allJsonFiles.push(fullPath);
    }
  }
}

findJsonFiles(rootDir);

console.log(`Checking ${allJsonFiles.length} JSON files for video settings...`);

const videoKeys = new Set();
const foundSettings = [];

allJsonFiles.forEach(file => {
  try {
    const content = fs.readFileSync(file, 'utf8');
    const json = JSON.parse(content);
    
    function traverse(obj, currentPath) {
      if (!obj || typeof obj !== 'object') return;
      for (const [k, v] of Object.entries(obj)) {
        const p = currentPath ? `${currentPath}.${k}` : k;
        if (typeof v === 'string') {
          if (v.includes('.mp4') || v.includes('/videos/') || k.toLowerCase().includes('video')) {
            foundSettings.push({
              file: path.relative(rootDir, file),
              key: p,
              value: v
            });
          }
        } else if (typeof v === 'object') {
          traverse(v, p);
        }
      }
    }
    
    traverse(json, '');
  } catch (e) {
    // Ignore parse error
  }
});

console.log(`Found ${foundSettings.length} video settings in JSON files:\n`);
foundSettings.forEach(s => {
  console.log(`[${s.file}] -> ${s.key}: "${s.value}"`);
});
