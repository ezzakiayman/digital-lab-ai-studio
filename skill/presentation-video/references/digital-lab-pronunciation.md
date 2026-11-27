# Pronunciation sections — approved simplifier reference

### Accent français obligatoire pour le français

Pour Digital Lab, les mots et phrases français doivent toujours être prononcés avec un accent français naturel, y compris les syllabes et le mot entier du vocabulaire. Ne pas accepter une lecture anglaise d’un mot français. Conserver la voix principale validée de la vidéo ; son identifiant seul ne garantit pas la langue ou l’accent.

Pour une nouvelle prise française Gemini, renseigner explicitement languageCode = fr-FR et placer les indications de diction/accent dans speechMetadata.style, jamais dans le texte à prononcer. Générer le passage avec son contexte français source plutôt qu’une suite de seuls sons isolés en langue automatique. Les autres langues gardent leur profil approuvé, notamment l’arabe standard ; ne pas les forcer en français.

Inclure langue et style dans la signature du cache pour qu’un changement de diction ne reprenne pas la prise fautive. Vérifier le mot final et les unités isolées par une écoute ou un contrôle acoustique ciblé ; une transcription écrite en français ou un reçu Kore ne certifie pas à lui seul l’accent. Aucune reformulation du contenu n’est autorisée pour résoudre un problème de diction.

### Vocabulaire — même voix et génération native obligatoire

Consigne du 25 novembre 2026 : pour chaque nouveau passage de vocabulaire/prononciation, générer une nouvelle animation native et sa voix avec le même fournisseur, la même voix et le profil vocal validé pour la langue du mot dans le reste de la vidéo. Pour un mot français, reprendre la voix française principale de cette vidéo ; ne pas imposer Kore à une vidéo validée avec une autre voix.

Ne jamais insérer le clip vidéo ni la piste sonore de vocabulaire intégrés au PowerPoint dans un nouveau rendu ou une nouvelle révision. Ces médias peuvent uniquement guider la compréhension de la référence. Cette règle remplace explicitement l’ancienne consigne de réutiliser les extraits de prononciation du PPT, ainsi que les anciennes exceptions de voix distincte pour le vocabulaire. Les exports historiques ne valent pas autorisation de les reproduire ainsi.

Conserver le mot et le contenu source intacts. Révéler les parties correctement orthographiées, puis réunir le mot selon le modèle simplifier ; réserver les aides phonétiques à la préparation vocale, sans les afficher. Vérifier la voix réellement sélectionnée, les prises générées et les repères d’animation. Réutiliser les prises de ce nouvel insert pour une reprise technique est possible ; cela n’autorise pas la réutilisation d’un média audio/vidéo du PPT.

User clarification, 2026-11-10. Follow the simplifier.mp4 reference for vocabulary pronunciation. Reveal correctly spelled syllables as they are spoken with short pauses, then fade the separators and smoothly join the full word as it is pronounced naturally. For premier, show pre and mier joining into premier. Phonetic guides such as « Prononciation : preu-mié » belong in voice preparation only and are excluded from on-screen text.

Permanent user rule,2026-11-05: future word-pronunciation sections must follow the animation and spoken-pronunciation pattern in the supplied simplifier.mp4. This supersedes earlier whole-word pulses/repeats or static syllable rows for these sections. Existing delivered videos are unchanged by this workflow update.

## Master and verified observations

Keep the supplied clip as the local audiovisual master: reference/pronunciation-simplifier/simplifier.mp4 (original Downloads/simplifier.mp4). SHA256 a62abbf0ebc676f30cdc9e649d694e5a0e956352c9df2ee01bdd366cf7cff0f2. It is1920×1080,24fps,212video frames,8.857seconds with AAC audio. Project exports remain1080p30; adapt timing by seconds, not reference frame numbers. Media/evidence stay ignored/local, outside saved skills and public repositories; include this master in future private project transfers.

Decoded contact sheet and full-resolution samples show:

1. Plain white background; one large bold lowercase word line in the central reading area. Reserve the final line's position/width so earlier syllables do not jump to a new centre as the word grows. Do not add a pedagogical box/header inside this pronunciation insert merely to reuse the old template.
2. Reveal progressively from left to right: sim- in blue, then pli in green and its blue separator, then fier in red. Earlier parts remain visible. The appearance is a horizontal reveal through the letters, rather than a whole-word pulse, bouncing letters or three disconnected rows.
3. Hold the coloured sim-pli-fier long enough for syllable reading. Fade the blue hyphens, smoothly change all letters to the same blue, then close the inter-part gaps so the line becomes the single correctly spelled word simplifier, centred in place. Hold that joined word for the full-word reading and reflection.
4. Indicative source phases: first part around0.5–1s; second around2.5–3s; last around3.75–4.25s; hyphen/colour transition around5.25–5.75s; joining around5.75–6.5s; complete word held to the end. These are reference observations, not automatic onset timestamps or a universal duration for every word. Recheck the actual clip when implementing.

