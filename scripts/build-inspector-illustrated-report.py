"""Local illustrated correction table; original captures remain unmodified."""
import base64,hashlib,json,mimetypes,re
from datetime import datetime
from html import escape as E
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'reference/inspector-revisions/2026-11-24'
OUT=ROOT/'outputs/inspector-revisions'
OUT.mkdir(parents=True,exist_ok=True)
report=json.loads((SOURCE/'consolidated-report.json').read_text(encoding='utf8'))
manifest=json.loads((SOURCE/'manifest.json').read_text(encoding='utf8'))
assets={}

def add(key,path,caption,origin):
 raw=path.read_bytes()
 assets[key]=dict(path=path.relative_to(ROOT).as_posix(),caption=caption,origin=origin,
  sha256=hashlib.sha256(raw).hexdigest(),data='data:'+mimetypes.guess_type(path.name)[0]+';base64,'+base64.b64encode(raw).decode('ascii'))

captions={
 1:'Capture groupée des remarques sur a, les propriétés et la voix. Plusieurs passages sont réunis dans cette capture.',
 2:'Identification fournie : 3AC semaine 3 VDP1, libellé V2.',
 3:'Extrait du script où le mot inférieur est entouré.',
 4:'Identification fournie : 3AC semaine 3 VDP2, libellé V2.',
 5:'Capture du vocabulaire périodique montrant pé – rio ; rattachement à N3 semaine 3 VDP3 confirmé par l’utilisateur le 25 novembre, passage à examiner.',
 6:'Identification fournie : 3AC semaine 3 VDP4, libellé V2.',
 7:'Flèche orange sous non périodique entourée dans l’objectif.',
 8:'Identification fournie : 1AC semaine 2 VDP4.',
 9:'Message demandant le signe + devant cinq, avec précision sur les timecodes.',
}
for item in manifest['assets']:
 path=SOURCE/item['savedName']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
 if path.suffix.lower()=='.png':
  n=int(path.name.split('-')[0]);add(f'S{n:02}',path,captions[n],item['originalName'])

docs={
 'D1':('Révision vidéo P1_Math_N3_SEM3_VDP1 (2).docx',[
  ('image1.png','Définition annotée : ou nul entouré.'),
  ('image2.png','Schéma mise au carré et racine carrée, à révéler progressivement.'),
  ('image3.png','Égalités √a = ? puis (?)² = a et leur flèche.'),
  ('image4.png','Propriété 1 : préambule Pour a ≥ 0 entouré.'),
  ('image5.png','Propriété 2 : préambule Pour a ≥ 0 entouré.')]),
 'D2':('Révision vidéo P1_Math_N3_SEM3_VDP2 (1).docx',[
  ('image1.png','Propriété de comparaison : formulation deux nombres positifs ou nuls entourée.')]),
 'D3':('Révision vidéo P1_Math_N3_SEM3_VDP3 (1).docx',[
  ('image1.png','Ellipse sur la fraction 225/10² et exposant répété en dessous.'),
  ('image2.png','Fraction 1/10³ et libellé Une fraction décimale.'),
  ('image3.png','Exemple −5/10⁰ et libellé Une fraction décimale.')]),
 'D4':('Révision vidéo P1_Math_N3_SEM3_VDP4 (1).docx',[
  ('image1.png','2,25 et libellé Une écriture décimale finie.'),
  ('image2.png','Capture de référence pour la taille des libellés autour de √7.'),
  ('image3.png','Propriété sur les rationnels, les irrationnels et les réels.'),
  ('image4.png','Propriété 3 : premier sens de la correspondance nombre réel et point.'),
  ('image5.png','Propriété 3 : phrase de réciproque entourée.')]),
 'D5':('Revision_Video_P1_MATHS_N1_SEM3_VDP1 (1) (1).docx',[
  ('image1.jpeg','Capture initiale : opérateur + rouge dans l’expression (−6) + (+4) + (−3).')]),
}
for prefix,(name,pics) in docs.items():
 with ZipFile(SOURCE/name) as z:
  for i,(filename,caption) in enumerate(pics,1):
   path=SOURCE/'docx-media'/Path(name).stem/filename
   assert path.read_bytes()==z.read('word/media/'+filename)
   add(prefix+str(i),path,caption,name+' · '+filename)
