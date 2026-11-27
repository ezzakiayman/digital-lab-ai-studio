# 3AC · Semaine 4 · VDP1 et VDP2 · 19 novembre 2026

## Sources et choix pédagogiques

Dans « P1 / Semaine 4 » (gid 1798831664), F8 fournit P1_MATHS_N3_SEM4_VDP1.pptx et F15 fournit P1_MATHS_N3_SEM4_VDP2.pptx. Deux VDP actives étaient disponibles lors de l’inventaire. Chacune compte 16 diapositives, réunies en sept scènes. Les sources et les images PowerPoint sont dans reference/n3-sem4-vdp1/ et reference/n3-sem4-vdp2/. Les empreintes MD5 des deux PowerPoint ont été comparées aux métadonnées Drive avant livraison et n’avaient pas changé.

La VDP1 traite du produit de deux racines carrées : √a × √b = √(a×b). Elle conserve les exemples √2 × √8 et √(16×25). La condition est explicitée par « positifs ou nuls », avec a ≥ 0 et b ≥ 0. La VDP2 traite du quotient : √a / √b = √(a/b). Elle conserve √8 / √2 et √(25/16), avec a ≥ 0 et b > 0. La narration précise que le dénominateur ne peut pas être nul. Les exemples restent aux étapes du storyboard, sans ajouter de simplification finale absente de la source.

La bande verte est utilisée pour la voix uniquement, la bande basse pour la réalisation. La zone pédagogique centrale fournit le contenu visible. Aucun MP4 ou audio de prononciation n’était intégré à ces deux fichiers. « Radical » utilise les syllabes ra–di–cal, puis leur réunion. La V1 avait suivi la note de la diapositive 12 en lisant le mot entier « Quotient » sans clip source. Ce choix est remplacé par la correction explicite de l’utilisateur décrite dans la section V2 ci-dessous.

Le lot reprend Soukaina, modèle Eleven v4, langue française, vitesse 0,94 et stabilité 0,45. Le choix assure la continuité des VDP de 3AC révisées. Les pauses inter-idées visent 0,65 s ; le traitement a ajouté 5,64 s de silence sur les 14 prises, sans modifier leur débit ni leur hauteur.

## Composants et reproduction

scripts/prepare-n3-sem4.py prépare les deux plans, puis les timelines. Les objectifs contiennent une formule KaTeX native, dans la couleur marine du titre. LinkedObjective accepte ce complément sans modifier les anciens objectifs. La largeur réservée à la formule et l’ensemble du bandeau ont été vérifiés dans les images de contrôle. Les flèches restent verticales, rouge puis verte ; seuls les mots expliqués sont soulignés.

Les égalités complètes sont composées dans un seul bloc KaTeX pour conserver l’espacement mathématique. Un membre masqué réserve sa place avant l’entrée du résultat à la voix. Le conteneur Formula de VdpSequence utilise désormais une hauteur au moins égale à cinq fois la taille du texte, avec un minimum de 400 px. Cette correction évite de couper le dénominateur des grandes fractions de radicaux. Le calcul de vocabulaire est dégagé du cadre du mot « Quotient ».

Pour reprendre les prises et leurs alignements existants :

~~~powershell
python -X utf8 scripts/prepare-n3-sem4.py prepare
python -X utf8 scripts/pace-n3.py --plan src/video/n3-sem4-plan.json --audio-dir n3-sem4-paced --output src/video/n3-sem4-paced-plan.json --gap-seconds 0.65
python -X utf8 scripts/prepare-n3-sem4.py timeline
npm run render:storyboards -- --stills --key-frames week-four
npm run render:storyboards -- week-four
python -X utf8 scripts/verify-storyboard-batch.py week-four
python -X utf8 -B scripts/check-n3-sem4.py
~~~

pace-n3.py attend un chemin relatif au dossier public pour --audio-dir : ne pas ajouter « public/ ». Les WAV sources et alignements sont dans public/n3-sem4/, les WAV avec pauses dans public/n3-sem4-paced/. Les plans et timelines sont dans src/video/n3-sem4-*.json. Les deux leçons sont dans le sélecteur du studio, avec leur fournisseur ElevenLabs correctement indiqué.

## Contrôles vérifiés

