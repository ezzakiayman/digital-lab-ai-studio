# Réutiliser Digital Lab avec un autre compte

Les deux dépôts sont privés. Le compte GitHub destinataire doit avoir accès aux dépôts (invitation dans Settings → Collaborators). Changer de compte Codex sur le même ordinateur ne change pas automatiquement le compte GitHub connecté.

## Installation

Installer Git, Node.js 22 ou plus récent, Python 3.12 et FFmpeg avec ffprobe. Windows est la plateforme de référence pour les polices Arial et Cambria Math. Les polices Windows ne sont pas redistribuées.

```powershell
git clone https://github.com/ezzakiayman/digital-lab-ai-studio.git
cd digital-lab-ai-studio
powershell -NoProfile -File scripts/setup-project.ps1 -InstallSkills
npm run dev
```

L'installation des compétences refuse d'écraser une compétence différente. Comparer les fichiers avant d'utiliser explicitement `-UpdateExisting`. Les deux compétences sont aussi directement disponibles dans le dossier `skill/` du projet ; le compte peut commencer par les lire sans les installer.

Dans Codex, ouvrir ce dossier comme projet principal et envoyer :

> Lis AGENTS.md, START_HERE.md, PROJECT_HANDOFF.md, docs/production-runbook.md et les compétences de skill/. Continue Digital Lab. Respecte mot pour mot le storyboard et sa voix off ; demande mon accord pour toute correction de contenu. Conserve la charte et utilise la voix validée pour la leçon.

## Vérifier sans clé API

```powershell
npm run typecheck
npm test
node scripts/doctor.mjs --portable
npm run render:demo
```

La démonstration technique de 12 secondes utilise les composants natifs et un WAV silencieux. Elle n'est ni une leçon livrée ni une voix TTS. Le MP4 est créé dans `outputs/demo/lesson-1.mp4`. Le studio démarre sur cette démonstration. Les timelines historiques restent dans le sélecteur et servent de références éditables ; leur narration et leurs médias ne sont pas fournis dans Git.

## Produire une leçon

Fournir son propre PPTX et les médias locaux autorisés. Les dossiers `reference/`, `outputs/`, les caches vocaux, les vidéos, les documents de révision et les captures d'inspecteur restent hors GitHub. Les règles, scripts et timelines JSON sont fournis. Les contrôles spécifiques d'une ancienne leçon nécessitent ses propres sources et reçus ; un clone seul ne peut pas les certifier.

Pour générer une voix, renseigner sa propre clé de fournisseur dans l'environnement du processus : `GEMINI_API_KEY` ou `ELEVENLABS_API_KEY`. Conserver la voix et la langue validées pour chaque vidéo. Ne pas copier l'ancien coffre DPAPI : il est lié à l'utilisateur et à l'ordinateur d'origine. Sept plans historiques contiennent des locateurs de dictionnaire privé sur le poste d'origine ; ces champs sont retirés de la copie GitHub et devront être recréés avec les outils de diction du nouveau compte. Les originaux locaux sont conservés.

Pour la génération, les alignements et la reconnaissance, installer les dépendances facultatives :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-video.txt
```

Les modèles d'alignement et ASR ne sont pas inclus ; ils se téléchargent séparément. Les identifiants et modèles disponibles du fournisseur doivent être vérifiés avant une nouvelle synthèse.

## Drive et Sheets

Configurer son propre client OAuth **Application de bureau**, puis autoriser son compte. Voir [google-vdp.md](google-vdp.md). Créer localement `private/google-oauth-client.json`, `private/google-references/storyboard-tracker.json` et `private/google-references/video-delivery-folder.json`. Ces fichiers, les jetons et l'historique privé du suivi sont exclus du dépôt. Aucun accès Google de l'ancien compte n'est transféré.

Le suivi toutes les deux heures doit être recréé dans le nouveau compte Codex : le dépôt fournit le script et la procédure dans `skill/digital-lab-project/references/storyboard-monitoring.md`, mais ne crée pas une automatisation active à l'installation. Conserver le choix de notification uniquement pour les nouveaux storyboards.

## Compétences seules

Les versions correspondantes sont également dans https://github.com/ezzakiayman/codex-skills : dossiers `digital-lab-project` et `presentation-video`. Elles conservent la charte, les règles, les corrections vérifiées et les limites connues. Elles ne remplacent pas le projet Node/Remotion.

Le dépôt est privé et ne comporte pas de licence publique de redistribution. Les droits sur les contenus, la marque, les voix et les polices restent à respecter lors d'un partage avec des tiers.


## État de validation et limite connue

Le 27 novembre 2026, une installation neuve avec le verrou existant, les vingt tests studio, les douze tests Google simulés, les quatre tests de surveillance, TypeScript, le précontrôle portable et le build Next passent sur Windows. L’audit npm signale une vulnérabilité modérée et le build rappelle une alerte Next.js. Aucun `npm audit fix --force` ni changement de version n’a été appliqué dans cette publication ; examiner cette mise à jour avant une exposition publique du studio. Le dépôt privé de sources ne constitue pas un déploiement. Les polices et le comportement Linux/macOS n’ont pas été recertifiés.

Le contrôle des anciennes leçons peut signaler des médias absents dans le clone : leurs fichiers ne sont pas distribués. Ces avertissements ne valident pas leurs voix ; le contrôle sans médias concerne le studio et la démonstration technique.
