import fs from 'node:fs/promises';
import { Workbook } from '@oai/artifact-tool';
const root = new URL('../../../', import.meta.url);
const components = JSON.parse(await fs.readFile(new URL('components.json', import.meta.url),'utf8'));
for (const name of ['BOM.csv','BOM_purchasing.csv']) {
 const path = new URL(name,root);
 const wb = await Workbook.fromCSV(await fs.readFile(path,'utf8'),{sheetName:'BOM'});
 const sheet = wb.worksheets.getItem('BOM');
 const width = name==='BOM.csv'?11:13;
 const last = String.fromCharCode(64+width);
 const rows=sheet.getRange(`A1:${last}100`).values.filter(r=>r[0] && r[0]!=='D2');
 const header=rows[0];
 for(const p of components){
  let row=rows.find(r=>r[0]===p.Reference);
  if(!row){row=Array(width).fill('');row[0]=p.Reference;rows.push(row);}
  for(const key of ['Value','Footprint','Manufacturer','MPN','Datasheet']) {
   const i=header.indexOf(key);if(i>=0 && p[key]!==undefined)row[i]=p[key];
  }
  row[header.indexOf('Selection Status')]=p.Selection_Status||'';
  if(p.Reference==='F1')row[header.indexOf('Specification')]='4 A, 32 VDC MINI blade fuse; coordination pending';
  if(p.Reference==='R5')row[header.indexOf('Specification')]='5 mOhm, 1%, 2 W four-terminal; pulse qualification pending';
  if(p.Reference==='C1')row[header.indexOf('Specification')]='22 nF, 100 V, C0G, 5%, 0805';
  if(/^R1[3-8]$/.test(p.Reference))row[header.indexOf('Specification')]='0805 resistor; verify exact manufacturer order code and tolerance';
  if(p.Reference==='R14')row[header.indexOf('Specification')]='22 MOhm, 5%, 0805';
  if(p.DNP)row[header.indexOf('Specification')]='DNP; host provides I2C pull-up to switched 3.3 V';
  if(header.includes('Quantity'))row[header.indexOf('Quantity')]=p.DNP?'0':'1';
  if(header.includes('BOM Role'))row[header.indexOf('BOM Role')]='Schematic component';
 }
 sheet.getRange(`A1:${last}100`).values=Array.from({length:100},()=>Array(width).fill(''));
 sheet.getRange(`A1:${last}${rows.length}`).values=rows;
 wb.recalculate();
 const out=sheet.getRange(`A1:${last}${rows.length}`).values;
 const encode=v=>{const s=String(v??'');return /[",\r\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
 await fs.writeFile(path,out.map(r=>r.map(encode).join(',')).join('\r\n')+'\r\n');
 console.log(`${name}: ${rows.length-1} entries; current schematic values reconciled`);
}

