import fs from 'node:fs/promises';
import sharp from 'sharp';
const svg=process.argv[2]||new URL('render/Osiris_PDB_RevA.svg',import.meta.url);
const output=process.argv[3]||new URL('render/schematic.png',import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1');
await sharp(await fs.readFile(svg),{density:160}).png().toFile(output);
