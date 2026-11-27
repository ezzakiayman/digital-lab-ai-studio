# 1AC · Semaine 3 · VDP1 · Expressions numériques

**Version courante : V5, prononciation Kore régénérée avec fr-FR explicite et métadonnées de diction française, sans média du PPT.** Les méthodes de réutilisation du clip décrites pour les V1–V3 sont historiques et remplacées par la consigne du 25 novembre.

Source vérifiée dans « P1 / Semaine 3 » (gid 1754986894), cellule F4. Le fichier P1_MATHS_N1_SEM3_VDP1.pptx contient 23 diapositives. Le fichier et les images sources sont conservés dans reference/n1-sem3-vdp1/. La lecture a croisé les formes OOXML, les images PowerPoint et la relation média de la diapositive 19.

La déclaration conserve l’objectif « Additionner et soustraire dans des expressions numériques ». L’explication utilise les signes plus et moins du storyboard, avec des soulignements rouge, vert et mauve. Le soulignement mauve accompagne la phrase en arabe dans la voix. Le développement du storyboard porte sur les suites d’additions et leurs termes. L’exemple (+7) + (−15) + (+5) souligne d’abord les deux opérateurs, puis entoure les trois nombres signés séparément. Le vocabulaire conserve l’exemple (−6) + (+4) + (−3).

La voix française est Gemini Kore, avec une prise Eleven Flash AR séparée pour la phrase « سنتعرّف عليها خلال هذه الحصّة ». L’animation et l’audio du mot « Expression » proviennent du clip MP4 intégré à la diapositive 19. La lecture du PowerPoint l’identifie en ppt/media/media1.mp4. Le clip s’affiche dans le cadre Vocabulaire et sa piste d’origine débute au même repère que l’image.

## Rendu avec les prises disponibles

```powershell
python -X utf8 scripts/prepare-n1-sem3-vdp1.py timeline
npm run render:storyboards -- --stills n1-sem3-vdp1
npm run render:storyboards -- n1-sem3-vdp1
python -X utf8 scripts/verify-storyboard-batch.py n1-sem3-vdp1
```

L’étape prepare crée le plan complet et les plans vocalisés distincts. L’étape assemble joint la prise française de l’objectif à la prise arabe. Utiliser align-n3.py avec src/video/n1-sem3-vdp1-plan.json, puis pace-n3.py avec n1-sem3-vdp1-paced et un intervalle de 0,68 s entre idées. L’étape timeline utilise le clip extrait à reference/n1-sem3-vdp1/prononciation-expression.mp4. Le montage du clip démarre sur un repère exact en images et conserve le son PCM du clip.

## Vérification et livraison

Le MP4 de 120,213 s contient 3 606 images en 1920 × 1080 à 30 i/s, H.264 et AAC. Le décodage complet, la couverture des 23 diapositives et 39 repères dans le fichier encodé ont été contrôlés. La première définition a été reformulée en « Une suite d’additions de nombres est une expression numérique » pour lever une ambiguïté de diction. La reconnaissance indépendante de la version finale a confirmé cette formulation, les nombres signés dans les exemples et la phrase arabe. L’audio de la prononciation intégrée correspond aux échantillons source et à la piste AAC. Les 18 tests du studio et TypeScript ont réussi.

La puce publique a été relue en K4 dans « P1 / Semaine 3 ». L’API a vérifié l’empreinte du fichier dans « Livrable video / 1AC / Semaine 3 ». Une requête anonyme a confirmé l’accès au MP4. N4 et O4 affichent le 17/11/2026 et 17:49, heure de Casablanca.

## V2 · révision de l’inspecteur · 24 novembre 2026

L’utilisateur a demandé de commencer par Revision_Video_P1_MATHS_N1_SEM3_VDP1 (1).docx. Son SHA256 est identique à la pièce déjà archivée avec le suffixe (1) (1). Les deux demandes sont traitées : nouvelle prise arabe de l’objectif pour حصة, et signe d’opération + noir entre (+4) et (−3) dans le vocabulaire. Aucun texte de narration arabe n’est ajouté à l’écran. Le générateur initial conserve également le signe d’opération noir pour les préparations futures ; la timeline et l’export V1 restent archivés.

