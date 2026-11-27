# GitHub et autre compte · 27 novembre 2026

L’utilisateur autorise explicitement la publication du projet et de ses compétences sur son GitHub pour les réutiliser avec un autre compte. Les dépôts retenus sont privés : ezzakiayman/digital-lab-ai-studio pour le projet et ezzakiayman/codex-skills pour les dossiers digital-lab-project et presentation-video. Le dépôt existant digital-lab-flux est une autre application et doit rester inchangé.

Le projet source inclut les composants, les timelines JSON, les scripts de préparation, synthèse, alignement, contrôle et livraison Google, les documents, les deux compétences, les éléments de charte approuvés et une démonstration technique silencieuse de douze secondes. Le démarrage et le rendu génériques utilisent cette démonstration ; la propriété historique reste sélectionnable. Les leçons de production nécessitent leurs médias locaux. Aucun MP4 livré n’est modifié par cette préparation.

Les médias de production et les originaux de référence restent locaux. Aucune clé, autorisation OAuth, donnée de suivi privée, archive DPAPI, document d’inspecteur ou poids de modèle ne doit être publié. Le constructeur scripts/build-github-snapshot.py utilise une sélection explicite et un contrôle de motifs de secrets ; il retire les champs pronunciationDictionaryLocators de sept plans historiques dans la copie exportée seulement, sans altérer les originaux. Le nouveau compte doit recréer ses propres dictionnaires si nécessaire.

Pour reprendre, cloner le dépôt privé avec un compte GitHub autorisé, ouvrir sa racine dans Codex et lire docs/github-reuse.md. scripts/setup-project.ps1 installe les dépendances verrouillées, vérifie le démarrage portable et peut installer les compétences sans écraser une copie différente. Les clés et OAuth sont configurés par le destinataire. La surveillance planifiée est à recréer dans son compte ; le script ne transfère pas l’automatisation ni l’historique de notifications.

Le dépôt codex-skills doit être mis à jour en conservant ses autres projets et agents. Les règles restent inchangées : contenu source et narration intouchables hors accord précis, charte, mathématiques professionnelles, prononciation native avec la voix principale et accent français, contrôle encodé et révision du même fichier Drive.

Au moment de cette note, la publication est en préparation. Les reçus de publication et les résultats de l’installation propre doivent être consignés dans PROJECT_HANDOFF.md et cette référence après vérification ; ne pas annoncer un push ou un contrôle distant avant qu’il n’ait réussi.
