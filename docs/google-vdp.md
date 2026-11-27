# Livraison VDP par les API Google

Le script Windows `scripts/google_vdp.py` lit le lien du storyboard dans Sheets, télécharge le PowerPoint depuis Drive et peut livrer un MP4 vérifié dans le dossier et la cellule de version correspondants. Le rendu de la leçon part d’une timeline éditable préparée et relue. Le circuit Google utilise des requêtes API.

## Autorisation initiale

Depuis ton propre navigateur, ouvre un projet Google Cloud de ton organisation.

1. Active [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) et [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) dans le même projet.
2. Configure [l’audience OAuth](https://console.cloud.google.com/auth/audience) avec l’option **Interne** si disponible pour ton organisation. Crée ensuite un [client OAuth](https://console.cloud.google.com/auth/clients) de type **Application de bureau**. Le consentement Google couvre les droits Drive et Sheets du compte professionnel. Les commandes Digital Lab ciblent le tableau et le dossier configurés. [Documentation Google Workspace](https://developers.google.com/workspace/guides/configure-oauth-consent)
3. Télécharge le JSON du client et enregistre-le localement sous `private/google-oauth-client.json` dans le projet Digital Lab. Le dossier `private/` est exclu de Git. Garde ce fichier sur le poste.
4. Ouvre un terminal PowerShell dans le projet et lance la commande ci-dessous. Ouvre toi-même le lien Google qu’elle affiche, puis valide avec ton compte de travail. Le terminal doit rester ouvert pendant la validation. Le jeton de renouvellement est protégé par Windows DPAPI pour ton utilisateur.

```powershell
Set-Location -LiteralPath 'C:/Users/EDITO/Desktop/digital lab video IA'
py -3 -X utf8 scripts/google_vdp.py auth
```

Sur le poste d’origine, c’est le projet de production qui contient le script et reçoit les fichiers dans `private/`. La commande confirme l’autorisation avec « Connected the work account » après la validation dans Google. Si elle réclame le client OAuth, déposer le JSON téléchargé à l’étape 3 sous le nom exact `google-oauth-client.json`.

Le script trouve les liens Google déjà enregistrés dans le dossier privé de la compétence Digital Lab. Sur un autre poste, place deux fichiers dans `private/google-references/` du projet. Dans `storyboard-tracker.json` et `video-delivery-folder.json`, indique respectivement le lien complet du tableau avec son `gid` et le lien du dossier de livraison sous la clé `url`. Utilise la même adresse professionnelle sous `account` dans les deux fichiers.

## Essai sur une VDP déjà livrée

Dans « P1 / Semaine 1 », F20 est la cellule storyboard de la VDP3 de 2AC. La puce publique est en K20. Les commandes suivantes lisent le tableau et comparent le fichier Drive au MP4 local.

```powershell
py -3 -X utf8 scripts/google_vdp.py inspect --gid 825019823 --cell F20 --version 1
py -3 -X utf8 scripts/google_vdp.py fetch --gid 825019823 --cell F20 --version 1
py -3 -X utf8 scripts/google_vdp.py verify --gid 825019823 --cell F20 --version 1 --mp4 outputs/n2-sem1/vdp3/P1_MATHS_N2_SEM1_VDP3.mp4
```

Dans « P1 / Semaine 1 », l’en-tête « video1 » correspond à la première livraison. Le script reconnaît cet en-tête pour `--version 1`, par exemple avec `--gid 825019823 --cell F20` ou `--gid 825019823 --cell F27`.

Ajoute `--gid` avec l’identifiant de l’onglet pour traiter une autre semaine. Le PowerPoint téléchargé arrive dans `outputs/google-vdp/storyboards/`. Pour une présentation au format Google Slides, le script utilise l’export PowerPoint de Drive.

## Publication d’une vidéo ou d’un lot

Chaque VDP garde un seul fichier Drive et un lien stable. Pour une première livraison, utilise `deliver` avec la même syntaxe que `verify`, la colonne « Version 1 » et un MP4 nommé d’après le storyboard.

Pour une correction, indique la nouvelle version et la colonne qui contient déjà le lien permanent du fichier. Par exemple, les quatre VDP de la semaine 3 de 3AC restent liées en K8, K15, K22 et K29 sous « Version 1 ». Leur version actuelle est la V4.

```powershell
py -3 -X utf8 scripts/google_vdp.py revise --cell F8 --link-version 1 --version 4 --mp4 outputs/n3-sem3-v4/vdp1/P1_MATHS_N3_SEM3_VDP1_V4.mp4
```

La commande vérifie l’identité de la VDP, le dossier, les droits et le MP4. Elle envoie les nouvelles données au même identifiant Drive. Le nom du fichier indique la version courante et le lien déjà inscrit dans Sheets reste valable. Le format d’affichage du numéro de version dans Sheets attend une décision. Utilise les mêmes paramètres avec `verify` pour relire cette livraison par le lien existant. L’option de lot équivalente utilise `"version": 4, "linkVersion": 1` pour cette leçon.

Pour les premières livraisons depuis la commande de rendu, place les correspondances dans `private/vdp-delivery.json`. Le format ci-dessous illustre deux entrées de la semaine 3. Pour les versions déjà déposées, utilise `verify`. Les clés sont les identifiants du rendu Digital Lab. Chaque entrée utilise la cellule du **storyboard**. Le script résout la cellule de version à partir des titres du tableau.

```json
{
  "n3-sem3-vdp1": {"cell": "F8", "version": 1},
  "n3-sem3-vdp2": {"cell": "F15", "version": 1}
}
```

```powershell
npm run render:storyboards -- n3-sem3-vdp1 n3-sem3-vdp2 --google-publish=private/vdp-delivery.json
```

Chaque rendu déclenche le contrôle 1080p, 30 i/s, H.264/AAC et le décodage complet avant le dépôt. La livraison reprend un transfert interrompu et vérifie le dossier et l’empreinte Drive. Elle active et vérifie la lecture pour toute personne disposant du lien, puis écrit et relit une puce Drive affichant le nom du MP4. Pour appliquer ce réglage à une vidéo déjà livrée, relancer la commande d’origine avec le même fichier MP4. Une puce déjà correcte est conservée et un lien simple vers ce fichier est converti. [Partage Drive](https://developers.google.com/workspace/drive/api/guides/manage-sharing) · [Puces Google Sheets](https://developers.google.com/workspace/sheets/api/guides/chips) Si l’écriture échoue après un envoi réussi, tu peux relancer `deliver` sur le même MP4 pour réutiliser le fichier. Une cellule qui contient déjà un lien différent est conservée.

Le rendu sur lot utilise le Python disponible via `python`. Sur le poste d’origine, lance d’abord cette commande pour choisir l’installation accessible par le lanceur Windows. Pour le kit avec Python déjà ajouté au PATH, `python` suffit et peut aussi remplacer `py -3` dans les commandes du guide.

```powershell
$env:DIGITAL_LAB_PYTHON = py -3 -c "import sys; print(sys.executable)"
```

## Date et heure de première livraison

Après avoir vérifié la puce et son accès public, renseigner le premier couple « Date » et « heure » de la ligne avec la date de création du MP4 dans Drive, convertie dans le fuseau du tableau. Ajouter uniquement les valeurs manquantes. Dans les onglets P1 inspectés, le premier couple se trouve en N et O. La commande `deliver` peut compléter les deux cellules à partir du MP4 déjà livré. Sous Windows, installer `tzdata` dans le Python de production si la base des fuseaux horaires manque.

[Formats Google Sheets](https://developers.google.com/workspace/sheets/api/guides/formats)

## Contrôles locaux

```powershell
py -3 -X utf8 -m unittest discover -s scripts -p test_google_vdp.py -v
npm run typecheck
npm test
```

Le test simulé couvre le repérage de la ligne et du dossier, la récupération du storyboard, la reprise d’envoi, la vérification d’empreinte, la protection de la cellule, la reprise après une erreur d’écriture dans Sheets et la révision du même fichier sans réserver un nouvel identifiant. Le test avec le tableau et le dossier de travail nécessite l’autorisation initiale.
