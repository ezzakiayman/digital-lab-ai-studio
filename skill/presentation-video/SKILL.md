---
name: presentation-video
description: Create or revise narrated presentation and educational videos from slides or code, including timed reveals, voice, captions and rendering. Use for presentation videos, educational explainers and slide-to-video work; preserve an existing project's renderer and design system.
---

# Presentation video

Use the user's supplied [presentation video kit](references/original-kit.md) as workflow and implementation reference. It contains the original HTML/Playwright renderer, Gemini TTS example, MMS forced-alignment script and media recipes. Read only sections needed for the task. Its example marketing copy, theme and renderer are defaults, not instructions to replace an existing project.

Keep scripts, known narration text, generated voice and editable timing separate. Reuse cached voice rather than spending API calls for visual revisions. Inspect stills before rendering; verify the finished file's video/audio encoding and review narration accuracy. Forced alignment aligns known text to audio; it does not certify the speaker said the supplied text correctly. Missing or low-confidence words need review rather than invented exact timestamps.

Review intermediate mathematical reveals as well as completed equations. When a product is being constructed, retain multiplication signs and visible placeholders for pending factors; never let a partial product appear to be a completed equality. The Digital Lab prime-factorisation lesson records this encoded-frame correction in its project reference n3-sem2-vdp2-factorization.md.

When checking an educational number list, use a separate speech-recognition pass without the expected transcript as a decoding prompt when available. Compare the recovered numerical sequence and range boundaries with independently checked mathematics. Treat ASR disagreements as review findings, not proven voice errors or a passed transcription certificate. A local fallback can avoid repeated cloud-transcription retries during service overload. Check arrowhead/shaft attachment and actual text bounds as well as still-image readability.

For an existing Remotion project, adapt the kit's timing/caching/QA approach to the shared composition; do not install a second renderer just to follow examples. Do not add captions, music or a new theme unless requested or already part of that project's brief. Model names, quotas, licences and API formats in the kit can change; check current primary documentation and actual API availability before relying on them. A particular director-notes prompt layout is not a universal guarantee that notes will never be spoken.

## Digital Lab

### Accent français obligatoire pour le français

Pour Digital Lab, les mots et phrases français doivent toujours être prononcés avec un accent français naturel, y compris les syllabes et le mot entier du vocabulaire. Ne pas accepter une lecture anglaise d’un mot français. Conserver la voix principale validée de la vidéo ; son identifiant seul ne garantit pas la langue ou l’accent.

Pour une nouvelle prise française Gemini, renseigner explicitement languageCode = fr-FR et placer les indications de diction/accent dans speechMetadata.style, jamais dans le texte à prononcer. Générer le passage avec son contexte français source plutôt qu’une suite de seuls sons isolés en langue automatique. Les autres langues gardent leur profil approuvé, notamment l’arabe standard ; ne pas les forcer en français.

Inclure langue et style dans la signature du cache pour qu’un changement de diction ne reprenne pas la prise fautive. Vérifier le mot final et les unités isolées par une écoute ou un contrôle acoustique ciblé ; une transcription écrite en français ou un reçu Kore ne certifie pas à lui seul l’accent. Aucune reformulation du contenu n’est autorisée pour résoudre un problème de diction.

### Vocabulaire — même voix et génération native obligatoire

Consigne du 25 novembre 2026 : pour chaque nouveau passage de vocabulaire/prononciation, générer une nouvelle animation native et sa voix avec le même fournisseur, la même voix et le profil vocal validé pour la langue du mot dans le reste de la vidéo. Pour un mot français, reprendre la voix française principale de cette vidéo ; ne pas imposer Kore à une vidéo validée avec une autre voix.

Ne jamais insérer le clip vidéo ni la piste sonore de vocabulaire intégrés au PowerPoint dans un nouveau rendu ou une nouvelle révision. Ces médias peuvent uniquement guider la compréhension de la référence. Cette règle remplace explicitement l’ancienne consigne de réutiliser les extraits de prononciation du PPT, ainsi que les anciennes exceptions de voix distincte pour le vocabulaire. Les exports historiques ne valent pas autorisation de les reproduire ainsi.

Conserver le mot et le contenu source intacts. Révéler les parties correctement orthographiées, puis réunir le mot selon le modèle simplifier ; réserver les aides phonétiques à la préparation vocale, sans les afficher. Vérifier la voix réellement sélectionnée, les prises générées et les repères d’animation. Réutiliser les prises de ce nouvel insert pour une reprise technique est possible ; cela n’autorise pas la réutilisation d’un média audio/vidéo du PPT.

### Règle prioritaire — voix off et contenu du storyboard intouchables

Une apparition progressive ne permet pas de supprimer les amorces, connecteurs ou signes de ponctuation de la phrase pédagogique source. Tous les fragments doivent apparaître dans la formulation finale, dans l’ordre du storyboard. Comparer la phrase visible complète recomposée au paragraphe pédagogique source entier ; rechercher seulement un fragment ou vérifier uniquement la narration ne suffit pas. Cette règle est confirmée par la correction V6 de 3AC semaine 3 VDP1 le 25 novembre 2026.