La V2 est reproductible avec scripts/revise-n1-sem3-vdp1.py : prepare écrit le plan arabe, build insère la prise isolée dans le PCM original et applique la couleur, check contrôle la conservation des prises et leur présence dans l’AAC. La nouvelle prise reprend le profil Eleven Flash v2.5, langue ar, Soukaina, vitesse 0,94 et stabilité 0,45. La voix française Kore et les six autres pistes restent inchangées. Tous les repères antérieurs au remplacement sont conservés ; les scènes suivantes se décalent de cinq images. Ne pas relancer le générateur initial pour remplacer cette V2.

```powershell
python -X utf8 scripts/revise-n1-sem3-vdp1.py build
npm run render:storyboards -- --stills --key-frames n1-sem3-vdp1-v2
npm run render:storyboards -- n1-sem3-vdp1-v2
python -X utf8 scripts/verify-storyboard-batch.py n1-sem3-vdp1-v2
python -X utf8 scripts/revise-n1-sem3-vdp1.py check
```

Sortie outputs/n1-sem3-vdp1-v2/P1_MATHS_N1_SEM3_VDP1_V2.mp4 : 3 611 images, 120,384 s avec padding AAC, 1080p30 H.264/AAC. Décodage intégral, 23 diapositives, 39 repères encodés, 19 tests et TypeScript réussis. Les aperçus et l’image encodée du passage corrigé montrent le + noir. Whisper small sans texte attendu retrouve le mot arabe demandé dans la prise isolée et l’AAC final. Ce contrôle ne certifie pas intégralement la phonétique. Le PCM français conservé est identique ; les sept débuts de scènes correspondent à l’AAC, la corrélation du nouvel insert arabe est 0,9995 et celle du clip de prononciation original 0,9999.

La révision remplace le même fichier Drive, avec puce publique K4 inchangée en identifiant. Empreinte b3928997e17f85cc68ddb6fc359dd3ef ; en-tête MP4 vérifié anonymement en HTTP 206. Aucun nouveau fichier Drive. N4/O4 sont strictement conservées. Attention : la relecture du 24 novembre affiche 17/11/2026 et 16:49, alors que le compte rendu initial ci-dessus mentionnait 17:49 Casablanca ; ne pas réécrire ces cellules sur la base de cette ancienne note. Les autres fiches de l’inspecteur restent en attente.


## Écart au script confirmé · contrôle du 25 novembre 2026

Après le signalement de l’utilisateur, une comparaison ciblée du PowerPoint original avec le plan et les textes de la VDP1 1AC semaine 3 confirme des reformulations dans la première définition (diapositive 6), dans la définition des termes (12), ainsi que la suppression d’une répétition vocale en 4. Les deux définitions ont changé dans la narration et à l’écran. Ces écarts sont antérieurs à la V2 ; la correction du 24 novembre conservait exactement le français existant et les a donc conservés aussi. La fidélité intégrale au script n’est pas acquise malgré les contrôles audio, graphiques et techniques réussis. Les constatations détaillées restent locales dans outputs/n1-sem3-vdp1-v2/script-fidelity-findings.json. Ce contrôle ciblé ne conclut pas sur toutes les productions.

État : écarts constatés, non restaurés. Aucun MP4, audio, générateur ou lien Google n’est modifié par cet audit. Avant une prochaine production/révision concernée, faire le relevé source/narration/texte visible et présenter les écarts ; conserver les formulations source. Toute reformulation pédagogique, correction de répétition ou modification éditoriale exige une décision explicite de l’utilisateur, même si elle paraît améliorer la diction.


## V3 · restauration du script source · 25 novembre 2026

