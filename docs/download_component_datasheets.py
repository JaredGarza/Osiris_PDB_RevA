from pathlib import Path
import urllib.request, concurrent.futures, hashlib, json

root = Path(__file__).resolve().parents[1]
dest = root / 'Datasheets'
dest.mkdir(exist_ok=True)
sources = {
 'AMASS_XT60PW-M.pdf':'https://www.tme.eu/Document/b13629717d44ae038681dba08d18c0b6/XT60PW-M.pdf',
 'AMASS_XT60PW-F.pdf':'https://www.tme.eu/Document/1191bc2fa3aee3c446e5a895fd8f7983/XT60PW-F.pdf',
 'JST_GH.pdf':'https://www.jst-mfg.com/product/pdf/eng/eGH.pdf',
 'Keystone_3568.pdf':'https://www.keyelco.com/product-pdf.cfm?p=306',
 'Littelfuse_MINI_0297_selection_guide.pdf':'https://www.littelfuse.com/assetdocs/fuse-selection-guide?assetguid=1d99e3a6-f314-48d7-b124-9d5d56955f09',
 'TPS7A16.pdf':'https://www.ti.com/lit/ds/symlink/tps7a16.pdf',
 'INA228.pdf':'https://www.ti.com/lit/ds/symlink/ina228.pdf',
 'Nexperia_74AUP1G07.pdf':'https://assets.nexperia.com/documents/data-sheet/74AUP1G07.pdf',
 'Ohmite_FC4L.pdf':'https://www.ohmite.com/assets/images/res-fc4l.pdf',
 'KEMET_C0603C104K4RACTU.pdf':'https://search.kemet.com/component-documentation/download/specsheet/C0603C104K4RACTU',
}
for mpn in ['C2012C0G2A562J125AA','C2012X7R1H105K125AB','C3216X7R1H106K160AC','C2012X7R1A106K125AC','C1608X7R1H104K080AA']:
 sources['TDK_'+mpn+'.pdf']='https://product.tdk.com/info/en/documents/chara_sheet/'+mpn+'.pdf'
def download(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=25) as res: data=res.read()
  if not data.lstrip().startswith(b'%PDF-'): raise ValueError('Response is not a PDF')
  (dest/name).write_bytes(data)
  return {'file':name,'source':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'status':'downloaded'}
 except Exception as e:
  return {'file':name,'source':url,'status':'failed','reason':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 records=list(pool.map(download,sources.items()))
(dest/'sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
for r in records: print(r['file'],r['status'],r.get('reason',''))
