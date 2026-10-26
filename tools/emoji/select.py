# Step 1: pick candidate emoji from Microsoft Fluent Emoji (flat SVGs) -> cands.json
# Run inside tools/emoji/work after cloning (see README.md).
import json,glob,os,re,collections
words="""beer|wine|cocktail|sake|champagne|tumbler|whisky|bottle with popping cork|clinking|cigarette|smoking|dagger|pistol|bomb|bow and arrow|crossed swords|kitchen knife|axe|pill|syringe|drop of blood|mosque|church|synagogue|kaaba|hindu temple|shinto shrine|menorah|prayer beads|latin cross|orthodox cross|star and crescent|om|wheel of dharma|yin yang|place of worship|coffin|funeral urn|skull|skull and crossbones|pile of poo|razor|adhesive bandage|stethoscope|x-ray|crutch|wheelchair|white cane|headstone|nazar amulet|hamsa|moai|tokyo tower|map of japan|middle finger|star of David|dotted six-pointed star|atom symbol|peace symbol|radioactive|biohazard"""
BAD=re.compile(r'\b(?:'+words+r')\b',re.I)
GOOD_GROUPS={'Animals & Nature','Food & Drink','Activities','Travel & Places','Objects','Smileys & Emotion','Symbols'}
SMILE_OK=re.compile(r'heart|cat|robot|alien|ghost|sun|star-struck|smiling face with heart|grinning|partying|cowboy|nerd|disguised|zany|sleepy|hugging|money-mouth|clown',re.I)
out=[]
for m in sorted(glob.glob('fe/assets/*/metadata.json')):
    d=json.load(open(m));name=d.get('cldr') or d.get('tts');g=d.get('group')
    if g not in GOOD_GROUPS or BAD.search(name): continue
    if g in ('Smileys & Emotion','Symbols') and not SMILE_OK.search(name): continue
    if g=='Symbols' and re.search(r'suit|button|symbol|sign|mark',name):continue
    dirp=os.path.dirname(m);svgs=glob.glob(dirp+'/Flat/*.svg')+glob.glob(dirp+'/Default/Flat/*.svg')
    if svgs: out.append({'name':name,'group':g,'glyph':d.get('glyph'),'svg':svgs[0]})
json.dump(out,open('cands.json','w'),ensure_ascii=False)
print(len(out),collections.Counter(o['group'] for o in out))
