# Remise d’un montage After Effects

Pour la leçon « Identifier les éléments d’un monôme », le projet source se trouve dans `outputs/n2-sem1-vdp4-v2/after-effects/`. Remettre le ZIP en entier. Une fois extrait, son fichier `.aep` s’ouvre directement dans After Effects. Le fichier `LIRE-MOI.txt` guide le monteur jusqu’à la séquence, au repère et au calque qu’il veut modifier. Chaque séquence possède sa propre voix. Le MP4 livré sert de guide de comparaison désactivé.

## Étape standard de production

Pour chaque nouvelle vidéo VM ou VDP et chaque révision livrée, effectuer cette étape après la vérification du MP4. En lot, traiter chaque vidéo avec sa propre timeline et ses propres médias.

1. Repartir de la timeline finale, des WAV et des illustrations de la version vérifiée.
2. Générer un .aep natif avec des séquences nommées et des repères de diapositives. Garder les textes, formules, flèches, formes et images clés modifiables. Placer la voix de chaque séquence sur son propre calque.
3. Collecter les médias par chemins relatifs dans le ZIP de la version, avec un guide d’ouverture. Inclure le MP4 validé comme calque guide désactivé et muet.
4. Vérifier le ZIP après extraction dans un autre dossier et comparer le contenu et le minutage au MP4 livré. Indiquer si la lecture dans Adobe a été contrôlée.
5. Remettre le ZIP via un canal privé et consigner son chemin et les contrôles dans le handoff. Le MP4 reste le fichier de livraison suivi dans Sheets.

## Reconstruction depuis les sources de production

Ce premier export couvre la composition V2 de la VDP4 de 2AC, semaine 1. Il exige la timeline validée, les dix WAV locaux, les illustrations et le MP4 de référence. La référence de la compétence Digital Lab `n2-sem1-vdp3-vdp4.md` décrit comment retrouver ou générer ces éléments à partir du storyboard révisé. Les vidéos, les polices système et les sources pédagogiques privées restent dans l’espace de production.

Depuis la racine du projet sur le poste de production, exécuter la capture et la collecte, puis écrire le projet natif dans un nouveau dossier. Le script Python d’écriture utilise `py-aep==0.20.0`. L’installer dans un environnement Python isolé avec Pillow. Les commandes suivantes supposent les dépendances du studio déjà installées.

```powershell
$work = 'outputs/n2-sem1-vdp4-v2/after-effects-work'
$source = 'outputs/n2-sem1-vdp4-v2/after-effects/P1_MATHS_N2_SEM1_VDP4_V2'
node scripts/after-effects/capture.mjs src/video/n2-sem1-vdp4-v2-lesson.json $work
python scripts/after-effects/collect.py "$work/capture.json" --dest $source
python scripts/after-effects/write-aep.py $source
Copy-Item scripts/after-effects/build-project.jsx -Destination $source
```

Le projet cible le format de fichier After Effects 22.6. Les calques de texte et les tracés animés sont natifs. La cible, le microphone et l’ombre du bandeau sont des illustrations PNG. Les lettres, chiffres et exposants qui s’animent séparément sont modifiables individuellement. Le fichier `project.json` contient les propriétés éditables, leur minutage et la correspondance des médias. Le script JSX permet au monteur de recréer et enregistrer le montage dans son installation d’After Effects.

## Création du ZIP

Rédiger LIRE-MOI.txt dans le dossier de remise. Indiquer le nom du .aep à ouvrir, les compositions à modifier et les polices nécessaires. Utiliser un dossier de remise dédié à cette version et vérifier son contenu avant compression.

```powershell
$archive = "$($source)_After_Effects.zip"
Compress-Archive -LiteralPath $source -DestinationPath $archive
```

## Vérification

Contrôler le fichier natif et ses médias après extraction du ZIP dans un autre dossier. Comparer les compositions, les points d’entrée et de sortie, les calques de texte, les tracés, les images clés, les repères et les dix WAV avec la livraison validée. Relire les états des animations sur des images extraites de la vidéo. Pour contrôler le rendu propre à Adobe, ouvrir la composition principale sur un poste équipé d’After Effects et comparer avec le calque guide.

```powershell
python scripts/after-effects/check-package.py $archive --timeline src/video/n2-sem1-vdp4-v2-lesson.json --reference outputs/n2-sem1-vdp4-v2/P1_MATHS_N2_SEM1_VDP4_V2.mp4 --native --out "$work/qa"
```

Les scripts de capture et de collecte contiennent des références propres à la VDP4 V2. Pour une autre leçon, identifier et adapter le composant capturé, la timeline, le nom de la composition, les médias, les repères et le MP4. Contrôler la prise en charge des éléments graphiques de cette leçon. Le générateur natif utilise le fichier project.json collecté.

