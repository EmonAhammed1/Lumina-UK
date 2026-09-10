const fs = require('fs');
const path = require('path');
const https = require('https');

const images = JSON.parse(fs.readFileSync('extracted_images.json', 'utf8'));
const outDir = path.join(__dirname, 'downloaded_images');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

console.log(`Starting download of ${images.length} images...`);

function downloadImage(filename) {
  return new Promise((resolve) => {
    const filePath = path.join(outDir, filename);
    if (fs.existsSync(filePath) && fs.statSync(filePath).size > 0) {
      return resolve({ filename, status: 'already_exists' });
    }

    const encodedFilename = encodeURIComponent(filename);
    const url = `https://markeu-2.myshopify.com/cdn/shop/files/${encodedFilename}`;

    const fileStream = fs.createWriteStream(filePath);
    https.get(url, (res) => {
      if (res.statusCode === 200) {
        res.pipe(fileStream);
        fileStream.on('finish', () => {
          fileStream.close();
          resolve({ filename, status: 'downloaded', size: fs.statSync(filePath).size });
        });
      } else {
        fileStream.close();
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
        resolve({ filename, status: 'not_found', statusCode: res.statusCode });
      }
    }).on('error', (err) => {
      fileStream.close();
      if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
      resolve({ filename, status: 'error', error: err.message });
    });
  });
}

async function run() {
  const batchSize = 10;
  let downloadedCount = 0;
  let notFoundCount = 0;
  let errorCount = 0;
  const notFoundList = [];

  for (let i = 0; i < images.length; i += batchSize) {
    const batch = images.slice(i, i + batchSize);
    const results = await Promise.all(batch.map(img => downloadImage(img)));
    results.forEach(res => {
      if (res.status === 'downloaded' || res.status === 'already_exists') {
        downloadedCount++;
      } else if (res.status === 'not_found') {
        notFoundCount++;
        notFoundList.push(res.filename);
      } else {
        errorCount++;
      }
    });
    console.log(`Progress: ${Math.min(i + batchSize, images.length)}/${images.length} (Downloaded: ${downloadedCount}, Not Found: ${notFoundCount})`);
  }

  console.log(`\nFinished! Total downloaded: ${downloadedCount}, Not Found: ${notFoundCount}, Errors: ${errorCount}`);
  if (notFoundList.length > 0) {
    fs.writeFileSync('not_found_images.json', JSON.stringify(notFoundList, null, 2));
    console.log('Saved not_found list to not_found_images.json');
  }
}

run();