L’utilisateur a demandé de corriger cette première vidéo après avoir rendu intouchables la narration et le contenu du storyboard. Le PowerPoint de F4 a été récupéré à nouveau via les API ; ses octets sont identiques à la source archivée. Le contrôle a porté sur les 23 bandes de voix off, les deux définitions visibles, les exemples signés et le vocabulaire, et non seulement sur les trois écarts initiaux. Les formulations source sont rétablies, y compris la répétition présente dans l’objectif. La V3 conserve la prise arabe حصة validée en V2, le + noir de vocabulaire et l’image/son du clip « Expression » de la diapositive 19.

scripts/restore-n1-sem3-vdp1.py extrait directement la source OOXML avec les textes mathématiques OMML et leur rôle. Il bloque une narration réécrite, une répétition supprimée et les anciennes définitions visibles. Les seules conversions de lecture sont enregistrées dans outputs/n1-sem3-vdp1-v3/source-audit.json : glyphes numériques normalisés, notation signée lue oralement et développement des ordinaux abrégés. Les aides de diction restent dans les plans techniques, hors contenu visible. La première définition utilise une pause de lecture après son premier mot ; aucun mot n’est remplacé. La prise initiale ambiguë et les essais sont conservés comme historiques locaux, la prise retenue est identifiée dans le reçu dictionParts.

Les sept séquences utilisent Kore en français, avec la prise arabe séparée inchangée. Le clip source conserve son audio exact. Toutes les cues ont été recalculées après génération et pauses. La source de la V3, le plan modifiable et la timeline sont distincts de ceux des V1/V2 ; ne pas réexécuter le générateur initial pour remplacer la V3.

```powershell
python -X utf8 scripts/test_restore_n1_sem3_vdp1.py
python -X utf8 scripts/restore-n1-sem3-vdp1.py timeline
npm run render:storyboards -- n1-sem3-vdp1-v3
python -X utf8 scripts/verify-storyboard-batch.py n1-sem3-vdp1-v3
python -X utf8 scripts/restore-n1-sem3-vdp1.py check
```

Ces commandes réutilisent les prises/alignements déjà sélectionnés. Pour de nouvelles prises, prepare et assemble précèdent align-n3.py ; diction conserve le début validé et utilise la recette de pause retenue ; refaire l’alignement avant pace-n3.py, puis timeline. L’étape diction exige le reçu/alignement de première prise, ne pas improviser de coupe sans ceux-ci.

Export : outputs/n1-sem3-vdp1-v3/P1_MATHS_N1_SEM3_VDP1_V3.mp4, 3 798 images, 126,613 s avec padding AAC, 1080p30 H.264/AAC. Décodage intégral, 23 diapositives et 38 repères encodés vérifiés. Les deux définitions et l’opérateur noir ont été examinés dans l’encodage. Les 19 tests du studio, quatre nouveaux tests de fidélité et TypeScript passent. La reconnaissance indépendante des six scènes françaises et de l’arabe dans l’AAC retrouve les formulations, répétitions et nombres signés attendus ; les variations orthographiques d’homophones ne certifient pas la phonétique. Une transcription secondaire vérifie l’amorce articulée de la première définition et la répétition finale de l’objectif. Une fausse fin de sous-titrage produite par Whisper sur le silence de l’objectif n’est pas reprise par la transcription secondaire et n’a motivé aucune réécriture du contenu. Les sept débuts de prises, l’arabe et le clip d’origine correspondent à l’AAC avec une corrélation supérieure à 0,99.

La V3 remplace le même fichier Drive public ; puce K4 relue, empreinte 3c1ab05fa1ebd19fbff02f51e08ef9a7 identique au fichier local, en-tête MP4 anonyme HTTP 206. Les cellules N4/O4 restent strictement identiques : 17/11/2026 et 16:49 affichés. La V2 et le constat de divergence antérieur restent des archives historiques ; les écarts signalés sont restaurés dans la V3. Aucun des cinq autres dossiers inspecteur n’est modifié.