assert len(assets)==24
comparison=ROOT/'reference/inspector-revisions/2026-11-25/n3-sem3-vdp1-notation-sentence.png'
if comparison.exists():
 evidence=json.loads((ROOT/'outputs/n3-sem3-v6/vdp1/correction-evidence.json').read_text(encoding='utf8'))
 assert hashlib.sha256(comparison.read_bytes()).hexdigest()==evidence['sha256']
 add('U01',comparison,'Comparaison fournie le 25 novembre : phrase complète dans le storyboard à gauche, mots manquants dans la V5 à droite. État avant la correction V6.','Capture utilisateur du 25 novembre · phrase de notation')
comparison=SOURCE/'user-comparisons/VDP4-propriete3-comparison.png'
if comparison.exists():
 evidence=json.loads((ROOT/'outputs/n3-sem3-v6/vdp4/comparison-evidence.json').read_text(encoding='utf8'))
 assert hashlib.sha256(comparison.read_bytes()).hexdigest()==evidence['sha256']
 add('U02',comparison,'Comparaison du 26 novembre : texte fourni à gauche et deux formulations approuvées de la V5 à droite. L’utilisateur demande ensuite la reprise exacte du storyboard et de sa fiche, appliquée dans la V6.','Capture utilisateur du 26 novembre · propriété 3 VDP4')
comparison=SOURCE/'user-comparisons/VDP4-limitee-comparison.png'
if comparison.exists():
 evidence=json.loads((ROOT/'outputs/n3-sem3-v7/vdp4/comparison-evidence.json').read_text(encoding='utf8'))
 assert hashlib.sha256(comparison.read_bytes()).hexdigest()==evidence['sha256']
 add('U03',comparison,'Comparaison du 26 novembre avant V7 : limitée dans le storyboard, finie dans la vidéo suivant la fiche. L’utilisateur choisit ensuite explicitement limitée, comme le storyboard et la voix.','Capture utilisateur du 26 novembre · limitée/finie VDP4')

image_map={
 'P1_MATHS_N3_SEM3_VDP1':{1:['D11'],3:['D12'],4:['D13'],5:['D14','D15'],7:['D12'],8:['S01']},
 'P1_MATHS_N3_SEM3_VDP2':{1:['D21'],3:['S03']},
 'P1_MATHS_N3_SEM3_VDP3':{3:['D31'],4:['D32'],6:['D33'],9:['S05']},
 'P1_MATHS_N3_SEM3_VDP4':{2:['D41'],3:['D42'],7:['D43'],8:['D44'],9:['D45'],10:['S07']},
 'P1_MATHS_N1_SEM3_VDP1':{1:['D51']},
 'P1_MATHS_N1_SEM2_VDP4':{0:['S09']},
}
if 'U01' in assets:image_map['P1_MATHS_N3_SEM3_VDP1'][2]=['U01']
if 'U02' in assets:
 image_map['P1_MATHS_N3_SEM3_VDP4'][8].append('U02')
 image_map['P1_MATHS_N3_SEM3_VDP4'][9].append('U02')
if 'U03' in assets:image_map['P1_MATHS_N3_SEM3_VDP4'][2].append('U03')
context={'P1_MATHS_N3_SEM3_VDP1':['S02'],'P1_MATHS_N3_SEM3_VDP2':['S04'],
         'P1_MATHS_N3_SEM3_VDP4':['S06'],'P1_MATHS_N1_SEM2_VDP4':['S08']}
clarify={('P1_MATHS_N3_SEM3_VDP1',8),
         ('P1_MATHS_N3_SEM3_VDP4',8),('P1_MATHS_N3_SEM3_VDP4',9),('P1_MATHS_N3_SEM3_VDP4',10)}