- VDP1 : 3 228 images, 107,605 s ; VDP2 : 3 053 images, 101,781 s.
- Deux MP4 1920 × 1080 à 30 i/s, H.264/AAC, décodés intégralement. Aucun intervalle noir inattendu ; crêtes audio −4,4 et −4,6 dB.
- Couverture des 32 diapositives et extraction de 92 repères dans les MP4 (47 et 45). Relecture visuelle des états d’objectif, propriétés, exemples, remarques, syllabes et vocabulaire.
- Les dix scènes contenant des formules passent la vérification de limites DOM dans le studio. Les deux aperçus et timelines modifiables se chargent sans débordement de page.
- scripts/check-n3-sem4.py vérifie les exemples et 961 couples numériques pour les identités sous leurs conditions. Les 14 débuts de prises correspondent à la piste AAC encodée, avec une corrélation minimale de 0,9998.
- Reconnaissance Whisper indépendante des huit scènes de propriété, exemple et vocabulaire dans l’AAC, sans transcription attendue. Les nombres et conditions sont cohérents avec les sources. Whisper small écrit « caussian » pour une occurrence de « quotient » et reconnaît mal sa lecture isolée. Une transcription Gemini indépendante (gemini-3.5-flash-lite), sans texte attendu, retrouve « quotient » dans ces deux passages. Résultats locaux dans reference/n3-sem4-vdp2/asr/gemini-review.json.
- Les trois segments syllabiques de « Radical » présentent du signal et des repères alignés. Les contrôles d’énergie et l’alignement ne certifient pas, à eux seuls, toute la prononciation.
- 18 tests du studio, TypeScript, 12 tests Google et build Next réussis. Le build signale cependant une mise à jour de sécurité à prévoir pour Next.js 16.4.4 ; aucun paquet n’a été mis à niveau pendant cette production.

Les reçus locaux sont verification.json, voice-review.json, review-frames.json, timeline.json dans outputs/n3-sem4/vdp1/ et vdp2/, ainsi que outputs/n3-sem4/ui-review.json. Ne pas confondre alignement d’un texte connu, reconnaissance indépendante et certification complète de la diction.

## Livraison vérifiée

Les deux MP4 ont été déposés par API dans « Livrable video / 3AC / Semaine 4 ». Les puces de fichiers publics ont été relues dans Sheets. Les identifiants Drive, les empreintes et les dossiers correspondent aux exports locaux. Une requête HTTP anonyme a obtenu le statut 206 et l’en-tête MP4 pour chaque vidéo.

- VDP1 : K8, N8–O8, 19/11/2026 à 16:27 (Casablanca) ; https://drive.google.com/file/d/1JyTj9dkPe69P_FubNGH961csKAHWctt_/view?usp=drivesdk
- VDP2 : K15, N15–O15, 19/11/2026 à 16:30 (Casablanca) ; https://drive.google.com/file/d/1POdDQZJpuVn4N6HBHAs1HITYKve8nSLX/view?usp=drivesdk

Les reçus de livraison sont dans outputs/n3-sem4/delivery.json. Pour une révision, utiliser files.update via google_vdp.py revise et conserver le même identifiant et la même puce ; ne pas créer un second MP4 dans Drive. Les statuts éditoriaux de la colonne J n’ont pas été modifiés.

## V2 · Correction de « Quotient » demandée par l’utilisateur

Le 19 novembre 2026, l’utilisateur a signalé le passage « Vocabulaire : Quotient » et confirmé que la correction porte sur la prononciation et l’animation. Cette demande remplace le choix de lecture entière de la V1. L’absence d’un média intégré ne dispense pas de reprendre le modèle simplifier.mp4 validé.

La séquence de la diapositive 12 montre une seule ligne : quo en bleu, puis tient en rouge. Les parties déjà révélées restent visibles. Le séparateur disparaît, la couleur devient uniformément bleue et les parties glissent pour former quotient. Aucun doublon du mot au-dessus, aucune indication phonétique et aucun cadre ajouté à cet insert autonome, conformément au modèle.

