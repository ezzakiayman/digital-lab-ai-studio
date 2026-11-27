# Base de connaissances Digital Lab

### Accent français obligatoire pour le français

Pour Digital Lab, les mots et phrases français doivent toujours être prononcés avec un accent français naturel, y compris les syllabes et le mot entier du vocabulaire. Ne pas accepter une lecture anglaise d’un mot français. Conserver la voix principale validée de la vidéo ; son identifiant seul ne garantit pas la langue ou l’accent.

Pour une nouvelle prise française Gemini, renseigner explicitement languageCode = fr-FR et placer les indications de diction/accent dans speechMetadata.style, jamais dans le texte à prononcer. Générer le passage avec son contexte français source plutôt qu’une suite de seuls sons isolés en langue automatique. Les autres langues gardent leur profil approuvé, notamment l’arabe standard ; ne pas les forcer en français.

Inclure langue et style dans la signature du cache pour qu’un changement de diction ne reprenne pas la prise fautive. Vérifier le mot final et les unités isolées par une écoute ou un contrôle acoustique ciblé ; une transcription écrite en français ou un reçu Kore ne certifie pas à lui seul l’accent. Aucune reformulation du contenu n’est autorisée pour résoudre un problème de diction.

Consulter cette référence avant de préparer ou de réviser une vidéo VM ou VDP. Elle rassemble les décisions de production issues des corrections de l’utilisateur. Les références de chaque leçon documentent les timecodes, les choix propres au storyboard et les contrôles effectués.

## Du storyboard à l’écran

### Règle prioritaire — voix off et contenu du storyboard intouchables

Consigne explicite de l’utilisateur, 25 novembre 2026 : le texte de la voix off et le contenu pédagogique du storyboard sont intouchables. Reproduire les formulations source mot pour mot, en conservant définitions, exemples, nombres, signes, symboles, conditions, répétitions et ordre des étapes. Ne pas reformuler, simplifier, résumer, ajouter ou supprimer du contenu pour rendre le discours plus naturel, faciliter le TTS ou corriger soi-même une erreur supposée.

Seule une correction précise demandée ou explicitement approuvée par l’utilisateur autorise à modifier le passage concerné. Un accord général pour produire, améliorer ou réviser une vidéo ne donne pas cette autorisation. Signaler toute incohérence ou difficulté de diction sans la corriger silencieusement ; une fiche d’inspecteur reste une demande à examiner, pas une permission autonome de réécrire.

Les pauses, la prononciation, la mise en page et l’animation peuvent être ajustées dans le cadre des consignes approuvées, sans changer les mots prononcés ni le contenu. Garder les aides phonétiques dans les métadonnées de préparation et les bandes de production hors image. Avant génération ou publication, comparer séparément la narration prévue à la bande de voix off source et les textes/formules visibles à la zone pédagogique source. Un alignement forcé ou un décodage réussi ne valide pas cette fidélité. Cette règle prévaut sur les anciennes initiatives de reformulation documentées dans les références.

- La bande verte du haut fournit la voix off. La bande du bas fournit les consignes d’animation. Afficher le contenu pédagogique issu de la zone centrale. Les instructions de production restent hors image et hors narration.
- Relire les calculs et les formulations. Conserver les étapes de raisonnement, les exemples du storyboard et les conditions qui rendent chaque affirmation vraie. Lors d’un désaccord entre le contenu et l’objectif, relever le passage précis avant de choisir une formulation.
- Comparer une fiche de révision au MP4 réellement examiné. Vérifier les corrections déjà présentes et repérer chaque scène dans la timeline. Quand l’utilisateur envoie plusieurs consignes successives, confirmer chacune et respecter son feu vert avant la production.

Contrôle de fidélité obligatoire avant un prochain rendu : comparer séparément la voix prévue à la bande de narration et les textes visibles à la zone pédagogique du storyboard. Consigner les écarts et les soumettre avant toute reformulation, même pour améliorer la diction ou enlever une répétition. Les contrôles de décodage, de synchronisation et de présence audio ne prouvent pas la fidélité au script. Le contrôle ciblé du 25 novembre de la VDP1 1AC semaine 3 a confirmé deux définitions reformulées et une répétition supprimée ; ces écarts restent à traiter.