ordered=['P1_MATHS_N1_SEM3_VDP1','P1_MATHS_N3_SEM3_VDP1','P1_MATHS_N3_SEM3_VDP2',
         'P1_MATHS_N3_SEM3_VDP3','P1_MATHS_N3_SEM3_VDP4','P1_MATHS_N1_SEM2_VDP4']
groups={g['video']:g for g in report['groups']}
latest=next((ROOT/f'outputs/n1-sem3-vdp1-v{n}/delivery.json' for n in [5,4,3] if (ROOT/f'outputs/n1-sem3-vdp1-v{n}/delivery.json').exists()))
delivery=json.loads(latest.read_text(encoding='utf8'))
version=re.search(r'_V(\d+)\.mp4$',delivery['filename'])[1]
deliveries={'P1_MATHS_N1_SEM3_VDP1':delivery}
for n in [6,5]:
 n3_receipt=ROOT/f'outputs/n3-sem3-v{n}/vdp1/delivery.json'
 if n3_receipt.exists():
  deliveries['P1_MATHS_N3_SEM3_VDP1']=json.loads(n3_receipt.read_text(encoding='utf8'));break
vdp2_receipt=ROOT/'outputs/n3-sem3-v5/vdp2/delivery.json'
if vdp2_receipt.exists():deliveries['P1_MATHS_N3_SEM3_VDP2']=json.loads(vdp2_receipt.read_text(encoding='utf8'))
for n in [6,5]:
 vdp3_receipt=ROOT/f'outputs/n3-sem3-v{n}/vdp3/delivery.json'
 if vdp3_receipt.exists():
  deliveries['P1_MATHS_N3_SEM3_VDP3']=json.loads(vdp3_receipt.read_text(encoding='utf8'));break
for n in [7,6,5]:
 vdp4_receipt=ROOT/f'outputs/n3-sem3-v{n}/vdp4/delivery.json'
 if vdp4_receipt.exists():
  deliveries['P1_MATHS_N3_SEM3_VDP4']=json.loads(vdp4_receipt.read_text(encoding='utf8'));break

n1_sem2_receipt=ROOT/'outputs/n1-sem2-vdp4-v2/delivery.json'
if n1_sem2_receipt.exists():deliveries['P1_MATHS_N1_SEM2_VDP4']=json.loads(n1_sem2_receipt.read_text(encoding='utf8'))

def delivered_version(name):
 return re.search(r'_V(\d+)\.mp4$',deliveries[name]['filename'])[1] if name in deliveries else ''

def item_state(name,i,item):
 if name in deliveries and item.get('status','').startswith(('corrected-and-verified','resolved-by-user-source-choice')):return 'done'
 return 'clarify' if (name,i) in clarify else 'pending'
def thumb(key):
 a=assets[key]
 return '<figure><a href="#image-'+key+'"><img loading="lazy" src="'+a['data']+'" alt="'+E(a['caption'],quote=True)+'"></a><figcaption><strong>'+key+'</strong> · '+E(a['caption'])+'</figcaption></figure>'

