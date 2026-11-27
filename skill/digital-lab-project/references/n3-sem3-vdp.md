# 3AC · Semaine 3 · Quatre VDP

Production à partir de l’onglet **P1 / Semaine 3** de « MATH College Digital Lab Intern ». Les quatre PowerPoint d’origine ont été récupérés depuis le dossier de chaque fichier dans Drive, puis examinés en OOXML et en aperçu PowerPoint. Les sources et les preuves d’inspection restent locales dans `reference/n3-sem3`. Le nom `P1_MATHS_N3_SEM3_VDP*.pptx` fait foi pour la semaine lorsque la colonne de suivi affiche S1.

| VDP | Objectif | Diapositives | Séquences | Storyboard | Version 1 |
| --- | --- | ---: | ---: | --- | --- |
| 1 | Reconnaître la racine carrée d’un nombre positif | 30 | 9 | F8 | K8 |
| 2 | Comparer les racines carrées des nombres positifs | 18 | 6 | F15 | K15 |
| 3 | Distinguer les écritures décimales illimitées périodiques et non périodiques | 31 | 10 | F22 | K22 |
| 4 | Distinguer rationnels, irrationnels et réels | 47 | 14 | F29 | K29 |

## Adaptations des storyboards

- Les deux VDP sur les racines précisent « positif ou nul » et distinguent `(√a)²` de `√(a²)`. Les exemples erronés restent signalés et la correction de `√((-5)²)` aboutit à 5. VDP2 montre `5 < 11` et son image par la racine carrée, puis le cas des radicandes négatifs dans ℝ.
- VDP3 corrige la voix du plan 18, qui reprenait l’exemple précédent, en lisant `−5 / 10⁰ = −5`. Le passage par 225 avant le déplacement de la virgule apparaît comme un repère de travail, sans signe égal. Le nombre 2,985 est lu chiffre par chiffre après la virgule et la conversion conserve les trois décimales. La périodicité est définie par une répétition indéfinie à partir d’un certain rang.
- VDP4 rétablit la vraie réciproque au plan 40. À chaque point de la droite graduée correspond une unique abscisse réelle. Le point M se place à √2 sur une droite à échelle constante. Les décimales de √7, √2 et π affichent les chiffres du développement dans l’ordre, suivis de points de suspension. Le bloc 714285 est marqué pour 45/63.
- Les éléments pédagogiques sont reconstruits dans la charte. KaTeX compose les radicaux, puissances, fractions et accolades. Les bandes de réalisation restent hors image. Les objectifs reprennent le bandeau cible et les flèches verticales de la charte. Le vocabulaire révèle les syllabes puis rejoint le mot. Sur les deux objectifs bilingues, la voix prononce une translittération et la notation du storyboard apparaît en arabe.

## Voix et reproduction

Les 39 séquences emploient Google Kore. Les modèles disponibles ont été vérifiés. Après le quota quotidien de Flash-Lite, les répliques ont été groupées par leçon et par lots de 122 mots au plus pour Flash TTS. Le découpage s’appuie sur l’alignement des frontières entre séquences. Une transcription locale indépendante a repéré un ajout après la première définition de VDP4. Il a été retiré dans un intervalle calme, puis la séquence a été alignée et transcrite de nouveau. La lecture de 2,985 et la synthèse orale de VDP4 ont été réenregistrées et contrôlées. Le contrôle indépendant est distinct de l’alignement MMS_FA.

Avec les enregistrements mis en cache, utiliser les timelines `src/video/n3-sem3-vdp1-lesson.json` à `src/video/n3-sem3-vdp4-lesson.json`.

```powershell
npm run render:storyboards -- --stills --key-frames week-three
npm run render:storyboards -- week-three
python -X utf8 scripts/verify-storyboard-batch.py week-three
```

Pour une mise à jour de la narration, préparer `scripts/prepare-n3-sem3.py`, générer les WAV Gemini compatibles ou utiliser `scripts/batch-vdp-speech.py prepare`, puis générer, aligner et découper les lots. Aligner le plan complet avec `scripts/align-n3.py src/video/n3-sem3-plan.json`, puis recréer les pauses et les timelines.

```powershell
python -X utf8 scripts/pace-n3.py --plan src/video/n3-sem3-plan.json --audio-dir n3-sem3-paced --output src/video/n3-sem3-paced-plan.json
python -X utf8 scripts/prepare-n3-sem3.py --timeline
```



## Livraison vérifiée le 16 novembre 2026

Les fichiers `P1_MATHS_N3_SEM3_VDP1.mp4` à `P1_MATHS_N3_SEM3_VDP4.mp4` ont été déposés dans « Livrable video / 3AC / Semaine 3 ». Chaque lien vidéo a été vérifié dans la bonne ligne « Version 1 » après rechargement du tableau, puis comparé à l’export de l’onglet. Les liens sont conservés localement dans `outputs/n3-sem3/delivery.json`.

Les quatre MP4, leurs timelines éditables, les rapports et les images sont dans `outputs/n3-sem3/vdp1` à `outputs/n3-sem3/vdp4`. Les durées sont 162,048 s, 93,568 s, 167,403 s et 226,603 s. Les quatre exports H.264/AAC 1080p à 30 i/s ont passé le décodage intégral. Le contrôle détecte et distingue les fondus sur le noir de 0,1 s demandés dans les storyboards. Il a extrait 174 images distinctes de l’encodage. Les captures aux repères clés, les égalités, la période 714285 et la position de √2 ont été revues. La vérification PCM confirme 27,96 s de pauses insérées entre les idées. La compilation Next.js, les 18 tests unitaires, le test du lecteur sur ordinateur et mobile et la vérification des 180 chemins audio ont réussi.

Pour le dépôt du lot, le sélecteur natif de Windows a accepté les fichiers lorsque Brave était maximisé. Après dépôt, les identifiants des lignes Drive ont permis de contrôler les liens avant de coller dans les cellules Version 1. La vérification de l’état « Enregistré dans Drive » et celle après rechargement ont confirmé les quatre écritures.


## Version 2 de la semaine 3