## V4 · vocabulaire avec la voix principale · 25 novembre 2026

L’utilisateur interdit désormais la réutilisation du clip ou de l’audio de vocabulaire inclus dans le PPT et demande une nouvelle génération avec la même voix que le reste de la vidéo. La V4 remplace uniquement la scène de prononciation « Expression ». Les six autres scènes sont identiques à la timeline V3 rendue : script restauré, définitions, arabe et + noir sont conservés.

scripts/replace-n1-sem3-vdp1-pronunciation.py prépare une nouvelle prise Gemini 3.8 Flash Lite TTS Kore, modèle et voix identiques aux prises françaises de la leçon. Le début vocal source déjà généré avec Kore reste identique en PCM. Les aides phonétiques sont uniquement des métadonnées ; l’image affiche Ex, pre, ssion, puis leur réunion en Expression. Les parties et le mot entier sont lus avec de courtes pauses. La ligne native réutilise PronunciationLine et les largeurs Arial Bold mesurées à 64 px. Pendant le début vocal, le mot source est visible, puis laisse place à la révélation et réunion. Le rendu ne référence aucun clip de PPT ni sa piste sonore.

```powershell
python -X utf8 scripts/replace-n1-sem3-vdp1-pronunciation.py timeline
npm run render:storyboards -- n1-sem3-vdp1-v4
python -X utf8 scripts/verify-storyboard-batch.py n1-sem3-vdp1-v4
python -X utf8 scripts/replace-n1-sem3-vdp1-pronunciation.py check
```

Les prises et alignements retenus sont en cache. Pour une nouvelle prise, prepare précède Gemini TTS, align-n3.py et pace-n3.py avec le répertoire relatif n1-sem3-vdp1-v4-paced et 0,75 s entre les unités, puis timeline. Le contrôle des scènes préservées compare les timelines rendues après validation Zod : le champ de préparation pauseAfter a déjà été appliqué au PCM et est retiré par ce schéma.

Export outputs/n1-sem3-vdp1-v4/P1_MATHS_N1_SEM3_VDP1_V4.mp4 : 3 673 images, 122,453 s avec padding AAC, 1080p30 H.264/AAC. Décodage complet, 23 diapositives et 50 repères extraits vérifiés techniquement ; phases syllabiques et mot réuni examinés dans le MP4. Les 19 tests du studio, quatre tests de fidélité source et TypeScript passent. Identité des six autres scènes, fournisseur/voix/modèle, PCM du début et nouvelle prise dans l’AAC vérifiés. La corrélation du nouvel insert est 0,9997. L’ASR local retrouve les syllabes et le mot dans la prise brute ; le passage encodé complet omet les unités isolées, un contrôle borné les retrouve avec une transcription approximative. Ces sorties ne certifient pas précisément chaque phonème.

Même fichier Drive public et puce K4 ; MD5 d2e46ddacd6ce888a3663e2220a5cd8b et en-tête MP4 anonyme HTTP 206 vérifiés. N4/O4 inchangées. La V3 reste historique. Les autres vidéos ne sont pas révisées automatiquement par cette nouvelle règle.

À la demande d’un rapport de workflow avec temps, workflow-timings.json distingue les commandes chronométrées et les intervalles reconstruits par horodatages de fichiers. Ne pas additionner les sous-mesures qui se chevauchent, ni présenter le temps TTS comme le temps total. La lecture initiale n’a pas été chronométrée ; le parcours de production tracé commence à la création du script de révision et se termine à la livraison vérifiée. Le rapport destiné à l’utilisateur documente ces limites.