## Production et livraison des VDP

Pour lire Google Sheets, récupérer un storyboard, accéder à Drive, déposer un MP4 ou écrire son lien, utiliser un connecteur autorisé ou les API Google. L’utilisateur exclut le pilotage de son PC et de son navigateur pour ce circuit.

1. Dans le tableau de suivi « MATH College Digital Lab Intern », ouvrir l’onglet de la semaine et repérer la ligne « Définition » par niveau, leçon et nom du fichier VDP. Ouvrir le PowerPoint lié dans la colonne « Storyboard ». Le tableau sert de point d’entrée au script. Vérifier le niveau et la semaine avec le nom du fichier, surtout si la colonne « Semaine » est incohérente.
2. Produire et vérifier le MP4 final d’après le storyboard. Nommer le MP4 d’après le storyboard afin de retrouver le même identifiant dans le tableau et dans Drive. Générer le [projet source After Effects](#projet-source-after-effects) de cette version.
3. À la première livraison, créer le fichier MP4 dans « Livrable video », au niveau puis à la semaine correspondants. À chaque correction, envoyer le nouveau MP4 comme révision du fichier Drive de la VDP pour conserver son identifiant et son lien. Vérifier après envoi que le lien ouvre le MP4 corrigé. Les repères du tableau et du dossier se trouvent dans les fichiers privés de la compétence installée.
4. Activer la lecture Drive pour toute personne disposant du lien sur le MP4. Insérer une puce de fichier Drive affichant le nom du MP4 sur la même ligne VDP, dans la colonne de première livraison. Pour une révision, conserver la puce liée au même fichier. Relire la puce et vérifier le partage. La façon de suivre les révisions dans Google Sheets reste à préciser avec l’utilisateur, qui vient de fixer la règle du fichier Drive unique.
5. Après avoir vérifié la puce et son accès public, renseigner le premier couple « Date » et « heure » de la ligne avec la date de création du MP4 dans Drive, convertie dans le fuseau du tableau. Ajouter uniquement les valeurs manquantes. Dans les onglets P1 inspectés, le premier couple se trouve en N et O.

Le projet fournit `scripts/google_vdp.py` pour lire, télécharger et livrer via les API, et l’option `--google-publish=PATH` de `render:storyboards` pour publier à la suite d’un rendu. Lire `docs/google-vdp.md` pour le consentement OAuth, l’essai en lecture seule et les commandes. `deliver` crée uniquement la première livraison et `revise` utilise Drive `files.update` sur le fichier identifié par le lien existant. Relire les cellules pour identifier la colonne réellement renseignée. `--link-version` sélectionne la colonne où se trouve le lien permanent et `--version` indique la version du MP4. Les deux numéros peuvent différer. Les liens storyboards insérés en puces Drive sont lus via `chipRuns`. Après révision, vérifier l’empreinte en suivant le même lien.

Le chemin « Livrable video / 3AC / Semaine 3 » a été vérifié. Sur l’onglet « P1 / Semaine 3 », les quatre storyboards 3AC VDP sont en F8, F15, F22 et F29. Leurs premières livraisons correspondent à K8, K15, K22 et K29. Revérifier les lignes au moment de la livraison.

L’onglet « P1 / Semaine 1 » utilise l’en-tête « video1 » pour la première livraison. `google_vdp.py` reconnaît cet en-tête comme l’équivalent de « Version 1 » et exige une seule colonne correspondante. Vérifier la présence de liens dans les autres colonnes et de vidéos homonymes dans le dossier avant une première livraison.

## Charte et animation

- L’objectif apparaît au centre, puis monte avant l’explication des mots-clés. Garder le texte uniformément bleu marine, de taille naturelle, sur une ligne si elle reste lisible. Sur deux lignes, aligner les débuts et équilibrer l’espace dans le bandeau. Employer la cible et la flèche orange approuvées.
- Souligner chaque mot-clé et tracer une flèche verticale depuis le milieu du soulignement jusqu’à son explication. Suivre l’ordre rouge, vert, violet, puis ambre si nécessaire. Quand les explications se succèdent, faire disparaître ensemble le soulignement, la flèche et son explication au passage au mot suivant. Un timecode validé pour une leçon peut fixer une disparition plus tôt.
- Faire entrer ensemble le badge turquoise et le cadre à fond blanc. Les titres de section se terminent par des deux-points précédés d’une espace, par exemple « Définition : ». Dans la synthèse de 3AC VDP2, les quatre cartes portent des expressions seules conformément à la correction de cette leçon.
- Pour une question, utiliser le PNG bleu approuvé le 12 novembre 2026, `public/brand/question-mark.png`, via `QuestionMark.tsx`. Le composant tient compte des marges transparentes. Cadrer la bulle avec le contenu et synchroniser son entrée avec la question.
- Choisir une animation qui signale l’information utile. Agrandir brièvement un nombre au moment où la voix le nomme. Pour expliquer un sigle, partir de la lettre concernée et la relier directement au mot avec la même couleur. Pour une phrase révélée mot par mot, réserver la place de la phrase entière afin de stabiliser la composition.

## Écriture mathématique

- Utiliser des chiffres droits, des variables italiques, des exposants surélevés et de vrais signes mathématiques. Rendre les variables algébriques avec les glyphes Cambria Math 𝒙 et 𝒚 validés et conserver les variables éditables dans la timeline. Espacer les opérateurs et garder leur couleur neutre lorsque les couleurs distinguent les termes. [Référence de composition mathématique](math-typesetting.md)
- Centrer les étapes d’un calcul dans le cadre et espacer les lignes. Aligner une conclusion à côté d’une fraction sur sa barre horizontale. Faire apparaître les nombres et les marques de vérification sur les mots correspondants de la voix.
- Quand la voix nomme les facteurs premiers, colorer les bases désignées. Garder la lecture des exposants et des signes de multiplication claire. Pendant la construction d’un produit, conserver une ellipse pour chaque facteur encore attendu.

- Quand un exemple est invalidé, placer le repère « Faux » près de l’expression pour le distinguer visuellement de l’opérateur ×. Dans une fraction, ancrer séparément la mise en évidence du dénominateur et celle de l’exposant sur les glyphes. Vérifier en pleine résolution que les ellipses laissent un espace autour des glyphes et de la barre. Pour comparer deux conversions, aligner les signes égaux sur une même colonne. Quand seule l’annotation change, garder l’équation au même emplacement et vérifier les deux états dans le MP4. [Exemples 3AC semaine 3](n3-sem3-vdp.md#v4--révision-des-quatre-vdp-de-3ac-semaine-3)

- Quand un titre d’objectif contient une équation, mesurer ensemble le titre et la formule dans leurs polices réelles pour que la formule garde la couleur du titre et que le soulignement reste aligné. Dans un calcul de degré, mettre en évidence l’exposant de chaque variable au moment où il est nommé, puis révéler leur somme. [Exemples de 2AC](n2-sem1-vdp3-vdp4.md)

- Pour une fraction avec des radicaux imbriqués, vérifier le numérateur et le dénominateur à la taille finale et pendant l’entrée. Le conteneur de formule doit inclure toute sa hauteur. Réserver aussi la géométrie complète d’une égalité avant de révéler le deuxième membre afin d’éviter un déplacement ou un signe égal collé. [Contrôles 3AC semaine 4](n3-sem4-vdp1-vdp2.md).

## Voix, rythme et prononciation

### Vocabulaire — même voix et génération native obligatoire

Consigne du 25 novembre 2026 : pour chaque nouveau passage de vocabulaire/prononciation, générer une nouvelle animation native et sa voix avec le même fournisseur, la même voix et le profil vocal validé pour la langue du mot dans le reste de la vidéo. Pour un mot français, reprendre la voix française principale de cette vidéo ; ne pas imposer Kore à une vidéo validée avec une autre voix.

Ne jamais insérer le clip vidéo ni la piste sonore de vocabulaire intégrés au PowerPoint dans un nouveau rendu ou une nouvelle révision. Ces médias peuvent uniquement guider la compréhension de la référence. Cette règle remplace explicitement l’ancienne consigne de réutiliser les extraits de prononciation du PPT, ainsi que les anciennes exceptions de voix distincte pour le vocabulaire. Les exports historiques ne valent pas autorisation de les reproduire ainsi.

Conserver le mot et le contenu source intacts. Révéler les parties correctement orthographiées, puis réunir le mot selon le modèle simplifier ; réserver les aides phonétiques à la préparation vocale, sans les afficher. Vérifier la voix réellement sélectionnée, les prises générées et les repères d’animation. Réutiliser les prises de ce nouvel insert pour une reprise technique est possible ; cela n’autorise pas la réutilisation d’un média audio/vidéo du PPT.

- Utiliser le profil vocal validé pour le lot. Google Gemini Kore correspond aux leçons dont la voix Google a été validée. Pour la révision des VDP 3AC de la semaine 3, choisir Soukaina en français avec Eleven v4 et reprendre les passages arabes validés. Réutiliser les prises validées lorsque leur insertion préserve une voix cohérente.
- Après une coupe, un ajout ou une pause, recalculer les repères visuels à partir du son final et des mots prononcés. Les anciens timecodes servent à localiser la correction. Vérifier les nouveaux repères dans la timeline puis dans le MP4.
- Pour le vocabulaire, révéler les syllabes écrites au rythme de leur lecture, puis estomper les séparateurs et réunir le mot au moment où il est prononcé naturellement. Exemples validés : **pre–mier**, **dé–com–po–si–tion**, **ir–ré–duc–tible**. Les indications phonétiques restent dans la préparation de la voix. [Référence de prononciation](pronunciation-reference.md)

- Pour les VDP bilingues, l’utilisateur demande une voix française naturelle et les mots arabes en arabe standard (الفصحى). Le profil validé pour la semaine 3 utilise Soukaina avec Eleven v4, langue fr, débit 0,94 et stabilité 0,45. Les mots arabes utilisent des prises séparées avec Eleven Flash v2.5, langue ar. Reprendre l’audio validé d’un mot déjà enregistré. Viser environ 0,65 s entre les idées avec ce profil, puis vérifier les passages arabes dans le MP4 encodé. [Essais Soukaina](n3-sem3-vdp.md#essais-de-voix-bilingues)

- Ancienne méthode de réutilisation du média de prononciation intégré : historique uniquement, remplacée le 25 novembre 2026. Créer désormais l’animation et la voix avec le profil de la vidéo ; ne pas insérer le MP4 ni son son du PowerPoint. Voir la nouvelle règle ci-dessus et [la leçon Expression](n1-sem3-vdp1.md).

- Pour une correction d’un mot arabe dans une courte prise séparée, conserver le PCM français validé et remplacer seulement la prise concernée. Contrôler le mot sans fournir le texte attendu à la reconnaissance, puis refaire ce contrôle sur l’audio encodé et vérifier le décalage des scènes suivantes. La V2 1AC semaine 3 VDP1 corrige ainsi حصة sans refaire la voix française ni le clip « Expression ». Son + de vocabulaire confirme la règle des opérateurs neutres, distincts des signes des nombres.

- La correction « Quotient » confirme que l’absence de clip intégré ne suffit pas à remplacer le modèle de prononciation par un mot entier statique. Montrer les parties correctement orthographiées, puis leur réunion ; conserver les guides phonétiques dans la préparation vocale. Revoir séparément la diction et l’animation. [Correction V2 de la semaine 4](n3-sem4-vdp1-vdp2.md#v2--correction-de--quotient--demandée-par-lutilisateur).

## Projet source After Effects

La génération du projet source fait partie de chaque nouvelle production VM ou VDP et de chaque révision livrée. Après contrôle du MP4, construire le .aep avec la timeline, la narration et les médias de la même version. En lot, répéter l’étape pour chaque vidéo.

- Préparer une composition principale avec des sous-compositions nommées et des repères de diapositives. Garder les textes, formules, formes, flèches et animations modifiables, ainsi que la voix séparée par séquence.
- Livrer en privé un ZIP versionné contenant le .aep, ses WAV et illustrations liés par chemins relatifs, un guide d’ouverture et le MP4 de comparaison désactivé dans le montage. Pour les VDP suivies dans Sheets, la puce continue de pointer vers le MP4.
- Extraire le ZIP dans un autre dossier. Vérifier le fichier natif, les médias, la durée et les repères. Comparer les états des animations à des images du MP4. Consigner séparément la lecture dans Adobe si elle a pu être testée.

Le guide du studio docs/after-effects.md donne les commandes. L’export initial est vérifié pour [la VDP4 V2 de 2AC, semaine 1](n2-sem1-vdp3-vdp4.md). Pour une autre leçon, adapter la capture et la collecte à ses composants, puis vérifier le montage obtenu avant de le remettre.

## Vérification et livraison

- Vérifier les calculs, les couleurs, les limites du texte et les étapes intermédiaires dans les aperçus. Vérifier à nouveau les images aux repères corrigés dans le MP4 encodé, notamment juste avant et après une révélation ou une disparition.
- Contrôler séparément le contenu de la voix. L’alignement donne les temps d’un texte connu. Une écoute ou une reconnaissance indépendante contrôle ce qui a été prononcé. Pour une syllabe isolée ou un passage bilingue omis, contrôler le segment court et documenter les ambiguïtés de reconnaissance.
- Vérifier le décodage complet du MP4 1080p à 30 i/s avec son AAC. Livrer le fichier final et sa timeline modifiable. En cas de révision, conserver l’export précédent et identifier la nouvelle version.

## Exemples vérifiés

| Leçon | Corrections à réutiliser selon le storyboard |
| --- | --- |
| [3AC VDP1 · Nombres premiers](n3-sem2-vdp1-2026-11-10.md) | Insertion de deux phrases courtes en français et en arabe dans la voix existante. Grand **1** au-dessus de la remarque. **11**, sa flèche et **1 et 11** sur le même axe. Conclusion révélée mot par mot. La bande orange et le clignotement relèvent de cette synthèse. |
| [3AC VDP2 · Factorisation](n3-sem2-vdp2-factorization.md) | Disparitions vérifiées à 00:10 et 00:13. Bases **2, 3, 5** puis **2, 3** colorées au mot prononcé. Syllabes, mot réuni et quatre cartes de synthèse sans deux-points. |
| [3AC VDP3 · Fractions](n3-sem2-vdp3-fractions.md) | Pulsations séparées de **23** et **41**, conclusion alignée sur la barre, retrait des répétitions sur les divisions par **3** et **6**. Fractions de synthèse et ellipse du dénominateur calées sur la voix. |
| [2AC · Algèbre](four-storyboards-2026-11-10.md) | Forme de **𝒙** et **𝒚** contrôlée dans l’image encodée. Opérateurs neutres, termes signés et colonnes alignés dans la soustraction. |
| [1AC VDP2 · Addition et valeur absolue](n1-sem2-vdp2-signed-addition.md) | La taille des carrés distingue les valeurs absolues. Le signe reste un élément distinct. La narration guide l’anneau du grand carré vers son signe et révèle le zéro dans le cas des opposés. |
| [1AC VDP3 et VDP4 · Semaine 2](n1-sem2-vdp3-vdp4.md) | Conserver l’ordre des termes quand les crochets changent et montrer le signe d’opération séparément du signe de l’entier. Lorsque le storyboard souligne un passage de l’objectif sans explication visuelle, le composant accepte un soulignement seul. Contrôler séparément l’amorce, les syllabes et le mot entier si la synthèse vocale omet une partie. |
| [3AC · Semaine 3 · Quatre VDP](n3-sem3-vdp.md) | Vérifier les chiffres parlés contre la fraction exacte. Montrer le numérateur seul tant que la conversion est en cours. Pour une droite graduée, calculer la position du point à l’échelle et vérifier la réciproque. Contrôler les fins des lots de voix par transcription indépendante. |

## Mise à jour après chaque révision

1. Après contrôle du résultat, noter le changement, la leçon ou la scène concernée et la preuve du contrôle dans le handoff et la référence de la leçon.
2. Mettre à jour cette base quand le retour confirme une règle réutilisable, en remplace une ou apporte un exemple qui aidera la prochaine production. Garder la portée donnée par l’utilisateur et rattacher les exceptions à leur leçon.
3. Enregistrer les remarques encore ouvertes comme telles dans le handoff. Synchroniser les copies locales de la compétence. Les versions et les références servent de mémoire d’un chat à l’autre.

## Dates du suivi des storyboards

Les alertes distinguent « Ajout repéré le » (première détection dans le tableau) et « Créé dans Drive » (création du fichier). Afficher les heures de Casablanca et signaler une date non historisée plutôt que de déduire une insertion exacte depuis createdTime ou depuis le contrôle courant. Conserver la mémoire des clés vues pour éviter les alertes en double. Voir [la référence du suivi](storyboard-monitoring.md).


La V3 de [1AC semaine 3 VDP1](n1-sem3-vdp1.md) illustre désormais le contrôle de fidélité : extraction directe des bandes de narration, lecture des mathématiques OMML incluse, textes pédagogiques contrôlés séparément, test du refus des anciennes reformulations et de la suppression d’une répétition. Une expansion orale de notation conserve le contenu ; elle doit être tracée distinctement du texte source. Les instructions phonétiques/pauses servent uniquement à la diction et ne permettent aucune réécriture. La restitution est vérifiée avant de remplacer le même lien public.


La V5 de 3AC semaine 3 VDP1 confirme deux contrôles avant rendu : conserver les radicaux OMML lors de l’extraction et distinguer les étiquettes pédagogiques contenues dans une image de la narration seule. Les étiquettes de la diapositive de synthèse ont été relues sur l’image source ; elles ne sont pas déduites de la bande verte. Les guillemets d’une phrase de lecture restent en texte SVG, avec variable mathématique, plutôt que d’assouplir globalement le mode strict KaTeX. Voir n3-sem3-vdp.md pour la restauration des 30 bandes, le vocabulaire natif Soukaina et les limites de contrôle. Une annotation de graphie non explicite reste documentée comme point à préciser même après rétablissement de la forme source.


### Fidélité des phrases visibles pendant les révélations

Une apparition progressive ne permet pas de supprimer les amorces, connecteurs ou signes de ponctuation de la phrase pédagogique source. Tous les fragments doivent apparaître dans la formulation finale, dans l’ordre du storyboard. Comparer la phrase visible complète recomposée au paragraphe pédagogique source entier ; rechercher seulement un fragment ou vérifier uniquement la narration ne suffit pas. Cette règle est confirmée par la correction V6 de 3AC semaine 3 VDP1 le 25 novembre 2026.

La V6 corrige uniquement les éléments de la phrase concernée : huit scènes identiques, neuf WAV réutilisés, piste AAC identique. Une correction d’affichage ne nécessite aucune nouvelle génération vocale lorsque l’audio source est déjà correct. Voir n3-sem3-vdp.md pour le contrôle et la livraison.


### Comparaison de racines carrées et contrôle des captures

La V5 de 3AC semaine 3 VDP2 montre comment vérifier le préambule et les connecteurs d’une propriété avant d’animer séparément condition et conclusion. Vérifier aussi les signes de chaque comparaison et les accents visuels des nombres sur leurs mots. Une correction orthographique de la carte a été demandée à l’utilisateur puis tracée après accord ; elle ne donne aucune permission générale de réécrire le storyboard.

L’utilisateur a confirmé que la capture périodique appartient à VDP3. L’ordre chronologique de réception des captures et un nom de fichier voisin ne prouvent pas le rattachement d’une image à une leçon. Conserver cette attribution confirmée et la remarque auprès de sa vraie vidéo.

Une reconnaissance de syllabe sur une fenêtre très courte peut halluciner une longue phrase. La durée du signal permet d’écarter ce résultat comme preuve de contenu prononcé. Utiliser du contexte et, si disponible, une seconde analyse acoustique indépendante sans fournir le texte attendu ; ne pas régénérer une bonne prise sur la seule base de cette sortie aberrante. Voir n3-sem3-vdp.md pour les vérifications, le vocabulaire natif Soukaina et les limites.


## Retour vérifié · VDP3 semaine 3 · 26 novembre 2026

- Composer fractions, égalités et résultats dans un même bloc mathématique natif ou ancrer explicitement leurs axes. Des blocs KaTeX indépendants au même y peuvent avoir des axes différents. Vérifier les pixels encodés, les colonnes communes et la stabilité pendant les révélations ; ici écart mesuré nul.
- Réserver invisiblement la géométrie des éléments futurs, sans ajouter de contenu visible. Ne jamais introduire une égalité transitoire fausse. Une contradiction voix/image nécessite un accord précis consigné ; cet accord ne vaut pas autorisation de reformuler le reste.
- Une difficulté de diction française peut être traitée par un dictionnaire IPA pris en charge par le fournisseur, en métadonnées non prononcées, en conservant les mots et la voix validés. Contrôler le son final, pas seulement le texte attendu ou l’alignement forcé. Une réponse secondaire tronquée ou incohérente ne certifie rien : cibler le passage disputé avec assez de contexte. Caches et locateurs privés restent locaux.
- Attribution confirmée : la capture périodique / pé–rio concerne N3 SEM3 VDP3. Révéler toutes les parties et vérifier le mot réuni ; aucune phonétique affichée, aucun média PPT.
- Résultat VDP3 V5 : dix points traités, quatre tests source/mathématiques, 19 tests studio et TypeScript validés ; même livraison publique K22. Détails et limites dans n3-sem3-vdp.md. Les modifications du contenu restent limitées aux accords consignés.


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


### Choix précis entre storyboard et fiche · VDP4 V7 · 26 novembre 2026

Conserver la provenance de chaque changement : finie venait de la fiche, limitée du storyboard et de la voix. Après choix explicite de limitée, remplacer seulement cette légende et sa réserve invisible, vérifier les bornes de pixels du nombre avant/après, et prouver que l’AAC intégral reste identique. Ne pas attribuer à une initiative un mot réellement demandé dans une fiche, ni traiter un choix limité comme l’annulation de toutes les corrections. Cas livré : N3 SEM3 VDP4 V7, même fichier K29.


### Signes d’entiers et valeurs absolues · N1 SEM2 VDP4 V2 · 26 novembre 2026

Une demande de + devant cinq dans un exemple d’opposés concerne les nombres signés et leur conclusion ; elle n’autorise pas à ajouter ce signe à toute occurrence de 5, notamment aux deux valeurs absolues. Identifier les occurrences par leur rôle source, conserver les couleurs sémantiques et vérifier les étapes encodées. Si les anciens timecodes dépassent la durée actuelle, documenter leur décalage et utiliser le contenu fourni pour retrouver sans ambiguïté le passage ; ne pas inventer de nouveaux passages. Pour cette correction, deux champs visuels seuls changent et l’AAC complet reste identique. Le même lien public et sa puce sont préservés.


### Vérifier la version du storyboard avant de réutiliser une vidéo

Un fichier portant le même nom peut avoir changé de déroulé. Pour la VDP4 de 2AC en semaine 1, le tableau affichait « Terminé » et le lien vidéo fonctionnait encore. Le PowerPoint fourni avait pourtant 33 diapositives, contre 17 lors de la première livraison. Comparer le contenu et l’ordre de la source reçue avant de reprendre une timeline ou un cache audio. Pour le vocabulaire, examiner aussi les illustrations fixes du masque ou de la mise en page. Ici le microphone figure dans la mise en page, tandis que la lecture syllabique est recréée avec la voix de la leçon.
