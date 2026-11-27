# 1AC · Semaine 2 · Propriétés de l’addition et soustraction

Le lot validé le 16 novembre 2026 couvre deux lignes VDP de l’onglet « P1 / Semaine 2 » du suivi Digital Lab (gid 1191794673).

| Leçon | Storyboard | Diapositives | Séquences | MP4 | Lien du suivi |
| --- | --- | ---: | ---: | --- | --- |
| VDP3 · Commutativité et associativité de l’addition | F17 | 30 | 8 | `outputs/n1-sem2-vdp3/P1_MATHS_N1_SEM2_VDP3.mp4` · 180,907 s | K17 |
| VDP4 · Soustraction de nombres entiers | F24 | 19 | 6 | `outputs/n1-sem2-vdp4/P1_MATHS_N1_SEM2_VDP4.mp4` · 85,077 s | K24 |

F17 pointait vers un fichier à la corbeille. Une copie active de même nom et de même empreinte a été retrouvée, téléchargée, puis reliée en F17 sous forme de puce Drive. Le PowerPoint en F24 est actif et contient 19 diapositives même si J24 indiquait « Pas de storyboard » à la lecture. Les colonnes de statut n’ont pas été modifiées. Le lien K10 de la VDP2 ouvre une VDP de 3AC. Ce point est distinct du lot produit.

## Production

- Le storyboard de VDP3 souligne en vert le nom des deux propriétés sans explication visuelle. Le composant partagé affiche le soulignement seul à ce repère. Le verbe « Utiliser » garde son explication en deux lignes et sa flèche rouge. Le calcul des deux groupements montre −1 et +1 comme résultats intermédiaires, puis −3 de part et d’autre. Les deux résultats de la commutativité valent 3.
- VDP4 préserve l’exemple −5 et 5 et distingue le signe d’opération du signe de l’entier. Des points de suspension indiquent la place de l’opposé de +10 lors de la réécriture, puis (−10) apparaît. La vidéo conserve le point d’arrêt du PowerPoint après la transformation en addition de l’opposé.
- La voix est Gemini Kore. Deux scènes utilisent Flash-Lite et les autres Flash. L’ASR a confirmé les nombres et les étapes essentielles. Pour l’amorce d’« associativité », le lot a repris le préfixe vérifié « Écoutez la prononciation du mot » de la prise de commutativité. Il l’a assemblé avec le mot isolé et une prise séparée contenant les six syllabes et le mot entier. L’amorce et la prise syllabique ont été contrôlées séparément, puis les six repères ont été recalculés sur la prise assemblée.
- La validation source couvre 49 diapositives. Le décodage intégral des deux MP4 H.264/AAC 1080p30 n’a détecté aucun noir inattendu. Le contrôle a extrait 52 et 28 repères encodés, avec inspection visuelle des étapes clés. TypeScript, 18 tests et l’ouverture locale des deux leçons dans le studio ont passé. La commande de build Next.js a signalé une alerte de sécurité intégrée après compilation et génération des pages. Les MP4 proviennent de Remotion.

## Reproduction et livraison

Les timelines éditables sont dans `outputs/n1-sem2-vdp3/timeline.json` et `outputs/n1-sem2-vdp4/timeline.json`. Les scènes et les traces d’alignement sont préparées via `scripts/prepare-n1-sem2.py`. Sur le poste où les voix sont en cache, le parcours de rendu est le suivant.

```powershell
npm run render:storyboards -- --stills n1-sem2-vdp3 n1-sem2-vdp4
npm run render:storyboards -- n1-sem2-vdp3 n1-sem2-vdp4
py -3.12 -X utf8 scripts/verify-storyboard-batch.py n1-sem2-vdp3 n1-sem2-vdp4
```

Les fichiers sont déposés dans « Livrable video / 1AC / Semaine 2 » via l’API Drive. Les cellules K17 et K24 ont été relues et chaque empreinte Drive correspond au MP4 local. Pour une correction, utiliser `revise --gid 1191794673 --link-version 1` avec la cellule storyboard et le nouveau numéro de fichier, afin de conserver le lien Drive.


## V2 · 1AC semaine 2 VDP4 · Signe du cinq positif · 26 novembre 2026

La correction autorisée ajoute le signe + devant le cinq positif dans la paire de nombres et dans la conclusion de l’exemple des opposés. Les deux valeurs absolues restent 5. Les timecodes fournis 01:25–02:25 ne correspondent pas à la durée actuelle de 85,077 s ; les passages ont été identifiés par leur contenu vers 00:23–00:41. Source PPTX API identique au fichier local de 19 diapositives ; vidéo publiée avant révision identique au MP4 local, MD5 1107769ae420cf21bac1f690197b518e.

Deux seuls champs visuels sont modifiés dans src/video/n1-sem2-vdp4-v2-lesson.json. Les cinq autres scènes, les six narrations, les WAV, toutes les durées et la piste AAC entière sont inchangés ; comparaison AAC octet par octet réussie. Aucune génération TTS. Cette révision ciblée ne certifie pas à nouveau la fidélité mot pour mot de tout le contenu historique. Reproduction : scripts/fix-n1-sem2-vdp4-plus-v2.py prepare ; rendu n1-sem2-vdp4-v2 ; verify-storyboard-batch.py ; étape check ; scripts/deliver-n1-sem2-vdp4-v2.py. Les assertions refusent toute différence autre que ces deux signes et protègent les valeurs absolues.

Export outputs/n1-sem2-vdp4-v2/P1_MATHS_N1_SEM2_VDP4_V2.mp4 : 2552 images, 85,077 s, H.264/AAC 1080p30, crête −4,2 dB. TypeScript, décodage intégral, couverture des 19 diapositives et absence de noir inattendu vérifiés. Trente-quatre repères encodés extraits ; paire, valeurs absolues et conclusion inspectées dans le MP4. Même fichier public révisé via API en K24, onglet P1 / Semaine 2, Livrable video / 1AC / Semaine 2 ; puce, MD5 ad22a2bfbaafdf6afd31c3d196a71c13, 5149397 octets, accès anonyme HTTP 206 et dates N24/O24 conservées vérifiés à 2026-11-26T18:15:45.702722+01:00.

Le rapport illustré réconcilie aussi le choix limitée de N3 SEM3 VDP4 V7 déjà livré : 41 points, 27 images originales, 39 traités et deux clarifications restantes (glyphe a et flèche non périodique). Aucun autre MP4 n’est modifié. Compétences Digital Lab synchronisées dans les trois copies locales ; aucun dépôt Git présent dans le projet ou le miroir, aucune publication GitHub.