rows=[];sections=[];counter=0
for name in ordered:
 group=groups[name];completed=sum(item_state(name,i,item)=='done' for i,item in enumerate(group['items']))
 done=completed==len(group['items']);v=delivered_version(name)
 heading=name.replace('P1_MATHS_','').replace('_',' · ')
 content='<section class="video-block" id="'+name+'"><h2>'+E(heading)+'</h2><p class="filename">'+name+'</p>'
 if completed:content+='<p>'+str(completed)+' point(s) de l’inspecteur traité(s) dans la V'+v+'. '+str(len(group['items'])-completed)+' point(s) restant(s) à contrôler ou préciser. Les images ci-dessous sont les pièces initiales, avant correction.</p>'
 else:content+='<p>Demandes relevées dans les pièces reçues. Comparaison avec la vidéo courante encore en attente ; un libellé V2 dans une capture ne prouve pas la présence du défaut dans une V4.</p>'
 if name=='P1_MATHS_N1_SEM2_VDP4' and v=='2':content+='<p><strong>Correction ciblée · V2 :</strong> signe + ajouté devant le cinq positif dans l’exemple et dans sa conclusion. Les deux valeurs absolues restent 5. La capture cite 01:25–02:25 ; la vidéo actuelle dure 85,077 s, les passages sont repérés par leur contenu vers 00:23–00:41. Les six voix et la piste AAC entière sont identiques à la première version.</p>'
 if name=='P1_MATHS_N3_SEM3_VDP3' and v=='6':content+='<p><strong>Correction complémentaire utilisateur · V6 :</strong> suppression de l’exemple précédent ajouté sous la fraction de la diapositive 17. Seule cette ligne est retirée ; les autres visuels, les dix pistes audio et les durées sont conservés. Les contrôles de la V5 ne détectaient pas cet ajout hors de son passage source ; le nouveau contrôle refuse sa réintroduction.</p>'
 if name=='P1_MATHS_N3_SEM3_VDP4' and v=='5':content+='<p><strong>Décisions utilisateur du 26 novembre :</strong> objectif repris de la voix source, sans énumération ajoutée ; chiffres exacts de π conservés ; deux formulations sur l’abscisse et la réciproque approuvées précisément. La capture de flèche sous « non périodique » ne correspond pas à l’objectif VDP4 actuel : attribution et changement attendu restent à préciser, sans modification de cette remarque.</p>'
 if name=='P1_MATHS_N3_SEM3_VDP4' and v=='6':content+='<p><strong>Dernière décision utilisateur · V6 :</strong> propriété 3 reprise mot pour mot du storyboard et de la fiche fournie ; ce choix remplace les deux formulations proposées et approuvées auparavant. La coupure signalée à 00:26–00:27 venait d’une pause artificielle de 0,63 seconde insérée dans un son : elle est supprimée, en conservant la prise originale du vocabulaire. Douze autres scènes sont identiques ; les décisions sur l’objectif et les chiffres de π sont conservées. La remarque de flèche non attribuée reste en attente.</p>'
 if name=='P1_MATHS_N3_SEM3_VDP4' and v=='7':content+='<p><strong>Dernière décision utilisateur · V7 :</strong> afficher limitée, comme le storyboard et la voix, plutôt que finie demandé dans la fiche initiale. Seuls ce mot visible et sa réserve de mise en page sont modifiés. La piste AAC entière est identique à celle de la V6 : propriété 3 selon le texte fourni et réparation de la coupure vocale conservées. La remarque de flèche non attribuée reste en attente.</p>'
 if name in context:content+='<div class="context-gallery">'+''.join(thumb(k) for k in context[name])+'</div>'
 content+='<div class="table-scroll"><table><thead><tr><th>Nº</th><th>Repère fourni</th><th>Correction demandée</th><th>Image fournie</th><th>État actuel</th></tr></thead><tbody>'
 for i,item in enumerate(group['items']):
  counter+=1;keys=image_map.get(name,{}).get(i,[]);state=item_state(name,i,item)
  label='Traité · V'+v if state=='done' else 'À préciser / valider' if state=='clarify' else 'À contrôler / traiter'
  if state=='done' and item.get('status','').startswith('resolved-by-user-source-choice'):label='Source conservée · V'+v
  note=item.get('verificationNote','')
  if name=='P1_MATHS_N3_SEM3_VDP4' and i in [8,9] and state!='done':note='Demande de la fiche à valider avec l’inspecteur ; ne pas appliquer une formulation mathématiquement ambiguë ni la réécrire sans décision.'
  pictures=''.join(thumb(k) for k in keys) if keys else '<span class="muted">Aucune image spécifique jointe à ce point.</span>'
  rowid='correction-'+str(counter)
  request=E(item['request'])+('<p class="row-note">'+E(note)+'</p>' if note else '')
  content+='<tr id="'+rowid+'" data-state="'+state+'"><td class="number">'+str(counter).zfill(2)+'</td><td class="time">'+E(item['timecode'])+'</td><td>'+request+'</td><td class="pictures">'+pictures+'</td><td><span class="status '+state+'">'+E(label)+'</span></td></tr>'
  rows.append(dict(number=counter,video=name,timecode=item['timecode'],request=item['request'],status=state,statusLabel=label,images=keys,qualification=note))
 content+='</tbody></table></div></section>';sections.append(content)
