-- Get the slug for the Latin learning path
SELECT id, name, slug 
FROM learning_paths 
WHERE id = '97765ae5-4d73-43eb-8072-6b110a8c6a8a'
OR name LIKE '%Henle%' 
OR name LIKE '%Latin%';