# Step 4: final.json -> emo_gen.js (picture data), emo_names.js (TR/EN/DE names), emo_albums.js (albums)
# The three files are pasted into index.html (EMO after `const POOL=...`, EMO_NAMES before `const nameOf`,
# EMO_ALBUMS before `const STAR_AT`).
import json,re
it=json.load(open('final.json'))
DROPF=re.compile(r"^grinning face|money-mouth|^(black|white|yellow|orange) heart$|tears of joy|ballot box|money with wings|^pig nose$|^wing$",re.I)
it=[i for i in it if not DROPF.search(i['name'])]
for i in it:
    if i['name']=='elephant':i['cat']='animals'
groups=[('animals',['Hayvanlar','Animals','Tiere']),('sea',['Deniz ve böcekler','Sea and bugs','Meer und Insekten']),('plants',['Bitkiler ve çiçekler','Plants and flowers','Pflanzen und Blumen']),
 ('fruit',['Meyve ve sebze','Fruit and vegetables','Obst und Gemüse']),('food',['Lezzetler','Treats','Leckereien']),('sky',['Gökyüzü ve doğa','Sky and nature','Himmel und Natur']),
 ('vehicles',['Taşıtlar ve yerler','Vehicles and places','Fahrzeuge und Orte']),('fun',['Spor ve oyun','Sports and games','Sport und Spiel']),('things',['Müzik ve eşyalar','Music and things','Musik und Dinge']),('faces',['Yüzler ve kalpler','Faces and hearts','Gesichter und Herzen'])]
merge={'bugs':'sea','places':'vehicles'}
for i in it:i['cat']=merge.get(i['cat'],i['cat'])
albums=[]
for gid,n in groups:
    sel=[i['name'] for i in it if i['cat']==gid]
    k=max(1,round(len(sel)/28));size=-(-len(sel)//k)
    for a in range(k):
        part=sel[a*size:(a+1)*size]
        if part: albums.append({'id':'e-'+gid+str(a+1),'n':[x+('' if k==1 else ' '+str(a+1)) for x in n],'items':part})
J=lambda o:json.dumps(o,ensure_ascii=False,separators=(',',':'))
open('emo_gen.js','w').write('const EMO='+J([[i['name'],i['nc'],i['rle']] for i in it])+';\n')
open('emo_names.js','w').write('const EMO_NAMES='+J({i['name']:[i['tr'],i['en'],i['de']] for i in it})+';\n')
open('emo_albums.js','w').write('const EMO_ALBUMS='+J(albums)+';\n')
print(len(it),'pictures,',len(albums),'albums')