assert counter==41
used={k for row in rows for k in row['images']}|{k for values in context.values() for k in values};assert used==set(assets)
summary=[]
for name in ordered:
 group=groups[name];completed=sum(item_state(name,i,item)=='done' for i,item in enumerate(group['items']))
 summary.append('<tr><td><a href="#'+name+'">'+E(name.replace('P1_MATHS_','').replace('_',' · '))+'</a></td><td class="number">'+str(len(group['items']))+'</td><td>'+(str(completed)+' point(s) traité(s) · version livrée V'+delivered_version(name)+' ; '+str(len(group['items'])-completed)+' à préciser/traiter' if completed else 'En attente de contrôle / précision')+'</td></tr>')
done_count=sum(r['status']=='done' for r in rows)
clarify_count=sum(r['status']=='clarify' for r in rows)
now=datetime.now(ZoneInfo('Africa/Casablanca')).strftime('%d/%m/%Y %H:%M')
css='''*{box-sizing:border-box}body{margin:0;background:#f3f6f9;color:#24344d;font:16px/1.55 Arial,sans-serif}main{max-width:1340px;margin:28px auto;background:white;padding:32px;border-radius:14px}h1{font-size:29px;line-height:1.2;margin:8px 0 16px}h2{font-size:23px;margin:30px 0 5px}.brand{color:#059c87;font-weight:bold;letter-spacing:.12em}.muted,.filename{color:#607087;font-size:13px}.cards{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}.cards div{flex:1;min-width:180px;border:1px solid #dce6eb;border-top:4px solid #0dbba1;padding:14px;border-radius:8px}.cards strong{display:block;font-size:28px}.notice{border-left:4px solid #d7a52b;background:#fff9e9;padding:14px 18px;margin:20px 0}.table-scroll{overflow-x:auto}table{width:100%;border-collapse:collapse;margin:16px 0;font-size:14px}thead{background:#263956;color:white}th,td{padding:13px;border:1px solid #d8e1e9;text-align:left;vertical-align:middle}tbody tr:nth-child(even){background:#f8fafb}.video-block table{min-width:920px;table-layout:fixed}.video-block th:nth-child(1){width:5%}.video-block th:nth-child(2){width:14%}.video-block th:nth-child(3){width:32%}.video-block th:nth-child(4){width:34%}.video-block th:nth-child(5){width:15%}.number{text-align:center;font-variant-numeric:tabular-nums}.time{font-weight:bold;font-size:13px}.status{display:inline-block;padding:5px 9px;border-radius:6px;font-size:12px;font-weight:bold}.status.done{background:#e3f6ec;color:#17643b}.status.pending{background:#e9f0fa;color:#365c91}.status.clarify{background:#fff0ce;color:#885b00}figure{margin:8px 0}figure img{max-width:100%;max-height:190px;object-fit:contain;background:white;border:1px solid #dce6eb;border-radius:5px}figcaption{font-size:12px;color:#607087;line-height:1.4}.row-note{font-size:12px;color:#885b00;margin:10px 0 0}.context-gallery{display:flex;gap:12px;flex-wrap:wrap}.context-gallery figure{max-width:480px}.context-gallery img{max-height:100px}.filters{position:sticky;top:0;background:white;padding:12px 0;border-bottom:1px solid #d8e1e9;display:flex;gap:8px;flex-wrap:wrap;z-index:2}.filters button,.filters input{font:inherit;border:1px solid #c9d7e1;border-radius:6px;padding:8px 11px;background:white}.filters button{cursor:pointer}.filters button.active{background:#263956;color:white}.filters input{flex:1;min-width:200px}a{color:#006d9f}.lightbox{display:none;position:fixed;inset:0;background:rgba(14,23,35,.96);z-index:10;padding:30px;align-items:center;justify-content:center;flex-direction:column}.lightbox:target{display:flex}.lightbox img{max-width:95vw;max-height:80vh;object-fit:contain;background:white}.lightbox p{color:white;max-width:1000px;font-size:14px}.lightbox .close{position:absolute;top:10px;right:22px;font-size:28px;color:white;text-decoration:none}.gallery{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.gallery figure{border:1px solid #dce6eb;padding:12px;border-radius:7px}.gallery img{width:100%;height:150px;object-fit:contain}.source-name{font-size:11px;overflow-wrap:anywhere;color:#607087}footer{font-size:12px;color:#607087;margin-top:28px}@media(max-width:700px){main{margin:0;padding:18px;border-radius:0}.gallery{grid-template-columns:1fr}h1{font-size:25px}}@media print{body{background:white}main{margin:0;padding:0;max-width:none}.filters,.lightbox{display:none!important}thead{display:table-header-group}tr,figure{break-inside:avoid}h2{break-after:avoid}.video-block table{min-width:0;font-size:11px}.video-block th,.video-block td{padding:7px}.video-block figure img{max-height:150px}.gallery{grid-template-columns:repeat(2,1fr)}a{color:inherit}}'''
html='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Digital Lab Tableau des corrections illustré</title><style>'+css+'</style></head><body><main id="top"><div class="brand">DIGITAL LAB</div><h1>Tableau des corrections avec les images fournies</h1><p>Pièces reçues le 24 novembre 2026 · Situation présentée le '+now+' · Heure de Casablanca.</p><p>Ce tableau reprend les <strong>41 points regroupés pour six vidéos</strong>. Il présente les images reçues à côté des remarques correspondantes, sans les modifier. Les mentions « à préciser » ne constituent pas une nouvelle correction inventée.</p><div class="cards"><div><strong>6</strong>vidéos concernées</div><div><strong>41</strong>points regroupés</div><div><strong>'+str(done_count)+'</strong>points inspecteur traités</div><div><strong>'+str(41-done_count)+'</strong>points en attente, dont '+str(clarify_count)+' à préciser</div><div><strong>'+str(len(assets))+'</strong>images originales intégrées</div></div><div class="notice"><strong>Les captures montrent les remarques et les états initiaux.</strong> Elles ne sont pas des captures de validation de la vidéo corrigée. Certaines portent un libellé V2 ; les autres versions courantes restent à confronter à ces pièces. Cliquer sur une image pour l’agrandir, puis sur × pour revenir au tableau.</div>'
html+='<table><thead><tr><th>Vidéo</th><th>Points</th><th>État</th></tr></thead><tbody>'+''.join(summary)+'</tbody></table><p><a href="'+E(delivery['link'],quote=True)+'">Ouvrir la vidéo 1AC semaine 3 VDP1 livrée en V'+version+'</a>.</p>'
html+='<p>'+''.join('<a href="'+E(d['link'],quote=True)+'">'+E(n.replace('P1_MATHS_','').replace('_',' · '))+' · V'+delivered_version(n)+'</a> · ' for n,d in deliveries.items())+'</p>'
html+='<div class="filters"><button class="active" data-filter="all">Tous les points</button><button data-filter="pending">À traiter</button><button data-filter="clarify">À préciser</button><button data-filter="done">Traités</button><input id="search" type="search" placeholder="Rechercher une vidéo, un mot ou un timecode" aria-label="Rechercher dans le tableau"></div><p id="count" class="muted">41 points affichés.</p>'+''.join(sections)
html+='<h2>Consignes communes et remarques postérieures</h2><ul>'+''.join('<li>'+E(t)+'</li>' for t in report['transversal'])+'</ul><p><strong>Règles utilisateur :</strong> voix off et contenu du storyboard intouchables, sauf correction précise explicitement demandée ou approuvée. Le vocabulaire doit être généré avec la voix principale de la vidéo ; aucun clip ou son du PPT ne doit être réutilisé. Pour les mots français, l’utilisateur demande un accent français.</p><p>Pour la VDP1 de 1AC semaine 3, le script a été restauré en V3 et le vocabulaire natif créé en V4. Pour la VDP1 de 3AC semaine 3, la V5 restaure le script source et génère le vocabulaire natif avec Soukaina ; la V6 rétablit ensuite la phrase de notation complète à l’écran, sans changer l’audio. La dernière version livrée indiquée ci-dessus provient du reçu de livraison local, et non du libellé visible dans les anciennes captures.</p>'
html+='<h2>Toutes les pièces visuelles fournies</h2><p>Les neuf captures initiales et les quinze images intégrées aux cinq DOCX sont conservées ci-dessous, ainsi que les comparaisons utilisateur des 25 et 26 novembre lorsqu’elles sont disponibles. Une même illustration peut servir à plusieurs lignes quand la fiche la réutilise.</p><div class="gallery">'+''.join('<div>'+thumb(k)+'<span class="source-name">'+E(a['origin'])+'</span></div>' for k,a in assets.items())+'</div><footer>Rapport local illustré. Les documents et captures restent dans les dossiers privés du projet, hors compétences et GitHub. Aucune vidéo, voix, cellule Google ou donnée de production n’est modifiée par la génération de ce tableau.</footer></main>'
for key,a in assets.items():html+='<div class="lightbox" id="image-'+key+'" role="dialog" aria-label="'+E(a['caption'],quote=True)+'"><a class="close" href="#top" aria-label="Fermer">×</a><img src="'+a['data']+'" alt="'+E(a['caption'],quote=True)+'"><p><strong>'+key+'</strong> · '+E(a['caption'])+'<br>'+E(a['origin'])+'</p></div>'
html+='''<script>(()=>{let state='all';const search=document.getElementById('search');const normalize=s=>s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');function apply(){const query=normalize(search.value);let total=0;document.querySelectorAll('.video-block').forEach(section=>{let count=0;section.querySelectorAll('tbody tr[data-state]').forEach(row=>{const visible=(state==='all'||row.dataset.state===state)&&(!query||normalize(section.querySelector('.filename').textContent+' '+row.textContent).includes(query));row.hidden=!visible;if(visible)count++});section.hidden=count===0;total+=count});document.getElementById('count').textContent=total+' point(s) affiché(s).'}document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{state=button.dataset.filter;document.querySelectorAll('[data-filter]').forEach(b=>b.classList.toggle('active',b===button));apply()}));search.addEventListener('input',apply)})();</script></body></html>'''
HTMLParser().feed(html)
assert html.count('data-state=')==41 and html.count('<tr')==html.count('</tr>')
assert len({a['sha256'] for a in assets.values()})==len(assets)
path=OUT/'Tableau-corrections-avec-images.html';path.write_text(html,encoding='utf8')
write_assets={k:{f:v for f,v in a.items() if f!='data'} for k,a in assets.items()}
(OUT/'tableau-corrections-illustre.json').write_text(json.dumps(dict(updatedAt=now,rows=rows,assets=write_assets,latestDeliveredVersion=int(version),deliveredVersions={n:int(delivered_version(n)) for n in deliveries},scope='Original captures as evidence of requests, not evidence of remaining defects in current videos'),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('Illustrated report:',path)
print('41 rows, '+str(len(assets))+' unmodified original images, 6 videos; latest delivered versions: '+str({n:delivered_version(n) for n in deliveries}))
