const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const rootDir = 'd:\\Lumina';
const videosDir = path.join(rootDir, 'videos');

if (!fs.existsSync(videosDir)) {
  fs.mkdirSync(videosDir, { recursive: true });
}

const foundUrls = new Map(); // url -> Array of { file, line }

function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (['.git', 'node_modules', 'videos', '.gemini'].includes(entry.name)) continue;
      scanDir(fullPath);
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name).toLowerCase();
      if (['.json', '.liquid', '.js', '.css', '.html', '.md'].includes(ext)) {
        scanFile(fullPath);
      }
    }
  }
}

function scanFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');

  // Regex to match video URLs or shopify video CDN links
  const regex = /https?:\/\/[^\s"'<>\\]+?\.(?:mp4|webm|mov|m3u8)(?:\?[^\s"'<>\\]*)?|https?:\/\/cdn\.shopify\.com\/videos\/[^\s"'<>\\]+/gi;

  lines.forEach((line, idx) => {
    let match;
    while ((match = regex.exec(line)) !== null) {
      let rawUrl = match[0].replace(/\\"/g, '').replace(/\\/g, '').replace(/",?$/, '').replace(/',?$/, '');
      if (rawUrl.endsWith('"') || rawUrl.endsWith("'") || rawUrl.endsWith(',')) {
        rawUrl = rawUrl.slice(0, -1);
      }
      if (!foundUrls.has(rawUrl)) {
        foundUrls.set(rawUrl, []);
      }
      const relPath = path.relative(rootDir, filePath);
      foundUrls.get(rawUrl).push({ file: relPath, line: idx + 1 });
    }
  });
}

scanDir(rootDir);

console.log(`Found ${foundUrls.size} unique video URLs across the store:\n`);

let index = 1;
for (const [url, locations] of foundUrls.entries()) {
  console.log(`[${index++}] ${url}`);
  locations.slice(0, 5).forEach(loc => console.log(`    -> ${loc.file}:${loc.line}`));
  if (locations.length > 5) {
    console.log(`    ... and ${locations.length - 5} more places`);
  }
}

// Function to download a URL to destination
function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return downloadFile(res.headers.location, destPath).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) {
        reject(new Error(`Failed with status ${res.statusCode}`));
        return;
      }
      const fileStream = fs.createWriteStream(destPath);
      res.pipe(fileStream);
      fileStream.on('finish', () => {
        fileStream.close();
        resolve(fs.statSync(destPath).size);
      });
      fileStream.on('error', (err) => {
        fs.unlink(destPath, () => {});
        reject(err);
      });
    });
    req.on('error', reject);
  });
}

async function runDownloads() {
  console.log('\n--- Downloading Videos ---');
  for (const [url, locations] of foundUrls.entries()) {
    try {
      // Determine appropriate filename
      let filename = path.basename(new URL(url).pathname);
      if (!filename.includes('.mp4') && !filename.includes('.webm')) {
        filename += '.mp4';
      }
      const destPath = path.join(videosDir, filename);
      console.log(`Downloading: ${url} -> ${filename}`);
      const size = await downloadFile(url, destPath);
      console.log(`  ✓ Saved ${filename} (${(size / 1024 / 1024).toFixed(2)} MB)`);
    } catch (err) {
      console.error(`  ✗ Failed to download ${url}: ${err.message}`);
    }
  }
  console.log('\n--- Download complete ---');
}

runDownloads();
