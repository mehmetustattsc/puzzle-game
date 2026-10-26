import json,re,collections,random
from PIL import Image,ImageDraw
PAL={'R':'#E53935','O':'#FB8C00','Y':'#FDD835','G':'#43A047','B':'#1E88E5','P':'#8E24AA','K':'#F06292','N':'#7B5136','W':'#F5F5F5','D':'#1E1E1E','C':'#26C6DA','M':'#A0182E','L':'#A5D63A','A':'#8FD3FF','V':'#B79CE6','T':'#00897B','E':'#F8BBD9','H':'#8EE3C3','I':'#FFCC99','J':'#FFF3A3','Q':'#757F8A','U':'#D7B98E'}
q=json.load(open('quant.json'))
ann={L:json.load(open(f'cldr/cldr-json/cldr-annotations-full/annotations/{L}/annotations.json'))['annotations']['annotations'] for L in ['tr','de','en']}
def nm(g,L):
    for k in [g,g.replace('️','')]:
        if k in ann[L] and 'tts' in ann[L][k]:return ann[L][k]['tts'][0]
DROPX=re.compile(r"o’clock$|-thirty$|quarter moon|crescent moon|gibbous|^new moon|mailbox|banknote|traffic light|envelope|e-mail|tray$|postbox|postal horn|ticket|credit card|chopsticks|spoon|fork and knife|amphora|^oden$|fish cake|moon cake|fortune cookie|canned food|takeout box|^salt$|^ice$|^mate$|baby bottle|cup with straw|pouring liquid|bellhop|construction|fuel pump|^wheel$|stop sign|railway track|oil drum|hourglass|stopwatch|timer clock|thermometer|motorway|derelict|^houses$|post office|love hotel|convenience store|department store|japanese|wedding|statue of liberty|^foggy$|night with stars|cityscape at dusk|sunrise over mountains|bridge at night|hot springs|barber pole|railway car|high-speed|bullet train|^metro$|light rail|^station$|monorail|mountain railway|tram car|oncoming|trolleybus|minibus|delivery truck|articulated lorry|auto rickshaw|bus stop|ring buoy|passenger ship|departure|arrival|^seat$|suspension railway|cableway|aerial tramway|closed umbrella|umbrella with rain|umbrella on ground|high voltage|^droplet$|jack-o-lantern|firecracker|sparkler|tanabata|pine decoration|carp streamer|wind chime|moon viewing|reminder ribbon|military|medal|flag in hole|direct hit|water pistol|playing cards|^joker$|mahjong|framed picture|^thread$|^knot$|necktie|briefs|thong sandal|lipstick|speaker|loudspeaker|megaphone|bell with slash|musical score|level slider|control knobs|studio microphone|with arrow|telephone receiver|^pager$|fax machine|battery|electric plug|desktop computer|^printer$|keyboard|computer mouse|trackball|disk$|^dvd$|abacus|movie camera|film|clapper board|videocassette|magnifying glass|diya lamp|notebook with|page with|^scroll$|page facing|newspaper|bookmark|^label$|receipt|card index|spiral|calendar|chart|clipboard|pushpin|paperclip|ruler|card file|file cabinet|wastebasket|locked|^old key$|^key$|hammer and|boomerang|carpentry saw|screwdriver|nut and bolt|^gear$|^clamp$|balance scale|^link$|broken chain|^chains$|^hook$|toolbox|^magnet$|^ladder$|alembic|test tube|petri dish|^dna$|microscope|telescope|satellite antenna|^door$|elevator|^mirror$|^window$|^bed$|couch and lamp|^chair$|^toilet$|plunger|^shower$|bathtub|mouse trap|lotion bottle|safety pin|^broom$|^basket$|roll of paper|^bucket$|^soap$|^bubbles$|toothbrush|^sponge$|fire extinguisher|shopping cart|placard|identification card|knocked-out|tropical drink|guide dog|service dog|^herb$|sheaf of rice|empty nest|^rock$|^wood$|^brick$|beverage box|bubble tea|^mosquito$|^fly$|cockroach|^worm$|microbe|^lungs$|anatomical heart|^brain$|^bone$|^tooth$|^mouth$|bikini|one-piece|^sari$|kimono|^shorts$|^socks$|^scarf$|^coat$|clutch bag|^purse$|hair pick|goggles|glasses|^memo$|black nib|rescue worker|slot machine|martial arts|safety vest|^hospital$|^bank$|^hotel$|^factory$|^school$|^package$|^satellite$|^bacon$|^gloves$|^handbag$|shopping bags|^jeans$|^t-shirt$|^dress$|lab coat|running shirt|ballet shoes|flat shoe|hiking boot|woman’s|man’s|^boot$|^sandal$|^cap$|helmet|prayer|^crown$|hat$|^ring$|^gem stone$|money bag|^coin$|identification|^pen$|fountain pen|^pencil$|^crayon$|paintbrush|^briefcase$|file folder|^scissors$|^hammer$|^axe$|^pick$|wrench|^shield$|^nut|^plug|^pager|mobile phone|^laptop$|^telephone$|^radio$|television|video camera|camera with flash|^candle$|^flashlight$|red paper lantern|notebook|closed book|^books$|green book|blue book|orange book|open book|ledger|^bell$|postal|^luggage$|^tent$|^stadium$|national park|^fountain$|^castle$|^cityscape$|^hut$|houses|^office building$|^classical building$|^building$|^moai$|^compass$|^clock$|^watch$|^anchor$|^stethoscope$|^bandage$|^dagger$|^water wave$|^fog$|^tornado$|^cyclone$|^comet$|^fire$|^high voltage$|^snowflake$|^umbrella$|^mantelpiece clock$|^alarm clock$|^chopsticks$|^hot beverage$|teacup|^teapot$|^jar$|^glass of milk$|^cup with straw$|^ice$|^bowl with spoon$|^plate$|^fork$|^knife$|^moon$|ogre|goblin|^imp$|devil|^pouting cat$|^weary cat$|^crying cat$|heart with arrow|heart with ribbon|sparkling heart|growing heart|revolving hearts|two hearts|heart decoration|heart exclamation|broken heart|mending heart|heart on fire|beating heart|grey heart|light blue heart",re.I)
cap=lambda s:s[:1].upper()+s[1:]
items=[];seen=set();rej=collections.Counter()
for e in q:
    n=e['name']
    if DROPX.search(n) or n in seen: rej['name']+=1;continue
    g=''.join(e['grid']);op=[c for c in g if c!='.'];N=len(op)
    if N<1600*0.15: rej['small']+=1;continue
    cnt=collections.Counter(op);big=[k for k,v in cnt.items() if v>=8];share=cnt.most_common(1)[0][1]/N
    if len(big)<2 or share>0.93: rej['flat']+=1;continue
    tr=nm(e['glyph'],'tr');de=nm(e['glyph'],'de');en=nm(e['glyph'],'en') or n
    if not tr or not de: rej['noname']+=1;continue
    seen.add(n);e.update(tr=cap(tr),de=cap(de),en=cap(en),nc=len([k for k,v in cnt.items() if v>=12]));items.append(e)