Dominant decoded flat colours approximate blue #087ABA, green #21A972 and red #E60000. Compression creates neighbouring shades; these samples do not certify original vector values. Use this blue→green→red pronunciation palette, distinct from the objective-arrow red→green→purple palette. For other words retain linguistically correct segmentation and any explicit storyboard semantic colours, adapting the number of parts without forcing exactly three syllables. Keep natural letter proportions and large readable type; match the master visually rather than claiming an unmeasured original font.

## Voice and synchronisation

Use the same teaching delivery: clearly articulate each actual French syllable separately, with short silent gaps, then pronounce the joined word naturally. Speak sounds, not letter names, punctuation or hyphens. For simplifier the written segmentation is sim / pli / fier and the pronunciation is /sɛ̃.pli.fje/; do not voice final r as an isolated consonant or turn the first syllable into literal letter names. Review the segmentation and pronunciation for each new mathematical word.

The latest provider/voice preference remains Google Gemini TTS Kore. This example defines the required pronunciation/cadence and motion; it is not a completed speaker-cloning implementation. Generate controlled syllable delivery and a natural full-word pass; retain clean recordings and real syllable-boundary cues separately from editable visual timing. Reveals should track their spoken parts and joining should support the natural whole-word pass. Adjust reflection pauses without stretching speech/pitch. Do not blindly reuse this clip's8.857s duration for longer words.

The user now explicitly authorises syllable spelling derived from the pronunciation target as learner content in these pronunciation sections. This narrow exception does not authorise transcript captions from the top voice-over strip or display of bottom production instructions. Do not add unrelated narrative text.

## Review and current implementation limit

Before delivering a future lesson, compare the new insert with the master: progressive reveal, retained parts, colour order, separator fade, smooth colour unification/join, final spelling, natural type, syllable audio and full-word pass. Inspect intermediate encoded frames and review bounded audio regions. A forced-alignment whole-word span cannot establish individual syllable onsets; use actual syllable evidence/cues and resolve ambiguous speech before claiming a match.

Local independent Whisper-small recognition without an expected prompt recovered syllable-like “Sam, pli, fié” and full-word “simplifié”; these phonetic/homophone transcriptions do not change the displayed infinitive simplifier or certify precise pronunciation/timbre. Contact sheet, sampled frames, extracted audio, ASR and visual-evidence.json are retained beside the ignored master. The PyAV decoder mismatch was bypassed using FFmpeg PCM input. No speech API calls were made.

The shared `PronunciationWord` component supports binôme, trinôme, polynôme and premier. Each insert uses separate spoken syllables within its narration clip, timed reveals and the joined full-word reading. For premier, the screen shows pre and mier while the speech preparation uses Preu and Mié. Extend the measured word data and review the speech for additional words. See the revised polynomial and prime lesson references for the encoded checks.

The four-storyboard batch extends the same component to sem–blables, dé–com–po–si–tion and ir–ré–duc–tible. It pairs each displayed part with its aligned spoken interval and joins the full word. The displayed ir preserves the first r while its sound cue is i. Verify the joined spelling when written and spoken boundaries differ. The two-part semblables follows spoken French with a silent final e. See the batch reference for the bounded audio checks and ambiguity limits.

## Correction du vocabulaire « Quotient » · 19 novembre 2026

L’utilisateur confirme une correction de l’animation et de la diction. Une lecture statique ou une pulsation du mot entier ne remplace pas le modèle simplifier.mp4 en l’absence de vidéo intégrée. Pour un nouvel insert de prononciation, appliquer la progression syllabique et la réunion du mot prévues par cette référence ; toute exception nécessite une consigne explicite de l’utilisateur.