Rapport de workflow enrichi à la demande de l’utilisateur : le même fichier outputs/n1-sem3-vdp1-v4/Rapport-workflow-et-temps-V4.html contient maintenant 15 fiches et 67 opérations, avec entrées, traitement, sorties, critères/limites, temps disponibles et distinction automatisation/relecture de l’agent. Trois images du MP4 sont intégrées au HTML pour la lecture hors connexion ; les anciens temps sont conservés sans être réinterprétés comme des mesures CPU. Navigation et fichiers de preuve vérifiés ; empreinte MP4 inchangée. Données détaillées dans workflow-steps-detailed.json. Cette tâche ne modifie aucune vidéo, voix, timeline de production ni donnée Google. Synchronisation locale des références ; aucune publication GitHub.


Le rapport V4 précise désormais un budget pour chacune des 15 étapes. Ces fourchettes sont explicitement des estimations de préparation pour une correction similaire, avec vidéo/source déjà contrôlées et runtime en cache, pas un découpage mesuré a posteriori. Budget séquentiel indicatif : environ 20 à 40 minutes, rapport compris ; les mesures historiques restent inchangées dans workflow-timings.json. Les budgets sont sauvegardés séparément dans workflow-planning-estimates.json et affichés dans chaque fiche. Aucun MP4, audio ou fichier Google modifié par cette mise à jour documentaire.


## V5 · accent français explicite · 25 novembre 2026

L’utilisateur signale un accent anglais dans le vocabulaire Expression en V4. Ce signalement prime sur la validation antérieure de l’identifiant Kore : un même identifiant de voix et une transcription correcte ne prouvent pas l’accent. La V4 n’avait pas fixé de langue pour ses sons isolés. La V5 régénère la scène avec son introduction source française complète, languageCode fr-FR et des indications de diction française dans speechMetadata.style, sans ajouter ces instructions au texte prononcé. Les parties écrites et l’animation native V4 sont conservées ; les six autres scènes sont identiques à la V4 rendue. Aucun contenu du script n’est reformulé et aucun média PPT n’est utilisé.

scripts/gemini-tts.mjs accepte désormais languageCode et speechStyle par scène, transmet le style comme métadonnée, et inclut ces options dans la signature de cache. Les signatures historiques sans ces options restent identiques. Deux tests dans scripts/test-gemini-tts-signature.mjs vérifient cette compatibilité et le rejet d’un ancien cache quand langue/style changent. La nouvelle prise et ses repères se reproduisent avec scripts/french-n1-sem3-vdp1-pronunciation.py prepare, le générateur Gemini, align-n3.py, pace-n3.py (n1-sem3-vdp1-v5-paced, 0,75 s), puis timeline. Pour le cache sélectionné, utiliser timeline, render:storyboards n1-sem3-vdp1-v5, verify-storyboard-batch.py n1-sem3-vdp1-v5 et le contrôle check du script de V5.

Le nouvel export contient 3 682 images, 122,752 s avec padding AAC, 1080p30 H.264/AAC. Décodage intégral, 23 diapositives, 48 repères extraits, parties/mot réuni encodés examinés, six scènes conservées et présence de la prise dans l’AAC vérifiés. Les 19 tests du studio, les deux tests de cache et TypeScript passent. La reconnaissance indépendante brute et encodée détecte fr avec probabilité supérieure à 0,999 ; un second contrôle audio, sans texte attendu ou IPA fournis au modèle, relève une prononciation française du mot final et ses voyelles nasales. Ce sont des contrôles assistés, pas une certification humaine de chaque phonème. Le reçu enregistre explicitement fr-FR et le style français.

La V5 remplace le même fichier Drive public : puce K4 relue, MD5 3a822dd27b1929a2ff5413cc9538b847, en-tête anonyme HTTP 206. N4/O4 inchangées. La règle d’accent français pour les passages français est enregistrée dans les six points d’entrée et les références ; l’arabe garde son profil de الفصحى et n’est pas forcé en français.

Documentation primaire vérifiée : [SpeechConfig et SpeechMetadata](https://aistudio.google.com/api-reference/generate-content), [génération vocale et langue explicite](https://firebase.google.com/docs/ai-logic/generate-speech?api=dev). Les métadonnées de style ne remplacent pas la revue du son.