Les quatre VDP ont été réencodées avec la voix ElevenLabs Soukaina et lues en contrôle technique. Le navigateur a confirmé le dépôt dans « Livrable video / 3AC / Semaine 3 » et les liens en L8, L15, L22 et L29 après rechargement au moment de la livraison. Les 39 entrées de scène encodées concordent avec l’audio de la nouvelle voix. Le retour de l’utilisateur indique que le résultat lui paraît robotique et que la prononciation arabe doit être corrigée. Le contrôle indépendant précédent avait notamment reconnu « كارين » à la place de « قارن » dans la VDP2. La vérification technique de la piste constitue un contrôle distinct de la qualité de la diction.

## Essais de voix bilingues

L’utilisateur a choisi l’arabe standard (الفصحى) et demande une voix française moins robotique. Deux essais Soukaina ont été préparés pour recueillir son avis. Le français (9,59 s) utilise Eleven v4, la langue fr, une vitesse de 0,94, une stabilité de 0,45 et une pause de 0,65 s entre les deux idées. L’arabe (2,38 s) utilise Eleven Flash v2.5 avec la langue ar sur deux clips séparés, « قَارِنْ » puis « أَتَعَرَّفْ ». La reconnaissance locale indépendante a retrouvé ces deux mots ensemble et isolément, ainsi que les nombres et la conclusion de l’exemple français. Le 16 novembre 2026, l’utilisateur a validé les deux essais à l’écoute. Ils servent de référence pour la prochaine production.

Les MP3 et le rapport sont dans `outputs/voice-audition/`. Le plan d’essai se trouve dans `reference/n3-sem3/voice-audition/`. Le script ElevenLabs prend les paramètres facultatifs `languageCode`, `speed` et `stability` pour chaque clip. Les valeurs par défaut des enregistrements précédents restent compatibles avec leurs reçus.

## Reproduire la révision bilingue V3

Le plan reprend les répliques et la composition de la V2 pour les quatre leçons. Le français est généré en langue fr et les deux prises arabes de l’essai sont reprises dans les objectifs VDP1 et VDP2, avec 0,30 s de silence de part et d’autre de l’insertion. La mise en rythme vise 0,65 s entre les idées et réutilise les silences naturels. Les repères d’apparition sont recalculés à partir du PCM final.

```powershell
python -X utf8 scripts/prepare-n3-sem3-bilingual.py prepare
$env:ELEVENLABS_VOICE_ID = '05Y5uLueU3x8LrkGHu0H'
$env:ELEVENLABS_MODEL = 'eleven_v4'
node scripts/elevenlabs-tts.mjs public/n3-sem3-elevenlabs-bilingual/french-plan.json
python -X utf8 scripts/prepare-n3-sem3-bilingual.py assemble
python -X utf8 scripts/align-n3.py src/video/n3-sem3-bilingual-plan.json
python -X utf8 scripts/pace-n3.py --plan src/video/n3-sem3-bilingual-plan.json --audio-dir n3-sem3-elevenlabs-bilingual-paced --output src/video/n3-sem3-bilingual-paced-plan.json --gap-seconds 0.65
python -X utf8 scripts/prepare-n3-sem3-bilingual.py timeline
npm run render:storyboards -- week-three-v3
python -X utf8 scripts/verify-storyboard-batch.py week-three-v3
python -X utf8 scripts/check-n3-sem3-bilingual.py 1 2 3 4
```

Pour un nouveau rendu avec les prises et les timelines en cache, lancer les trois dernières commandes. Les timelines de chaque VDP sont livrées avec leurs MP4. La commande de vérification compare les données visuelles et les répliques à la V2 et contrôle le signal audio réellement encodé. Pour les mots arabes, elle compare aussi le PCM inséré à l’enregistrement de référence. La reconnaissance en arabe sur l’extrait encodé s’effectue séparément.

Les V3 produites se trouvent dans `outputs/n3-sem3-v3/vdp1` à `outputs/n3-sem3-v3/vdp4`. Durées MP4 148,437 s, 91,904 s, 158,208 s et 217,387 s. Les 39 séquences et les 126 diapositives ont été contrôlées. Les quatre MP4 sont en 1080p30 H.264/AAC, avec décodage intégral réussi et sans noir inattendu. La mise en rythme a inséré 4,67 s de pauses supplémentaires dans les silences. La reconnaissance locale des deux extraits arabes encodés retrouve « أتعرف » et « قارن ». Les deux passages du numérateur 2985 dans VDP3 ont été confirmés en isolant les extraits. Pour « comparer », la reconnaissance ne distingue pas les syllabes isolées et le contrôle d’énergie confirme la présence d’un signal dans chacun des trois segments. Les preuves restent auprès des exports ou dans la référence locale.

Les quatre V3 sont en ligne dans « Livrable video / 3AC / Semaine 3 » via les API Google. Les liens en K8, K15, K22 et K29 ouvraient les V2 et ouvrent maintenant les V3 sous les mêmes identifiants. La lecture après envoi a confirmé les quatre empreintes et les quatre noms de fichiers V3. La mise à jour a utilisé `revise --link-version 1 --version 3`.

## V4 · Révision des quatre VDP de 3AC, semaine 3

Les quatre fiches de révision DOCX ont été confrontées aux scènes déjà livrées. Les timecodes de ces fiches servent de repères dans le montage relu. Les repères V4 sont recalés sur la voix effectivement encodée.

- **VDP1.** Le bandeau explique « Reconnaître, c’est savoir ». La notation √a entre à 31,03 s et sa lecture à 33,50 s. Le schéma déroule √a, la flèche rouge, a et la flèche bleue à 36,23 s, 38,00 s, 39,60 s et 40,40 s. Le schéma se reconstruit également en synthèse. L’exemple révèle √a = ?, ⇒ et (?)² = a à 61,57 s, 63,20 s et 66,03 s.
- **VDP2.** La voix dit « Comparer, c’est utiliser l’un des symboles, supérieur à ou inférieur à ». La condition et la conclusion bleues apparaissent séparément à 36,60 s et 39,43 s. Les deux VDP utilisent un repère textuel « Faux » dans les vérifications. La narration de VDP2 explique qu’un radicande doit être positif ou nul, ce qui inclut zéro et exclut l’exemple négatif. La répétition a été retirée et les accents visuels du vocabulaire suivent les mots.
- **VDP3.** Définition et propriété en noir, avec révélations séparées. La fraction s’affiche avant son libellé. Le dénominateur entier puis l’exposant sont entourés à 63,43 s et 72,60 s, sans chiffre 2 dupliqué. Les égalités de 1/10³ et 225/10² sont reprises sur deux lignes avec des signes égaux alignés. La voix lit « deux virgule neuf cent quatre-vingt-cinq ».
- **VDP4.** La voix dit « moins trois sur quatre ». La condition est « a et b des entiers » avec b ≠ 0. Le nombre 2,25 précède son libellé. Les explications sur l’écriture de √7 et π sont agrandies. L’équation de π garde les mêmes coordonnées pixel lors du changement d’annotation. Les libellés concernant les entiers et la droite graduée ont été harmonisés.