Consigne explicite de l’utilisateur, 25 novembre 2026 : le texte de la voix off et le contenu pédagogique du storyboard sont intouchables. Reproduire les formulations source mot pour mot, en conservant définitions, exemples, nombres, signes, symboles, conditions, répétitions et ordre des étapes. Ne pas reformuler, simplifier, résumer, ajouter ou supprimer du contenu pour rendre le discours plus naturel, faciliter le TTS ou corriger soi-même une erreur supposée.

Seule une correction précise demandée ou explicitement approuvée par l’utilisateur autorise à modifier le passage concerné. Un accord général pour produire, améliorer ou réviser une vidéo ne donne pas cette autorisation. Signaler toute incohérence ou difficulté de diction sans la corriger silencieusement ; une fiche d’inspecteur reste une demande à examiner, pas une permission autonome de réécrire.

Les pauses, la prononciation, la mise en page et l’animation peuvent être ajustées dans le cadre des consignes approuvées, sans changer les mots prononcés ni le contenu. Garder les aides phonétiques dans les métadonnées de préparation et les bandes de production hors image. Avant génération ou publication, comparer séparément la narration prévue à la bande de voix off source et les textes/formules visibles à la zone pédagogique source. Un alignement forcé ou un décodage réussi ne valide pas cette fidélité. Cette règle prévaut sur les anciennes initiatives de reformulation documentées dans les références.

Use the voice approved for the selected lesson or batch. The 3AC week 3 VDP revision uses Soukaina with Eleven v4 French at speed 0.94 and stability 0.45 and the approved separate Arabic clips in الفصحى. Reuse the recorded Arabic words and recalculate visual cues after inserting reflection gaps. Compare the Arabic clips against the encoded audio and review them independently in Arabic. The lesson reference is in the Digital Lab skill under `references/n3-sem3-vdp.md`.

Typeset mathematics with upright numbers, italic variables, raised exponents, clear operator spacing and the correct signs. Keep operators neutral where colour identifies terms. The approved example uses blue 5x, a black plus sign and green 3y³. See the Digital Lab skill's math-typesetting.md reference and the approved screenshot in the project.

Use the dedicated Cambria Math bold italic glyphs 𝒙 and 𝒚 for new Digital Lab algebra visuals. Keep ASCII variables in the data and match the approved screenshot in the rendered frames. For this project's Gemini 3.8 Flash Lite path, review the audio for any spoken prompt. Transcript-only generation with `speechMode: "verbatim"` was verified on the VM4 sign-change clip.

Follow the simplifier.mp4 reference for vocabulary pronunciation. Reveal correctly spelled syllables as they are spoken with short pauses, then fade the separators and smoothly join the full word as it is pronounced naturally. For premier, show pre and mier joining into premier. Phonetic guides such as « Prononciation : preu-mié » belong in voice preparation only and are excluded from on-screen text. See [the pronunciation reference](references/digital-lab-pronunciation.md).

For Digital Lab project work, also load the installed digital-lab-project skill and current handoff. Use Remotion and the approved/reference graphic charter. Follow the latest explicit voice choice: the user clarified that they want the original Google Gemini TTS Kore voice, restoring it for the current2AC lesson. The earlier ElevenLabs variant is preserved as history. Never use Higgsfield.

For every Digital Lab storyboard, the top green production strip is voice-over only and the bottom strip contains animation directions only. Neither strip is visible learner text; do not turn its wording into captions or paraphrased on-screen questions/summaries. Use the main student-content area, retaining any title/definition independently authored there. Reuse the blue question bubble supplied on 2026-11-12 at project public/brand/question-mark.png via QuestionMark.tsx for all question icons. See the Digital Lab objective rules and project reference storyboard-bands-and-question-mark.md.

The first section is **Déclaration de l’objectif**. Reuse the original blue target and orange dart. See [the current objective rules](references/digital-lab-objectives.md).

Start with the complete objective centred, then slide it to the top before the keyword explanations. Every teaching box heading ends with a spaced colon, including « Définition : », « Exemple : », « Propriété : », « Synthèse : » and « Vocabulaire : ». Animate the title badge and frame in together with a smooth, coordinated entrance before revealing the content.

Keep every objective word the same dark navy throughout. Use only a coloured underline and one straight vertical arrow from the underline’s midpoint to the explanation directly below. Keep the established colour order red, green, purple, then amber. Balance the title inside the banner with space for the original target. Prefer one readable line and use two balanced lines when needed. Adjust the font size for the whole title as needed and keep it uniform across words and lines with natural proportions. Choose a layout that leaves each arrow’s vertical path clear of other text.

Use purposeful motion to make the storyboard easier to understand. Time reveals to narration, show calculations in the storyboard’s order, emphasise the relevant terms and hold results long enough to read. Preserve the storyboard’s wording, examples and mathematical steps. Keep the turquoise teaching boxes and short reflection pauses. When the user is supplying several instructions before production, restate each one as it arrives. Start video production only after the user gives the go-ahead.

