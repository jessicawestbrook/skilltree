-- Clean up CLEARLY invalid/concatenated words from spelling_words table
-- Generated on 2025-08-23T06:43:01.730Z
-- Deleting 43 clearly invalid words
-- Backup saved to: scripts/clearly_invalid_words_backup_1755931381729.json

BEGIN;

-- Delete clearly invalid words
DELETE FROM spelling_words WHERE id = '00c77c14-cb41-4fc2-b4d9-0adb3ea0b4ec'; -- "constantbalm" ()
DELETE FROM spelling_words WHERE id = '0174496b-9f8a-474f-9744-5d78ea16c5bf'; -- "propinquityepidermis" (Contains propinquity + more text)
DELETE FROM spelling_words WHERE id = '02cee441-4ac0-43a7-b14e-5a79e3d7d75e'; -- "accordaturacavalletti" (Contains accordatura + more text)
DELETE FROM spelling_words WHERE id = '05206c78-23f3-4bf7-8cc1-7913c225e087'; -- "abstrusenephrolith" ()
DELETE FROM spelling_words WHERE id = '07d5fc39-1381-4162-82f7-e8a0331ce16a'; -- "laterigradehyssop" ()
DELETE FROM spelling_words WHERE id = '08d7dad8-3fd9-4f88-b54d-6743dd77cf06'; -- "zygotenoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '09b31628-1e39-4d81-8476-35b5f475fee3'; -- "consecrateadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = '1c2eda5f-6360-4a21-a598-7909f0c5b61b'; -- "chauve-sourisadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = '1d273287-1af3-4c9d-9fe7-e50bff9722ef'; -- "antidisestablishmentarianism" (Extremely long (>25 chars))
DELETE FROM spelling_words WHERE id = '1da0a994-5f37-41d9-8dfb-bdf7b89d3ac3'; -- "veneernoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '20a9ad2e-ccdc-4cc4-8722-f2a0f2525acc'; -- "fiduciaryadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = '293a2e6d-792e-4bcb-8991-7a410f4af97f'; -- "shamanverb" (Ends with "verb")
DELETE FROM spelling_words WHERE id = '2b6ebe3f-dc00-44b3-b8c5-b8f62d386aa0'; -- "perspicaciousadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = '3148c3ab-532c-4be9-89e3-4c1d90884b38'; -- "proverb" (Ends with "verb")
DELETE FROM spelling_words WHERE id = '34b943c7-b950-461c-a9be-c310269ea75a'; -- "epicureanepidermis" ()
DELETE FROM spelling_words WHERE id = '36c7596f-f43f-481f-ae38-856356028d31'; -- "undergirdnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '3929ded1-9023-4430-96d6-bb2bf8659ed9'; -- "sennanoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '3d711c90-30ff-48cc-a252-dac99042771c'; -- "fortificationnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '3fae83dc-795c-4856-85c6-236ee394eee0'; -- "adverb" (Ends with "verb")
DELETE FROM spelling_words WHERE id = '43bad3ee-fe86-4bd1-9e22-603ec67e546c'; -- "rambunctiousnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '5424a494-e66d-4ea5-b715-5ce0dece3e44'; -- "ogivalnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '569a0e8c-3acd-457d-b483-672daca4ada6'; -- "hydriotaphiahydrocortisone" (Extremely long (>25 chars))
DELETE FROM spelling_words WHERE id = '57b3c05b-75a6-4bfd-b19e-71975e0b84e0'; -- "theriatricsnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '625b193f-91a0-4ae3-8552-5b935e9ebba0'; -- "thoughtsverb" (Ends with "verb")
DELETE FROM spelling_words WHERE id = '63293bb7-4253-4bf5-b803-0405925e0318'; -- "neuropathynoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '69b5312e-3cbb-4044-b242-5f3a21289edd'; -- "lambentlyadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = '76e5043c-acc0-4ea5-8397-10665960548a'; -- "nulliusnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '7a789cff-f5ce-452c-aa11-9d19df6aabf2'; -- "whetnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '835f00b7-5ad3-4d75-97fa-c0d0ffc54536'; -- "breviloquencenoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '84256519-4702-46a9-a6e7-54c5c8e56d33'; -- "vizierialnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '9467e353-17ea-4809-b55e-f5db8e79ba61'; -- "voraciousnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '96ffb3ad-913f-4f57-a997-36957195cc56'; -- "holocaustnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '97fb9497-1fa0-432c-81f4-40fbbd8264ee'; -- "germanenoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = '989754a1-1991-4ff2-8cdd-4bb6535e5bc3'; -- "busbyadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = 'a1f65f22-dc07-4a15-82ec-6f713bede2ba'; -- "scentverb" (Ends with "verb")
DELETE FROM spelling_words WHERE id = 'a4010aa3-227f-4e26-8fba-17425203a454'; -- "renvoinoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = 'b3666ffc-570b-443e-b90f-3aae88990380'; -- "disasternoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = 'ba5d6f7a-5488-4fce-bcf8-9389501d198a'; -- "colcannonnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = 'c7d9a753-9d55-4009-9c42-ae655fc9a9c5'; -- "lorikeetnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = 'd02334a8-1e97-40ad-b8e5-c9f62299957e'; -- "zyzomysadjective" (Ends with "adjective")
DELETE FROM spelling_words WHERE id = 'de09bc92-c774-4033-821b-480c1a1413c7'; -- "shaanxinoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = 'de7ebc4c-4e0c-4567-8174-c0e23e31518c'; -- "kenningnoun" (Ends with "noun")
DELETE FROM spelling_words WHERE id = 'e9284394-530b-4f8f-8c5f-2d8d4e7c36e0'; -- "sourisadjective" (Ends with "adjective")

COMMIT;

-- Verification queries
SELECT 'Clearly invalid words deleted' as description, 43 as count;

SELECT 'Remaining words' as description, COUNT(*) as count 
FROM spelling_words;

SELECT 'Words by difficulty after cleanup' as description, source_difficulty, COUNT(*) as count 
FROM spelling_words 
WHERE source_difficulty IS NOT NULL 
GROUP BY source_difficulty 
ORDER BY source_difficulty;