L’insert retenu utilise Google Kore, gemini-3.8-flash-lite-tts. Les guides vocaux Co et Cyan servent uniquement à produire les sons des deux parties écrites quo et tient ; l’écran conserve l’orthographe du mot. La lecture naturelle du mot entier suit les deux sons. L’amorce de production est coupée dans un silence pour que l’insert commence directement par la lecture syllabée. Le premier repère est à 0,50 s, le deuxième à 1,68 s et le mot entier vers 3 s. Le son est abaissé de 3 dB pour rejoindre le niveau de la leçon. L’insert dure 5,6 s et inclut 1,5 s de maintien après la fin du WAV. Les six autres scènes et leurs prises Soukaina sont identiques à la V1.

Les essais de diction ElevenLabs avec un dictionnaire phonétique restent des candidats locaux non retenus. Le support optionnel de dictionnaires dans elevenlabs-tts.mjs préserve les signatures des anciennes prises sans dictionnaire. L’API renvoie une Response à décoder avec json(). Aucun changement global de voix n’est déduit de cette correction.

### Reproduction de la V2

~~~powershell
python -X utf8 scripts/prepare-n3-sem4-vdp2-v2.py prepare
# Si la prise n’est pas déjà disponible, choisir GEMINI_TTS_MODEL=gemini-3.8-flash-lite-tts :
node scripts/gemini-tts.mjs src/video/n3-sem4-vdp2-v2-google-voice-plan.json
python -X utf8 scripts/align-n3.py src/video/n3-sem4-vdp2-v2-plan.json
python -X utf8 scripts/pace-n3.py --plan src/video/n3-sem4-vdp2-v2-plan.json --audio-dir n3-sem4-v2-kore-paced --output src/video/n3-sem4-vdp2-v2-paced-plan.json --gap-seconds 0.85
python -X utf8 scripts/prepare-n3-sem4-vdp2-v2.py timeline
npm run render:storyboards -- --stills n3-sem4-vdp2-v2
npm run render:storyboards -- n3-sem4-vdp2-v2
python -X utf8 scripts/verify-storyboard-batch.py n3-sem4-vdp2-v2
python -X utf8 scripts/check-quotient-revision.py
~~~

La préparation conserve les autres scènes et fournit src/video/n3-sem4-vdp2-v2-lesson.json. La prise brute est dans public/n3-sem4-v2-kore/, la prise avec pauses dans public/n3-sem4-v2-kore-paced/ et l’extrait final dans public/n3-sem4-kore-insert/. La même source et les mêmes alignements permettent de refaire l’extrait sans nouvel appel vocal. Le groupe week-four rend et vérifie maintenant la VDP1 initiale et cette VDP2 V2. La V1 de la VDP2 reste sélectionnable explicitement comme historique.

### Vérifications et livraison de la V2

Le MP4 P1_MATHS_N3_SEM4_VDP2_V2.mp4 compte 3 081 images et dure 102,72 s en 1080p30 H.264/AAC. Le décodage complet et 55 repères extraits ont été vérifiés, avec relecture des états avant la deuxième syllabe, des deux parties, de la transition et du mot réuni. Le pic audio est de −4,6 dB. Les sept débuts de prise correspondent à l’AAC encodé, avec une corrélation minimale de 0,9998. Le script vérifie aussi les six scènes conservées et l’extrait PCM, avec la coupe et le gain documentés. Les 19 tests et TypeScript passent.

La reconnaissance indépendante des sons isolés reste approximative : Whisper écrit notamment co-scient pour la prise Google et d’autres formes phonétiques pour les essais ElevenLabs. Ces sorties sont des éléments de revue, pas une certification de phonèmes. Les fichiers de comparaison sont conservés localement ; ne pas transformer l’alignement ou le signal en preuve d’une diction parfaite.

La V2 a remplacé le contenu du même fichier Drive par files.update. La puce publique K15 garde l’identifiant 1POdDQZJpuVn4N6HBHAs1HITYKve8nSLX. Le nom courant est P1_MATHS_N3_SEM4_VDP2_V2.mp4 et l’empreinte MD5 est 8bd7ba51e32401e393d65a9db3c9caec. Le dossier, la puce et les octets ont été relus. L’accès anonyme renvoie 206 et l’en-tête MP4. La première date et heure, le 19/11/2026 à 16:30 en N15–O15, sont conservées. Reçus, timeline et court aperçu audiovisuel : outputs/n3-sem4-v2/vdp2/.