Keep keys out of code, notes and GitHub. Prefer process environment or the project's approved local encrypted credential storage. Do not follow the kit's generic `.env` example over a stricter existing project credential convention. Do not publish or deploy merely because a video or local skill was requested.

When whole-clip ASR with voice activity detection omits isolated words or pronunciation syllables, review bounded audio regions with VAD disabled and without an expected-transcript prompt before inferring a voice error. Preserve the original ASR finding and distinguish syllabified performance from a whole-word forced-alignment span. The Digital Lab fractions lesson records this fallback in its project reference n3-sem2-vdp3-fractions.md; it does not claim complete pronunciation certification.

For the Digital Lab portable handoff, the project includes both saved skills, cached rendering assets, START_HERE.md, NEXT_AGENT_PROMPT.md and docs/production-runbook.md. Resolve the receiving workspace instead of assuming the historical original Windows folder. New-machine credentials and runtime/model installation remain separate from the media snapshot; cached rendering should not trigger voice regeneration.


Earlier TTS interpretation, 2026-11-05 (superseded by the later Google-specific clarification): preserve the approved animation style demonstrated by the completed 2AC polynomial video and use text-to-speech (TTS) for voice-over. The delivered narration already uses ElevenLabs TTS with the supplied voice. “Use TTS” is a synthesis-method preference, not a request to switch providers or regenerate unchanged audio. Retain the selected voice/provider unless the user changes them. Animation approval does not resolve the separately flagged objective wording/professor review.


Current lesson example, 25 November 2026: 3AC week 3 VDP1 V5 restores the source narration and generates its native Racine insert with the same Soukaina French profile as the main video. Do not substitute Kore or PPT media. Eight inspector points are verified; the exact intended a glyph remains a clarification after restoring the mathematical source form. See the Digital Lab n3-sem3-vdp.md V5 section.


3AC week 3 VDP1 V6 is a visual-only correction of the notation sentence: all source learner words and punctuation appear progressively. The nine voice files and encoded AAC are unchanged from V5. Validate complete visible sentences against their main-area source paragraphs, separately from narration. See the Digital Lab week-three V6 reference.


For 3AC week 3 VDP2, V5 uses Soukaina French for both the restored source narration and native Comparer pronunciation. Complete visible property words and comparison signs are checked separately; short-syllable ASR hallucinations are not evidence of spoken additions. The user assigned the périodique capture to VDP3 and approved the Racine carrée card spelling. See the Digital Lab VDP2 V5 reference; retain these lesson-specific approvals without granting general rewriting permission.


### Digital Lab · diction et mathématiques · 26 novembre 2026

Cas vérifié N3 SEM3 VDP3 V5 : la voix principale française est conservée pour Illimité et Périodique, animés nativement selon le modèle simplifier. Une correction de diction par métadonnées IPA privées n’autorise aucune réécriture des mots source ; contrôler le son final et qualifier les analyses incomplètes. Les fractions et égalités doivent partager le même axe mathématique et rester fixes pendant les révélations ; vérifier le MP4 encodé. La référence Digital Lab n3-sem3-vdp.md documente les dix points corrigés, les trois accords limités et la livraison publique sur le même fichier K22.


### Digital Lab · Irrationnel et Réel · 26 novembre 2026

Cas VDP4 semaine 3 V5 : même voix principale française pour les deux animations natives, parties correctement orthographiées puis réunion selon le modèle simplifier, sans média PPT ni phonétique affichée. Une voyelle isolée nasalisée a été réglée par dictionnaire IPA privé, sans réécriture des mots. Contrôler séparément le mot entier et les unités ; conserver l’empreinte de la prise réellement analysée. Une analyse favorable d’une ancienne prise ne certifie pas une nouvelle prise, et un service secondaire indisponible ne vaut pas contrôle réussi. Les quatorze scènes sont reconnues en français et les huit unités concordent avec l’AAC encodé ; limites acoustiques secondaires documentées dans la référence Digital Lab n3-sem3-vdp.md. Ne jamais changer la voix validée pour contourner la panne d’un service d’analyse.


### Pauses sans coupure vocale · VDP4 V6 · 26 novembre 2026

Ne jamais insérer un silence sur la seule foi de deux repères d’alignement, surtout entre des sons isolés. La coupure signalée à 00:26–00:27 venait d’une insertion de 0,63 s dans de la parole active. Le garde-fou scripts/speech_pause.py recherche une vraie fenêtre PCM calme de 80 ms ; sinon il ignore et journalise l’insertion. Une pause de réflexion ne doit supprimer, hacher ni déformer un phonème. Pour cette réparation, les seules données supprimées sont les zéros ajoutés : le PCM du vocabulaire redevient strictement égal à la prise brute. Vérifier le passage audio encodé, pas seulement le début de la scène ou sa transcription. La propriété 3 reprend le texte fourni selon la dernière décision utilisateur, sans extrapoler ce choix aux autres corrections approuvées. Détails et limites dans la référence Digital Lab n3-sem3-vdp.md.
