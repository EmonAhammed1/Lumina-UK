const fs = require('fs');
const path = require('path');

const sourceBaseDir = 'D:\\Downloads\\Website Lumina Europa-20260806T045554Z-1-001';
const targetDir = 'D:\\Lumina\\videos';

if (!fs.existsSync(targetDir)) {
  fs.mkdirSync(targetDir, { recursive: true });
}

const foundVideos = [];

function scanDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      scanDir(fullPath);
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name).toLowerCase();
      if (['.mp4', '.mov', '.webm'].includes(ext)) {
        foundVideos.push({
          name: entry.name,
          fullPath: fullPath,
          size: fs.statSync(fullPath).size
        });
      }
    }
  }
}

scanDir(sourceBaseDir);

console.log(`Found ${foundVideos.length} video files in ${sourceBaseDir}:\n`);

foundVideos.forEach((vid, idx) => {
  const sizeMB = (vid.size / (1024 * 1024)).toFixed(2);
  console.log(`[${idx + 1}] ${vid.name} (${sizeMB} MB)`);
  console.log(`     Path: ${vid.fullPath}`);
  
  // Copy to targetDir
  const destPath = path.join(targetDir, vid.name);
  fs.copyFileSync(vid.fullPath, destPath);
});

console.log(`\nSuccessfully copied all ${foundVideos.length} videos to ${targetDir}!`);