La VDP2 de 3AC, semaine 4, utilise maintenant la ligne quo–tient → quotient, avec une nouvelle prise Google Kore pour cet insert seulement. Les guides vocaux Co et Cyan ne sont jamais affichés. La forme française de référence est /kɔ.sjɑ̃/ ; « tien » se prononce « cian ». Sources linguistiques : [CNRTL](https://www.cnrtl.fr/definition/Quotient), [Académie française](https://www.dictionnaire-academie.fr/article/A9Q0321).

PronunciationLine, dans PronunciationWord.tsx, réutilise le mouvement approuvé avec des parties et des largeurs éditables mesurées à 64 px. Une scène vdp-sequence peut l’activer avec pronunciation.style = simplifier et une liste advances. Le schéma refuse une liste de largeurs incohérente ou des parties dont la réunion ne forme pas le mot final. Les autres modes historiques restent disponibles pour reprendre les exports précédents. La référence Digital Lab n3-sem4-vdp1-vdp2.md détaille le son, la coupe, les contrôles et la livraison ; les reconnaissances approximatives de syllabes ne constituent pas une certification phonétique.


Cas vérifié le 25 novembre 2026 : la V5 de 3AC semaine 3 VDP1 emploie Soukaina Eleven v4 en français pour la voix et le vocabulaire natif Ra–cine réuni en Racine, sans média du PPT. La prise et les trois unités sont contrôlées dans l’AAC encodé ; reconnaissance locale indépendante, limites phonétiques explicites. Conserver le profil propre à chaque leçon plutôt qu’imposer la voix Kore d’une autre vidéo. Détails dans la référence Digital Lab n3-sem3-vdp.md.


Cas VDP2 de 3AC semaine 3, V5 du 25 novembre 2026 : Com–pa–rer est animé nativement puis rejoint Comparer avec la voix principale Soukaina, langue française explicite. Une sortie ASR aberrante sur le premier son très court est rejetée après contrôle de durée ; une analyse acoustique indépendante sans texte attendu retrouve les trois sons français et le mot entier. La prise correcte est conservée et les quatre unités sont comparées à l’AAC encodé. La capture périodique a été rattachée par l’utilisateur à VDP3 ; ce mot n’est pas ajouté à VDP2. Voir la référence Digital Lab n3-sem3-vdp.md.


### Digital Lab · diction et mathématiques · 26 novembre 2026

Cas vérifié N3 SEM3 VDP3 V5 : la voix principale française est conservée pour Illimité et Périodique, animés nativement selon le modèle simplifier. Une correction de diction par métadonnées IPA privées n’autorise aucune réécriture des mots source ; contrôler le son final et qualifier les analyses incomplètes. Les fractions et égalités doivent partager le même axe mathématique et rester fixes pendant les révélations ; vérifier le MP4 encodé. La référence Digital Lab n3-sem3-vdp.md documente les dix points corrigés, les trois accords limités et la livraison publique sur le même fichier K22.


### Digital Lab · Irrationnel et Réel · 26 novembre 2026

Cas VDP4 semaine 3 V5 : même voix principale française pour les deux animations natives, parties correctement orthographiées puis réunion selon le modèle simplifier, sans média PPT ni phonétique affichée. Une voyelle isolée nasalisée a été réglée par dictionnaire IPA privé, sans réécriture des mots. Contrôler séparément le mot entier et les unités ; conserver l’empreinte de la prise réellement analysée. Une analyse favorable d’une ancienne prise ne certifie pas une nouvelle prise, et un service secondaire indisponible ne vaut pas contrôle réussi. Les quatorze scènes sont reconnues en français et les huit unités concordent avec l’AAC encodé ; limites acoustiques secondaires documentées dans la référence Digital Lab n3-sem3-vdp.md. Ne jamais changer la voix validée pour contourner la panne d’un service d’analyse.


### Pauses sans coupure vocale · VDP4 V6 · 26 novembre 2026

Ne jamais insérer un silence sur la seule foi de deux repères d’alignement, surtout entre des sons isolés. La coupure signalée à 00:26–00:27 venait d’une insertion de 0,63 s dans de la parole active. Le garde-fou scripts/speech_pause.py recherche une vraie fenêtre PCM calme de 80 ms ; sinon il ignore et journalise l’insertion. Une pause de réflexion ne doit supprimer, hacher ni déformer un phonème. Pour cette réparation, les seules données supprimées sont les zéros ajoutés : le PCM du vocabulaire redevient strictement égal à la prise brute. Vérifier le passage audio encodé, pas seulement le début de la scène ou sa transcription. La propriété 3 reprend le texte fourni selon la dernière décision utilisateur, sans extrapoler ce choix aux autres corrections approuvées. Détails et limites dans la référence Digital Lab n3-sem3-vdp.md.
