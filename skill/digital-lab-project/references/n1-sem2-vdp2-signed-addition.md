# 1AC SEM2 VDP2 · Additionner avec la valeur absolue

Production du 12 novembre 2026 à partir de `P1_MATHS_N1_SEM2_VDP2.pptx`. Les 26 diapositives ont été inspectées et exportées en images. Le storyboard et les éléments de contrôle restent dans `reference/n1-sem2-vdp2/`.

| Diapositives | Séquence |
| --- | --- |
| 1–3 | Déclaration de l’objectif, signe de l’addition et valeur absolue de −5 |
| 4–12 | Règle 1, addition de deux entiers de même signe |
| 13–22 | Règle 2, signes contraires et valeurs absolues différentes |
| 23–26 | Règle 3, somme de deux entiers opposés |

Le bandeau d’objectif commence centré, monte puis présente les explications dans l’ordre rouge et vert. Les deux flèches descendent à la verticale depuis les soulignements. Le titre reste bleu marine sur une ligne de taille uniforme. Les titres « Règle » et « Illustration » utilisent la charte turquoise et se terminent par deux-points. Les consignes de réalisation et le texte des bandes de voix restent hors écran.

La règle 2 précise à l’écran et dans la voix que les valeurs absolues sont différentes. La règle 3 présente le cas des valeurs absolues égales avec des signes contraires. La mention résiduelle sur la comparaison de nombres négatifs et la lettre isolée de la diapositive 22 ont été écartées. Les exemples conservent les carrés et le triangle du storyboard. Le bleu des formes indique la valeur absolue, la taille distingue les deux valeurs absolues et la couleur du signe distingue le positif du négatif. Le signe de l’opération reste neutre. L’anneau orange repère d’abord le grand carré puis son signe au moment où la voix les désigne. Les points de suspension indiquent une valeur encore à calculer.

`SignedAddition.tsx` utilise le lecteur et la composition Remotion partagés. `signed-addition-lesson.json` est la timeline éditable. Elle contient 26 étapes et les repères d’animation associés aux mots prononcés. Les quatre enregistrements Google Gemini TTS Kore ont été contrôlés avec une transcription indépendante. L’alignement MMS_FA place les repères dans le son. Les pauses ajoutent 5,51 s de silence entre les idées. Un contrôle PCM confirme que les échantillons de parole d’origine sont conservés.

## Reproduction locale

Avec les enregistrements en cache, lancer depuis le projet.

```powershell
npm run render:storyboards -- --stills signed-addition
npm run render:storyboards -- signed-addition
python -X utf8 scripts/verify-storyboard-batch.py signed-addition
```

Pour renouveler les voix, préparer le plan avec `scripts/prepare-signed-addition.py` et utiliser `scripts/gemini-tts.mjs src/video/signed-addition-plan.json` avec le modèle `gemini-3.1-flash-tts-preview`. Lancer ensuite ces commandes.

```powershell
python -X utf8 scripts/align-n3.py src/video/signed-addition-plan.json
python -X utf8 scripts/pace-n3.py --plan src/video/signed-addition-plan.json --audio-dir signed-addition-paced --output src/video/signed-addition-paced-plan.json
python -X utf8 scripts/prepare-signed-addition.py --timeline
python -X utf8 scripts/check-paced-n3.py src/video/signed-addition-lesson.json
```


## Export vérifié

Le MP4 `outputs/n1-sem2-vdp2/P1_MATHS_N1_SEM2_VDP2.mp4` et sa timeline `outputs/n1-sem2-vdp2/timeline.json` couvrent les 26 diapositives. L’export compte 3 734 images en 1080p à 30 i/s et dure 124,48 s. Décodage intégral H.264 et AAC réussi. Le contrôle a extrait 39 images de l’export et une image juste avant le zéro pour vérifier sa révélation. Les identités des trois règles ont été vérifiées sur des valeurs absolues entières de 1 à 11. La reconnaissance vocale indépendante du MP4 confirme les trois règles. Une vérification ciblée retrouve la phrase sur le carré et le triangle, abrégée dans la première transcription automatique.

La compilation Next.js, les 18 tests unitaires, les contrôles du lecteur et de la mise en page sur ordinateur et mobile et la vérification des 141 références audio ont réussi.