print(len(items),rej,collections.Counter(i['group'] for i in items))
PL=re.compile(r"flower|blossom|rose|hibiscus|sunflower|tulip|tree|cactus|shamrock|clover|leaf|bouquet|lotus|plant|maple|palm|hyacinth|seedling|coral|nest|rosette|mushroom",re.I)
SEA=re.compile(r"fish|whale|dolphin|shark|octopus|seal|shell|crab|lobster|shrimp|squid|oyster|jellyfish|blowfish|coral|turtle|otter",re.I)
BUG=re.compile(r"ant$|bee|beetle|bug|butterfly|snail|spider|cricket|scorpion|caterpillar|lady",re.I)
SKY=re.compile(r"sun|cloud|rainbow|snow|tornado|fog|wind|milky way|star|comet|moon|volcano|mountain|desert|island|beach|wave|fire|globe|world|earth|ringed",re.I)
VEH=re.compile(r"car|bus|train|tram|taxi|truck|airplane|helicopter|rocket|ship|boat|ferry|canoe|sailboat|motor|bicycle|scooter|tractor|ambulance|fire engine|police|vehicle|locomotive|parachute|ufo|saucer|skateboard",re.I)
def cat(i):
    g=i['group'];n=i['name']
    if g=='Animals & Nature':
        if PL.search(n):return 'plants'
        if SEA.search(n):return 'sea'
        if BUG.search(n):return 'bugs'
        return 'animals'
    if g=='Food & Drink':
        return 'fruit' if re.search(r"apple|pear|tangerine|lemon|banana|watermelon|grapes|strawberr|melon|cherr|peach|mango|pineapple|coconut|kiwi|tomato|olive|blueberr|avocado|eggplant|potato|carrot|corn|pepper|cucumber|leafy|broccoli|garlic|onion|peanut|bean|chestnut|ginger|pea pod|lime|mushroom",n,re.I) else 'food'
    if g=='Travel & Places': return 'sky' if SKY.search(n) else ('vehicles' if VEH.search(n) else 'places')
    if g=='Activities': return 'fun'
    if g in('Smileys & Emotion','Symbols'): return 'faces'
    return 'vehicles' if VEH.search(n) else 'things'
for i in items:
    i['cat']=cat(i);g=''.join(i['grid']);out=[];prev=None;run=0
    for ch in g+'\0':
        if ch==prev:run+=1;continue
        if prev is not None: out.append(prev+(str(run) if run>1 else ''))
        prev=ch;run=1
    i['rle']=''.join(out)
print(collections.Counter(i['cat'] for i in items),'bytes',sum(len(i['rle']) for i in items))
json.dump(items,open('final.json','w'),ensure_ascii=False)
def sheet(items,fn,res=24,cols=14):
    cs=res*4+8;rows=(len(items)+cols-1)//cols
    im=Image.new('RGB',(cols*cs,rows*cs),'#9CA3AD');d=ImageDraw.Draw(im)
    for idx,e in enumerate(items):
        ox=(idx%cols)*cs+4;oy=(idx//cols)*cs+4
        for y in range(res):
            for x in range(res):
                c=e['grid'][int((y+.5)*40/res)][int((x+.5)*40/res)]
                if c!='.':d.rectangle([ox+x*4,oy+y*4,ox+x*4+3,oy+y*4+3],fill=PAL[c])
    im.save(fn)
for c in ['animals','sea','bugs','plants','faces','things','fun','places']:
    sel=[i for i in items if i['cat']==c]
    sheet(sel,f'sh_{c}.png')
    print(c,len(sel),', '.join(i['name'] for i in sel))
