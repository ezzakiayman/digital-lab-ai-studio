# 2AC · Semaine 1 · VDP3 et VDP4

Les deux storyboards proviennent de « P1 / Semaine 1 » (gid 825019823). Les 13 et 17 diapositives ont été relues à partir d’une extraction OOXML et des images exportées par PowerPoint. Les originaux et images restent dans `reference/n2-sem1-vdp3/` et `reference/n2-sem1-vdp4/`.

| Leçon | Storyboard | Lien de première livraison | Contenu |
| --- | --- | --- | --- |
| VDP3 | F20 | K20 | Résoudre x² = a, avec a > 0 |
| VDP4 | F27 | K27 | Identifier les éléments d’un monôme |

La VDP3 garde la définition pendant les deux exemples et montre séparément les deux solutions et leurs vérifications. Pour x² = 36, la pause de réflexion dure au moins deux secondes. Voir le point d’interrogation approuvé avant l’affichage de 6 et −6. Les deux vérifications de x² = 2 affichent aussi les parenthèses autour de la racine avant de l’élever au carré.

La VDP4 oppose 4x²y³ à 2x + y, puis distingue le coefficient 4 et les variables x et y. Les exposants 2 et 3 sont repérés séparément au moment où la voix les nomme, avant le calcul 2 + 3 = 5. La synthèse révèle les quatre cartes dans l’ordre du storyboard. Les objectifs suivent l’ordre de flèches rouge puis vert de la charte.

## Narration et reproduction

La narration française utilise Kore. Gemini 3.1 Flash TTS a fourni les premières prises. Gemini 3.8 Flash-Lite TTS a produit la dernière synthèse après le quota de Flash et les prises contrôlées de « monôme » et « degré ». Pour l’objectif de la VDP4, une prise Eleven Flash en arabe standard porte uniquement « يتعرف ». Le montage coupe à 10,89 s la fin de la prise française mise en cache, où Kore avait ajouté une occurrence du mot. Après une nouvelle prise française, contrôler à nouveau le point de coupe avant de l’appliquer.

Les timelines éditables sont `src/video/n2-sem1-vdp3-lesson.json` et `src/video/n2-sem1-vdp4-lesson.json`. Les deux entrées figurent dans le studio. Avec les WAV locaux déjà préparés, relancer les commandes suivantes.

```powershell
python -X utf8 scripts/prepare-n2-sem1.py timeline
npm run render:storyboards -- --stills week-one
npm run render:storyboards -- week-one
python -X utf8 scripts/verify-storyboard-batch.py week-one
```

`scripts/prepare-n2-sem1.py prepare` reconstruit les plans de voix. L’étape `assemble --before-end 10.89` concerne la prise d’objectif mise en cache. Aligner le plan complet puis passer par `pace-n3.py` avec un intervalle de 0,70 s entre les idées. La durée spécifique `pauseAfter` du temps de réflexion est définie sur la question.

## Contrôles et livraison

Les MP4 durent 119,445 s et 152,576 s. Le décodage intégral en 1080p30 H.264/AAC, 72 repères encodés et la couverture des 30 diapositives ont été vérifiés. Les 10 séquences ont été comparées aux WAV dans l’AAC encodé. La reconnaissance indépendante de l’extrait arabe a retrouvé « يتعرف » une seule fois dans l’objectif assemblé. Les repères des syllabes et le signal de chaque segment ont été contrôlés. La reconnaissance automatique du passage français regroupe certaines syllabes isolées. Les 18 tests du studio, TypeScript et les 9 tests Google ont réussi.

Les deux MP4 ont été déposés dans « Livrable video / 2AC / Semaine 1 ». L’API Google a confirmé les liens en K20 et K27 et la concordance des empreintes avec les exports locaux.

Vérifié sur « P1 / Semaine 1 » en K20 et K27. Les deux cellules affichent le nom du MP4 via une puce Drive. Les identifiants des vidéos et les empreintes du contenu ont été confirmés. Une requête HTTP sans compte Google a lu l’en-tête MP4 des deux fichiers.

## Date et heure de première livraison

Sur « P1 / Semaine 1 », l’API a confirmé le 17/11/2026 à 12:46 en N20–O20 pour la VDP3 de 2AC, et le 17/11/2026 à 12:47 en N27–O27 pour la VDP4 de 2AC, en heure de Casablanca. Les puces K20 et K27 pointent vers les mêmes MP4 publics.


## 2AC · Semaine 1 · VDP4 · Storyboard révisé de 33 diapositives · 27 novembre 2026

Le fichier lié en F27 contient maintenant 33 diapositives. Le premier MP4 avait été produit à partir de 17 diapositives. La V2 reconstruit les dix séquences à partir du PowerPoint révisé. Le script français provient des 33 bandes vertes. La définition du degré conserve la condition « non nul ». L’objectif utilise la flèche rouge sous « Identifier », puis le soulignement vert seul. L’utilisateur a explicitement demandé de garder les deux occurrences de « Degré » sur la dernière diapositive.

Les lectures Mo–nôme et De–gré ont été recréées avec la voix française principale Gemini Kore, en fr-FR. La deuxième syllabe est verte et le mot réuni est bleu. Le microphone provient de l’illustration fixe de la mise en page. Les 39 passages de narration ou de prononciation ont été contrôlés dans l’AAC final. Les dix pistes correspondent à leurs WAV sans décalage mesuré. La comparaison indépendante des 33 états s’appuie sur 157 images du MP4. Les pauses naturelles des prises ont été conservées.

V2 livrée à 16 h 50, heure de Casablanca, sur le fichier public déjà lié en K27, « P1 / Semaine 1 ». La puce, les dates de première livraison, le dossier « Livrable video / 2AC / Semaine 1 », l’empreinte et la lecture anonyme du MP4 ont été vérifiés par API. Export de 4 250 images, 141,675 s, H.264/AAC 1920 × 1080 à 30 images/s. Décodage complet, crête −4,2 dB, MD5 318312d9645cef3f3d6a992a930b5fa7. Les 21 tests du studio et la vérification TypeScript passent.

### Reproduire la V2

La source attendue a pour SHA-256 4a70f4f3267284922bb9257f7060f622f8d63f6c16a8aff0523b88cbef3fba56. Pour une nouvelle installation, fournir ce PPTX et ses propres accès de synthèse. Les médias restent dans l’espace de production local.

```powershell
python scripts/voice-n2-sem1-vdp4-v2.py prepare --source $storyboard
$env:GEMINI_TTS_MODEL='gemini-3.8-flash-lite-tts'
node scripts/gemini-tts.mjs outputs/n2-sem1-vdp4-v2/voice-plan.json
python scripts/align-n3.py outputs/n2-sem1-vdp4-v2/voice-plan.json
python scripts/voice-n2-sem1-vdp4-v2.py timing
python scripts/prepare-n2-sem1-vdp4-v2.py $storyboard
npm run render:storyboards -- --stills --key-frames n2-sem1-vdp4-v2
npm run render:storyboards -- n2-sem1-vdp4-v2
python scripts/verify-storyboard-batch.py n2-sem1-vdp4-v2
```

La timeline du studio est src/video/n2-sem1-vdp4-v2-lesson.json. Une régénération vocale sur un autre compte exige un nouvel alignement et une nouvelle écoute. L’ancien script de la leçon à 17 diapositives sert à reproduire la première livraison. L’accord sur le mot « Degré » concerne seulement la diapositive 33 de cette source.