La V4 reprend la voix Soukaina Eleven v4, en français à 0,94 et stabilité 0,45. Sept scènes contiennent de nouvelles prises, dont les deux explications d’objectif désormais en français selon la fiche. Les 32 autres séquences reprennent les WAV de V3. Pour une reproduction avec les prises locales disponibles, exécuter les commandes suivantes.

```powershell
python -X utf8 scripts/prepare-n3-sem3-v4.py timeline
npm run render:storyboards -- --stills --math-proof week-three-v4
npm run render:storyboards -- week-three-v4
python -X utf8 scripts/verify-storyboard-batch.py week-three-v4
```

Pour recréer une prise, utiliser l’étape `prepare` du même script, le [profil Soukaina](#reproduire-la-révision-bilingue-v3), puis `align-n3.py` et `pace-n3.py` sur `src/video/n3-sem3-v4-voice-plan.json`. La sortie de la mise en rythme est `src/video/n3-sem3-v4-paced-plan.json`, avec l’audio dans `public/n3-sem3-elevenlabs-v4-paced/` et un objectif de 0,65 s entre idées.

Les exports et timelines éditables se trouvent dans `outputs/n3-sem3-v4/vdp1` à `vdp4`. Les quatre sources couvrent 126 diapositives et 39 séquences. Les MP4 passent le décodage complet en 1080p30 H.264/AAC. 221 repères ont été extraits de l’encodage, dont les étapes corrigées. Le contrôle audio a comparé les débuts des séquences sur AAC avec leurs WAV. La reconnaissance indépendante a retrouvé les deux numérateurs 2985 dans des fenêtres ciblées. Pour l’annonce de 2,985 et l’explication « Reconnaître, c’est savoir », des fenêtres avec contexte ont départagé des sorties divergentes de la reconnaissance sur des extraits courts.

Les quatre V4 ont été déposées via `files.update`. La relecture a confirmé les empreintes dans « Livrable video / 3AC / Semaine 3 » via les liens permanents K8, K15, K22 et K29.

## Remarques de l’inspecteur · reçues le 24 novembre 2026 · en attente

L’utilisateur demande uniquement l’enregistrement et annonce d’autres remarques. Neuf captures et cinq DOCX ont été copiés à l’identique dans reference/inspector-revisions/2026-11-24/, avec manifeste SHA256 vérifié. Les captures concernent les VDP1, VDP2 et VDP4 de 3AC semaine 3 ainsi que la VDP4 de 1AC semaine 2. Les DOCX concernent les quatre VDP de 3AC semaine 3 et la VDP1 de 1AC semaine 3.

Les annotations visibles sont consignées comme points à vérifier ; les cinq DOCX ne sont pas encore relus. Les libellés V2 dans les captures doivent être confrontés aux versions réellement examinées, le handoff décrivant aussi des livraisons V4. Aucune correction, voix, vidéo, donnée Google ou automatisation n’a été changée. Attendre la suite des remarques et l’accord de l’utilisateur avant de modifier. [Dossier de collecte](references/inspector-notes-2026-11-24.md)

## Rapport consolidé des remarques de l’inspecteur · 24 novembre 2026

À la demande d’un rapport sous forme de tableau, les cinq DOCX ont été lus, leurs tableaux extraits et leurs quinze images intégrées inspectées, avec les neuf captures déjà reçues. Le rapport local reference/inspector-revisions/2026-11-24/consolidated-report.json contient 41 entrées regroupées pour six vidéos et les consignes transversales. La notation du a, le vocabulaire périodique, la flèche de non périodique et les deux formulations sur l’abscisse de la fiche VDP4 demandent validation. Les versions V2 signalées doivent être rapprochées des vidéos réellement examinées avant de comparer avec les V4 documentées. Aucune modification de vidéo ni de données Google n’est effectuée. [Remarques et points à valider](references/inspector-notes-2026-11-24.md)


## V5 · 3AC semaine 3 VDP1 · Révision du 25 novembre 2026

L’utilisateur autorise cette leçon uniquement. La source courante téléchargée via API est identique au PPTX archivé. Les 30 bandes de voix et les zones pédagogiques ont été comparées à la V4. Les reformulations antérieures ont été retirées ; la voix reprend les mots source, avec expansions orales tracées des notations/ordinaux et ponctuation technique de fin de phrase. L’explication française de l’objectif validée par la fiche et la syllabification native explicitement demandée sont les deux exceptions documentées localement. Une maladresse grammaticale de source est conservée et signalée dans l’audit, sans correction silencieuse.

Huit points de l’inspecteur sont traités et vérifiés : définition/synthèse sans ajout de condition, notation puis lecture séparées, deux schémas progressifs, trois étapes de recherche, préambules des propriétés conformes à la source et marqueur Faux distinct de la multiplication. Les fondus au noir sont supprimés pour cette leçon. Le a de la définition et du radical reprend la graphie mathématique italique grasse de la diapositive 6 ; l’intention exacte de l’annotation non précisée reste à confirmer si une autre graphie était visée. Ne pas déclarer ce dernier point entièrement validé par l’inspecteur.

Les neuf nouvelles prises utilisent Soukaina, Eleven v4, langue fr, vitesse 0,94 et stabilité 0,45. Le passage Ra–cine rejoint Racine avec PronunciationLine, sans média intégré au PPT. Les aides phonétiques restent hors image. Détection indépendante française sur les neuf scènes ; les unités isolées et le mot entier ont aussi été reconnus sans texte attendu. Le second service d’analyse acoustique était indisponible (HTTP 503) : ne pas revendiquer une certification phonétique humaine. Les corrélations AAC contrôlent les neuf débuts de scène et les trois unités de prononciation.

Reproduction : scripts/revise-n3-sem3-vdp1-v5.py prepare ; génération ElevenLabs avec le profil ci-dessus ; align-n3.py sur src/video/n3-sem3-vdp1-v5-voice-plan.json ; pace-n3.py vers n3-sem3-elevenlabs-v5-vdp1-paced, sortie src/video/n3-sem3-vdp1-v5-paced-plan.json, pause cible 0,65 s ; étape timeline ; npm run render:storyboards -- n3-sem3-vdp1-v5 ; verify-storyboard-batch.py n3-sem3-vdp1-v5 ; étape check. Quatre tests dans scripts/test-n3-sem3-vdp1-source.py refusent la réintroduction des réécritures, une omission et la perte du radical OMML. TypeScript et les 19 tests studio passent.

Export local : outputs/n3-sem3-v5/vdp1/P1_MATHS_N3_SEM3_VDP1_V5.mp4, 5 215 images, 173,845 s, 1080p30 H.264/AAC. Décodage complet, couverture 30 diapositives, aucune image noire détectée ; 89 repères extraits du MP4 et états corrigés revus. Sources, voix, captures et audits détaillés restent locaux.

Livraison API par révision du même fichier public en K8, onglet P1 / Semaine 3. Puce, dossier, empreinte MD5 b2e8ceff12c9c0f3a619a7c49440e4f0 et en-tête MP4 anonyme HTTP 206 vérifiés ; dates existantes conservées. Le rapport illustré conserve 41 points et 24 images initiales : dix points vérifiés au total (deux N1 et huit N3), 31 en attente dont cinq à préciser. Les quatre autres vidéos du dossier inspecteur restent hors de cette révision.


## V6 · 3AC semaine 3 VDP1 · Phrase de notation complète · 25 novembre 2026

La comparaison utilisateur révèle une omission visuelle dans la V5 : l’amorce et la conjonction de la phrase de notation avaient disparu, alors que la voix source était complète. La V6 restitue tous les mots et la ponctuation de cette phrase, en révélant l’amorce, le radical puis la lecture sur leurs repères vocaux. La capture originale est archivée sans modification dans le dossier de référence local ; le tableau illustré la rattache au point concerné.

La correction est limitée aux éléments visuels de cette phrase dans la scène Définition. Les huit autres scènes, les schémas, les neuf WAV, la narration et les durées sont identiques à la V5. Les pistes AAC extraites des deux MP4 sont strictement identiques octet par octet. Aucune nouvelle génération de voix n’est effectuée.

Script reproductible : scripts/fix-n3-sem3-vdp1-definition-v6.py prepare ; npm run render:storyboards -- --stills --math-proof n3-sem3-vdp1-v6 ; npm run render:storyboards -- n3-sem3-vdp1-v6 ; verify-storyboard-batch.py n3-sem3-vdp1-v6 ; étape check du script V6. Le contrôle compare la phrase visible complète au paragraphe pédagogique de la diapositive 7, indépendamment de la bande de voix, et rejette l’omission de l’amorce ou de la conjonction. TypeScript passe.

Export outputs/n3-sem3-v6/vdp1/P1_MATHS_N3_SEM3_VDP1_V6.mp4 : 5 215 images, 173,845 s, H.264/AAC 1080p30. Décodage complet et absence de noir vérifiés, 91 repères encodés extraits ; états de la phrase avant/après relus. Les neuf prises correspondent à l’audio encodé. Révision du même fichier public en K8, dossier Livrable video / 3AC / Semaine 3 ; empreinte 0b59579fcb92737106a74bd32f27ab93, puce et accès anonyme HTTP 206 vérifiés, dates existantes conservées. Rapport : 41 points, 25 images originales, dix points traités au total ; les clarifications antérieures et les quatre autres dossiers restent inchangés.


## V5 · 3AC semaine 3 VDP2 · Comparaison des racines carrées · 25 novembre 2026

L’utilisateur autorise la correction de cette vidéo, puis confirme deux points : corriger la graphie de la carte en Racine carrée et rattacher la capture périodique à N3 SEM3 VDP3. Cette dernière remarque est déplacée dans le rapport vers VDP3, avec son image et la trace de confirmation ; aucune vidéo VDP3 n’est modifiée ici. Les huit points réellement associés à VDP2 sont traités et vérifiés.

La source courante récupérée par API est identique au PPTX archivé, 18 diapositives. Les six scènes reprennent les formulations source, avec les deux remplacements précis de narration demandés par la fiche : explication française de l’objectif regroupant les diapositives 2–3 et question explicative de la diapositive 14. Les notations numériques sont développées oralement, sans autre reformulation. La répétition artificielle est absente ; aucune occurrence de strictement ou condition ajoutée ne subsiste. Le paragraphe pédagogique complet de la propriété, les quatre comparaisons et leurs signes sont contrôlés séparément de la narration contre les zones source. Les trois cartes reprennent leur disposition dans l’image du storyboard, avec la correction orthographique explicitement approuvée.

Les deux inégalités bleues apparaissent séparément après le préambule complet. Les nombres et signes de l’exemple s’animent sur leurs mots. Le repère textuel Faux se distingue de la multiplication ; une pulsation douce pendant l’explication et l’accent simultané sur les deux radicandes négatifs suivent la consigne. repeatPulse est un champ facultatif des visuels VDP : cycle de 48 images, début sur le repère de pulsation, amplitude/atténuation discrètes. Les scènes existantes qui n’activent pas ce champ gardent leur comportement. Aucun fondu au noir.

Les six prises utilisent Soukaina, Eleven v4, langue fr, vitesse 0,94, stabilité 0,45. La prononciation Com–pa–rer rejoint Comparer avec PronunciationLine et la voix principale ; aucun média PPT ni guide phonétique affiché. Reconnaissance indépendante française sur les six scènes. Un second contrôle acoustique Gemini, sans texte ni phonèmes attendus, retrouve les trois syllabes françaises et le mot entier sans lecture anglaise signalée. Une fenêtre locale trop courte du premier son a produit une transcription manifestement impossible pour sa durée ; ce résultat ASR est annoté comme non fiable, sans modifier la bonne prise. Les six débuts de scène et les quatre unités de prononciation concordent avec l’AAC encodé. Ces contrôles automatiques ne sont pas une certification phonétique humaine complète.

Reproduction : scripts/revise-n3-sem3-vdp2-v5.py prepare ; génération ElevenLabs avec le profil validé ; align-n3.py sur src/video/n3-sem3-vdp2-v5-voice-plan.json ; pace-n3.py vers n3-sem3-elevenlabs-v5-vdp2-paced et src/video/n3-sem3-vdp2-v5-paced-plan.json, pause cible 0,65 s ; étape timeline --correct-card-spelling ; npm run render:storyboards -- n3-sem3-vdp2-v5 ; verify-storyboard-batch.py n3-sem3-vdp2-v5 ; étape check. Le reçu local user-approvals.json conserve l’accord orthographique et l’attribution de la remarque périodique. TypeScript, les 19 tests studio et quatre tests source dédiés passent. Ces derniers refusent une réécriture non approuvée, la perte d’un connecteur de la propriété et un signe de comparaison modifié.

Export outputs/n3-sem3-v5/vdp2/P1_MATHS_N3_SEM3_VDP2_V5.mp4 : 2 907 images, 96,917 s, H.264/AAC 1080p30. Décodage intégral, absence de noir et couverture des 18 diapositives vérifiés ; 53 repères extraits du MP4, états corrigés revus. Livraison API par révision du même fichier public en K15, dossier Livrable video / 3AC / Semaine 3. Puce, MD5 2156e7db5546d12b04696693ffe0dc94 et en-tête anonyme HTTP 206 confirmés ; dates existantes conservées. Le rapport illustré contient toujours 41 points et 25 images : 18 points vérifiés, 23 en attente dont cinq à préciser. VDP2 compte huit points vérifiés ; VDP3 compte désormais dix points, dont la capture périodique. Les trois autres dossiers inspecteur restent en attente.


## V5 · 3AC semaine 3 VDP3 · 26 novembre 2026

Les dix points inspecteur de cette vidéo sont corrigés et vérifiés. La source API courante correspond au PPTX archivé de 31 diapositives. Les dix scènes restaurent les formulations source ; seules les corrections précises approuvées sont appliquées : cohérence de la narration de la fraction négative avec le visuel de la diapositive 18, coquille Car de la diapositive 11 et numérateur 225 seul avant l’égalité finale correcte. Les accords sont enregistrés dans outputs/n3-sem3-v5/vdp3/user-approvals.json. La lecture du nombre décimal suit la fiche inspecteur. L’objectif source et sa progression validée sont conservés ; les maladresses source non autorisées restent signalées sans réécriture.

Définition et propriété complètes, noires et de taille uniforme ; légendes différées sur leurs mots, exposants noirs, accents sur le dénominateur puis l’exposant existant sans dupliquer le chiffre. Chaque égalité utilise une seule composition KaTeX, avec réserves invisibles pour stabiliser la géométrie pendant les révélations. Deux lignes partagent la colonne des égalités. La mesure des pixels du MP4 donne un écart nul entre axes des fractions et des égalités ; les barres restent fixes avant/après résultat. Le champ facultatif toFrame permet une sortie précise d’un visuel, validée dans les bornes de la scène ; les leçons ne l’utilisant pas conservent leur comportement.

Illimité et Périodique suivent le modèle natif PronunciationLine : parties orthographiques complètes, puis réunion du mot, même voix principale Soukaina, Eleven v4, langue fr, vitesse 0,94, stabilité 0,45. Aucun média PPT ni aide phonétique à l’image. La remarque pé–rio est bien attribuée par l’utilisateur à VDP3. Une confusion acoustique m/n a été corrigée avec un dictionnaire IPA français non prononcé, uniquement sur les deux prises concernées, sans modifier les mots source. Son cache privé local est nécessaire pour reproduire exactement ces prises ; ne copier aucun identifiant privé, locateur ni secret dans les compétences ou GitHub. Reconnaissance indépendante des dix scènes et analyse acoustique ciblée des sons et mots ; les réponses secondaires incomplètes sont annotées comme non probantes, sans certification phonétique humaine complète. Les dix débuts de scène et neuf unités de prononciation concordent avec l’AAC final.

Reproduction : scripts/revise-n3-sem3-vdp3-v5.py prepare, préparation privée de diction par scripts/prepare-n3-sem3-illimite-voice.mjs, génération du plan vocal, align-n3.py, pace-n3.py, étape timeline, npm run render:storyboards -- n3-sem3-vdp3-v5, verify-storyboard-batch.py n3-sem3-vdp3-v5, étape check. scripts/test-n3-sem3-vdp3-source.py contient quatre tests contre reformulation, omission, erreur de formule et égalité intermédiaire fausse. scripts/check-n3-sem3-vdp3-layout.py vérifie les axes encodés. TypeScript et les 19 tests studio passent. Les audits de narration et de contenu visible sont distincts et comparent les zones source réelles, y compris les formules OMML.

Export outputs/n3-sem3-v5/vdp3/P1_MATHS_N3_SEM3_VDP3_V5.mp4 : 4 766 images, 158,869 s, H.264/AAC 1920×1080 à 30 images/s. Décodage intégral, couverture des 31 diapositives, absence de noir et 105 repères encodés contrôlés ; crête audio −5,7 dB. Livraison API par révision du même fichier public, puce K22 du suivi P1 / Semaine 3, dossier Livrable video / 3AC / Semaine 3. MD5 9740ca08282b0322ab6d286e27428057, puce, accès anonyme HTTP 206 et en-tête MP4 vérifiés ; cellules de dates existantes conservées. Reçu local delivery.json. La source, les prises, les captures et les audits détaillés restent locaux.

Le tableau illustré conserve 41 points et 25 images originales : 28 traités, 13 en attente dont quatre à préciser. VDP3 compte dix points traités ; VDP4 et N1 SEM2 VDP4 ne sont pas révisées ici. L’intention exacte de l’annotation du a dans N3 VDP1 reste à préciser. Références synchronisées dans les trois copies locales Digital Lab et notes de prononciation ajoutées séparément aux trois compétences présentation vidéo ; aucun dépôt Git dans le projet ou le miroir, aucune publication GitHub.


## Anomalie VDP3 V5 signalée après livraison · 26 novembre 2026

La comparaison utilisateur montre que la diapositive 17 ne contient que sa fraction et son résultat, alors que la scène fraction-1 de la V5 ajoute en dessous la formule de la diapositive 15. Vérification directe de source-inventory.json et du générateur : cet ajout est explicitement créé par eq2 puis formula(eq2, ...) ; il ne vient ni d’un cache ni du storyboard de ce passage. L’audit visible compare à tort cette ligne à la diapositive 15, ce qui valide sa formule mais pas son appartenance à la scène. Les contrôles antérieurs et la mention des dix points traités ne constituent donc pas une validation complète de la fidélité de cette scène.

État : anomalie supplémentaire confirmée, correction de production en attente. À ce stade, aucun code de rendu, MP4, fichier Drive ou cellule Sheets n’est modifié. Retirer ce rappel non demandé lors de la correction et contrôler la scène complète contre ses seules diapositives 16–17. Comparer l’ensemble des éléments visibles et leurs transitions aux sources du passage, en détectant aussi les ajouts, pas seulement les omissions ou la validité mathématique. Aucun rappel d’un exemple précédent sans consigne source ou accord explicite. Les preuves détaillées restent locales dans outputs/n3-sem3-v5/vdp3/post-delivery-extra-formula-issue.json.


### Confirmation utilisateur · aucune initiative sur le contenu · 26 novembre 2026

L’utilisateur réaffirme la règle existante après l’ajout indu d’un ancien exemple en VDP3 : aucune initiative sur le contenu pédagogique ou la voix off. Ne pas ajouter de rappel, comparaison, exemple, explication ou élément provenant d’une autre diapositive sans consigne source ou accord précis déjà donné. Toute anomalie, incohérence ou correction proposée doit être signalée avec le passage source et la modification exacte envisagée ; attendre la confirmation de l’utilisateur avant de modifier ce passage. Ne pas interpréter un accord général de production ou de correction comme l’accord sur une modification particulière. Les accords précis déjà enregistrés restent valables dans leur périmètre. Les ajustements de mise en page et d’animation déjà autorisés restent possibles seulement s’ils ne changent pas le contenu ni la séquence pédagogique. Vérifier les ajouts autant que les omissions à l’échelle des diapositives du passage.

La formule supplémentaire de la V5 reste une anomalie confirmée en attente ; cette mise à jour documentaire n’effectue aucune modification du rendu ni des données Google. Références synchronisées localement, sans publication GitHub.


## V6 · 3AC semaine 3 VDP3 · Suppression du rappel non autorisé · 26 novembre 2026

Après comparaison utilisateur et accord explicite de suppression, la V6 retire uniquement le quatrième visuel de la scène fraction-1 : le rappel de l’exemple précédent qui n’appartient pas aux diapositives 16–17. Le passage conserve ses trois visuels source, ses positions et ses repères. Les neuf autres scènes, tous les textes de narration, les dix fichiers audio et les durées sont strictement identiques à la V5. Les pistes AAC extraites des MP4 V5/V6 sont identiques octet par octet. Aucun appel TTS ni changement de contenu supplémentaire.

Le défaut de la V5 venait du générateur et d’un contrôle comparant une formule supplémentaire à une diapositive extérieure au passage. Les anciens dix points inspecteur traités ne prouvaient pas l’absence de cet ajout. L’anomalie supplémentaire est désormais résolue en V6 ; conserver son historique et la comparaison originale locale. La règle reste : aucune initiative sur le contenu ; toute autre anomalie nécessite confirmation avant modification du passage concerné. Les accords précédents restent limités à leur périmètre.

Reproduction : scripts/fix-n3-sem3-vdp3-extra-example-v6.py prepare ; npm run render:storyboards -- --stills --math-proof n3-sem3-vdp3-v6 ; npm run render:storyboards -- n3-sem3-vdp3-v6 ; verify-storyboard-batch.py n3-sem3-vdp3-v6 ; étape check du correctif ; scripts/check-n3-sem3-vdp3-v6-encoded.py. Deux tests dans scripts/test-n3-sem3-vdp3-extra-example.py refusent la réintroduction du rappel, une substitution par un ancien exemple, une omission et une modification hors périmètre. TypeScript et les 19 tests studio passent. Le contrôle V6 compare tous les visuels du passage à ses propres diapositives ; ne pas employer le contrôle V5 historique comme validation de cette appartenance. Les exports historiques et le générateur V5 restent des traces de la version antérieure, pas le point de départ validé d’une nouvelle livraison.

Export outputs/n3-sem3-v6/vdp3/P1_MATHS_N3_SEM3_VDP3_V6.mp4 : 4 766 images, 158,869 s, H.264/AAC 1920×1080 à 30 images/s. Décodage intégral et absence de noir vérifiés ; 103 repères encodés extraits. Sept images du passage et les 376 images continues de la zone inférieure confirment l’absence de la ligne ajoutée. Les axes fraction/égalité conservent un écart mesuré nul. Les autres contrôles vocaux V5 restent historiques et applicables au son identique ; aucune nouvelle certification phonétique n’est revendiquée.

Livraison API vérifiée sur le même fichier Drive public, puce K22, dossier Livrable video / 3AC / Semaine 3. MD5 955d48c9ac4a5d468a547afa93ccdd6c, taille 9183887 octets, accès anonyme HTTP 206 avec en-tête MP4, dates N22/O22 inchangées. Reçu local delivery.json à 2026-11-26T12:24:53.860958+01:00. L’aperçu studio propose la V6 et identifie la V5 comme historique. Le tableau illustré indique V6 et la correction complémentaire, sans gonfler les 41 points initiaux : 28 traités, 13 restants dont quatre à préciser. Les autres dossiers ne sont pas révisés ici.

Handoff et cinq références Digital Lab synchronisés dans les trois copies locales. Sources, capture de comparaison, prises et audits restent locaux. Aucun dépôt Git dans le projet ou miroir, aucune publication GitHub.


## V5 · 3AC semaine 3 VDP4 · 26 novembre 2026

La V5 est livrée et vérifiée sur le même fichier public. Le storyboard courant récupéré par API correspond aux 47 diapositives archivées ; égalité reconfirmée juste avant livraison. Quatorze scènes rétablissent les formulations source et les textes pédagogiques complets, avec les seules exceptions autorisées. Quatre décisions utilisateur sont consignées dans outputs/n3-sem3-v5/vdp4/user-approvals.json : deux formulations précises sur le point, son abscisse et la réciproque ; chiffres exacts de pi ; objectif limité à sa phrase source, sans l’énumération ajoutée dans la V4. Ce dernier choix remplace la demande antérieure de lecture détaillée des nombres de l’objectif : ne pas remettre cette énumération sous prétexte de corriger une fraction parlée absente de la source choisie. Les exemples mathématiques restent visibles selon le storyboard.

Les définitions, les conditions exprimées en français avec le dénominateur non nul, les conclusions complètes et les légendes sont contrôlées contre leurs propres diapositives. La légende finie de l’exemple décimal suit la fiche inspecteur ; la voix conserve le mot source de ce passage. La position de toute l’écriture de pi reste fixe pendant le changement d’annotation. Un décalage interne de 17 pixels découvert avant publication provenait du type d’atome KaTeX de l’accolade ; un atome ordinaire explicite stabilise aussi les chiffres, pas seulement le conteneur. Les deux cadres de pixels encodés sont maintenant identiques. La propriété est noire, les tailles sont harmonisées, les accolades/accents gardent leur sens et les fondus au noir sont supprimés.

La fidélité est temporelle : la phrase de propriété disparaît avant son tableau, le premier exemple entier disparaît avant le suivant et les explications de l’objectif se terminent avant sa phrase de transition. endFrame est un champ facultatif des liens d’objectif, borné dans sa scène, transmis au mécanisme de fin déjà présent dans LinkedObjective. Les anciennes leçons sans ce champ gardent leur comportement. Le tableau natif source-full conserve les trois libellés complets et utilise setPulses pour des accents discrets sur les mots concernés ; mode historique inchangé. Les fragments de texte multicolores conservent leurs espaces avec xmlSpace preserve.

Deux prononciations natives, Irrationnel et Réel, utilisent Soukaina Eleven v4, français explicite, vitesse 0,94 et stabilité 0,45, comme la voix principale. Aucun son ou clip du PPT et aucune aide phonétique affichée. Une voyelle isolée nasalisée a été corrigée par dictionnaire IPA privé, sans changer les mots ni la voix ; les parties orthographiques restent complètes puis se réunissent selon PronunciationLine. Les dictionnaires, leurs identifiants et les prises détaillées restent locaux. Reconnaissance indépendante en français sur les quatorze prises, avec empreintes actualisées après correction de diction ; huit unités et les quatorze débuts de scène concordent avec l’AAC (corrélation minimale 0,9996). L’analyse acoustique secondaire de Réel est favorable ; celle de la première prise Irrationnel a signalé la voyelle. Les nouvelles analyses secondaires ont échoué avec HTTP 503, et un modèle listé a renvoyé HTTP 404 pour cet accès. Ces échecs ne sont pas des validations et les anciennes analyses ne certifient pas la nouvelle prise. Le contrôle local reconnaît la nouvelle suite syllabique et le mot français ; aucune certification phonétique humaine complète n’est revendiquée.

Extraction source : ne pas classifier uniquement selon y. Dans ce deck, une équation haute est un contenu élève, les graduations basses sont du contenu élève, une consigne est placée plus haut que la bande habituelle, et le tableau contient des cellules à lire. Ces cas sont vérifiés avec les images source ; ce lecteur reste spécifique à ce storyboard, pas un interpréteur universel.

Reproduction : scripts/revise-n3-sem3-vdp4-v5.py prepare ; dictionnaire ciblé via scripts/prepare-n3-sem3-irrationnel-voice.mjs si nécessaire ; génération du plan vocal avec le profil validé ; align-n3.py ; pace-n3.py avec pause minimale 0,65 s ; étapes timeline et audit ; npm run render:storyboards -- n3-sem3-vdp4-v5 ; verify-storyboard-batch.py n3-sem3-vdp4-v5 ; étapes check et scripts/check-n3-sem3-vdp4-v5-encoded.py. Le cache privé des dictionnaires est nécessaire à une reproduction exacte des prises. Cinq tests source/mathématiques, les 19 tests studio et TypeScript passent. Les tests refusent ajouts, omissions, modifications non autorisées et report d’un ancien exemple ; les préfixes décimaux sont vérifiés indépendamment, dont pi par la formule de Machin.

Export outputs/n3-sem3-v5/vdp4/P1_MATHS_N3_SEM3_VDP4_V5.mp4 : 7 063 images, 235,435 s, H.264/AAC 1920×1080 à 30 images/s, crête −4,8 dB. Décodage intégral, 47 diapositives et absence de noir contrôlés ; 157 repères encodés extraits. Mesures indépendantes : écriture de pi stable, aucune ancienne légende entière pendant le nouvel exemple, texte de propriété noir, marqueur de racine de deux correctement placé entre un et deux, anciennes explications absentes après leurs changements de diapositive.

Livraison API sur le même fichier public, puce K29, dossier Livrable video / 3AC / Semaine 3 ; MD5 4bcd87ed0b28111cf421e646321fd339, 14510194 octets. Puce, accès anonyme HTTP 206, en-tête MP4 et dates N29/O29 inchangées vérifiés à 2026-11-26T13:22:34.784666+01:00. Le suivi illustré conserve 41 points et 25 images initiales : 38 traités, trois restants dont deux à préciser. VDP4 a dix points traités, dont le choix utilisateur de voix source ; la capture avec flèche sous non périodique reste à attribuer/préciser et n’est pas modifiée. L’annotation du a en VDP1 et le dossier N1 SEM2 VDP4 restent ouverts. Aucun autre MP4 livré n’est modifié.

Handoff et références Digital Lab synchronisés dans les trois copies locales ; notes de prononciation ajoutées séparément aux trois compétences présentation vidéo en préservant leurs différences. Aucun dépôt Git dans le projet ou le miroir, aucune publication GitHub. Sources, voix, images et audits détaillés restent locaux.


## V6 · 3AC semaine 3 VDP4 · Texte fourni et coupure vocale · 26 novembre 2026

Après comparaison utilisateur, la dernière consigne porte spécifiquement sur la propriété 3 : reprendre exactement le storyboard en tenant compte de la fiche de correction fournie. Ces deux sources ont la même formulation à cet endroit. Cette décision remplace, pour ces deux phrases seulement, les formulations proposées puis approuvées lors de la V5. La V6 reprend mot pour mot le texte et la voix fournis, en conservant l’accent rouge source sur le mot abscisse. Les difficultés logiques de cette formulation ont été expliquées auparavant ; la conformité au texte demandé ne constitue pas une certification de sa justesse mathématique. Ne pas réintroduire les formulations V5 de sa propre initiative. Les décisions sur l’objectif sans énumération et les chiffres exacts de pi restent inchangées.

La coupure signalée à 00:26–00:27 était réelle : pace-n3.py insérait 0,63 s de zéro numérique à 26,945 s, au milieu d’un son de la prononciation Irrationnel. L’alignement estimait un intervalle de 20 ms alors que le PCM était fortement voisé (RMS environ 0,17). Treize autres insertions de cette vidéo sont dans des zones de faible énergie, contrôlées séparément. La V6 supprime uniquement cette pause artificielle dans la prise de vocabulaire : le PCM réparé est exactement celui de la prise brute, et les échantillons avant/après les 15 120 échantillons de silence retirés sont identiques. Aucun mot ni son de la voix originale n’est retranché. Seule la scène de propriété 3 nécessite une nouvelle génération de voix, avec le même profil Soukaina français. Douze autres scènes sont strictement identiques à la V5.

Correctif réutilisable : scripts/speech_pause.py contrôle une fenêtre PCM de 80 ms avant toute insertion. Pour les PCM 16 bits connus, il recherche une zone réellement calme (RMS ≤ −55 dB, crête ≤ −40 dB), sinon ignore et journalise la pause au lieu de couper la parole. Le milieu de deux repères d’alignement n’est pas une preuve de silence. Les formats non validés n’autorisent pas une insertion aveugle. Trois tests couvrent parole active, vrai silence et la coupure réellement signalée ; deux tests V6 couvrent le texte fourni et la protection des autres scènes. TypeScript passe. Les anciennes prises et leurs silences restent archivés ; aucune autre vidéo livrée n’est recalculée par ce correctif.

Reproduction : scripts/revise-n3-sem3-vdp4-v6.py prepare ; génération de son plan vocal unique ; align-n3.py sur le pacing-plan ; pace-n3.py vers n3-sem3-elevenlabs-v6-vdp4-paced ; étape timeline ; npm run render:storyboards -- n3-sem3-vdp4-v6 ; verify-storyboard-batch.py n3-sem3-vdp4-v6 ; étape check ; scripts/check-n3-sem3-vdp4-v5-encoded.py --folder outputs/n3-sem3-v6/vdp4. Les audits vérifient séparément les deux phrases contre les zones élèves source et leur narration contre les bandes de voix. Les autres décisions V5 sont contrôlées sans transformer la dernière demande en permission générale de modifier le contenu.

Export outputs/n3-sem3-v6/vdp4/P1_MATHS_N3_SEM3_VDP4_V6.mp4 : 6 988 images, 232,939 s, H.264/AAC 1080p30, crête −4,8 dB. Décodage intégral, couverture des 47 diapositives, absence de noir et 161 repères encodés contrôlés. Les quatorze prises concordent avec l’AAC (minimum 0,9996) ; la fenêtre réparée a une corrélation de 1,0 avec la prise brute. Les contrôles de placement de pi, des anciens exemples, du tableau et du point sur la droite passent. La nouvelle prise de propriété est reconnue indépendamment en français ; les transcriptions homophones ne modifient pas la source. Aucune certification phonétique humaine complète.

Livraison par révision du même fichier public en K29, dossier Livrable video / 3AC / Semaine 3 ; MD5 b52436dabe0af27dd338cac272a2ce14, 14296808 octets. Puce, accès anonyme HTTP 206, en-tête MP4 et dates N29/O29 inchangées vérifiés à 2026-11-26T16:19:02.612887+01:00. La comparaison originale du 26 novembre est archivée sans modification et ajoutée au tableau illustré. Celui-ci conserve 41 points, avec 26 images : 38 traités, trois restants dont deux à préciser. Les deux lignes de propriété portent désormais le choix source de la V6 ; l’incident audio est un complément, pas un nouveau point artificiel. La flèche non attribuée et les autres dossiers ouverts ne sont pas modifiés.

Handoff et références Digital Lab synchronisés dans les trois copies locales ; références présentation vidéo ajustées séparément en conservant leurs différences. Aucun dépôt Git dans le projet ou le miroir, aucune publication GitHub. Images, voix, contenu détaillé et caches privés restent locaux.


## V7 · 3AC semaine 3 VDP4 · Choix limitée · 26 novembre 2026

Après comparaison, la fiche initiale demandait finie alors que le storyboard et la voix utilisent limitée. Le dernier choix explicite utilisateur retient limitée. La V7 remplace uniquement ce mot visible et sa réserve de mise en page invisible ; tous les autres champs, les quatorze voix et les durées restent identiques à la V6. Cette décision remplace seulement cette demande de la fiche, sans annuler les autres corrections. La propriété 3 selon le texte fourni et la réparation de la coupure restent conservées.

Reproduction : scripts/fix-n3-sem3-vdp4-limitee-v7.py prepare ; rendu n3-sem3-vdp4-v7 ; verify-storyboard-batch.py ; étape check ; contrôle encodé des placements. TypeScript passe. Export 6 988 images, 232,939 s, H.264/AAC 1080p30, 161 repères encodés, décodage intégral sans noir inattendu. AAC entier strictement identique à la V6 ; coordonnées de 2,25 identiques avant/après légende. Livraison API sur le même fichier public en K29, dates conservées, puce et accès anonyme HTTP 206 vérifiés. MD5 bccfd8345ce1f093a8ac63cb8c02786b, 14302136 octets, reçu outputs/n3-sem3-v7/vdp4/delivery.json à 2026-11-26T17:13:32.137338+01:00. La flèche non périodique reste à préciser. La comparaison originale est archivée sans modification pour le tableau illustré.
