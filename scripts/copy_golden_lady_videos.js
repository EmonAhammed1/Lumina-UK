const fs = require('fs');
const path = require('path');

const targetDir = 'D:\\Lumina\\videos';

const additionalFiles = [
  'D:\\dev\\Golden Lady video\\kling_20260723_VIDEO_1__Subject_568_0.mp4',
  'D:\\dev\\Golden Lady video\\kling_20260723_VIDEO_1__Subject_602_0.mp4',
  'D:\\dev\\Golden Lady video\\kling_20260408_作品_1__Subject_5962_0.mp4',
  'D:\\dev\\Golden Lady video\\WhatsApp Video 2026-08-10 at 15.00.17 (1).mp4',
  'D:\\dev\\Golden Lady video\\WhatsApp Video 2026-08-10 at 15.00.17.mp4',
  'D:\\dev\\Golden Lady video\\WhatsApp Video 2026-08-10 at 15.05.00.mp4',
  'C:\\Users\\Betopia\\Downloads\\kling_20260420_Image_to_Video_1____Subje_6094_0.mp4'
];

additionalFiles.forEach(file => {
  if (fs.existsSync(file)) {
    const filename = path.basename(file);
    const dest = path.join(targetDir, filename);
    fs.copyFileSync(file, dest);
    console.log(`Copied: ${filename}`);
  }
});
