
---------------------------------------
------------ ROLLBACK------------------

-- Exemple with UPDATE
BEGIN;
-- Before change
SELECT city, longitude, latitude
FROM location
WHERE city = 'Jerusalem' AND longitude =34.142932;   

-- Change
UPDATE cckerlocation
SET longitude = 40,
    latitude = -40
WHERE city = 'Jerusalem' AND longitude =34.142932;


-- Display change
SELECT city, longitude, latitude
FROM location
WHERE city = 'Jerusalem' AND longitude = 40 AND    latitude = -40;

ROLLBACK;

--display
-- after rollback
SELECT city, longitude, latitude
FROM location
WHERE city = 'Jerusalem' AND longitude =34.142932;



------------ Exemple with DELETE
BEGIN;
-- Before delete the volunteer who not work since one year
SELECT volunteer_id,first_name
FROM volunteer v
WHERE EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
)
AND NOT EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
      AND t.date >= CURRENT_DATE - INTERVAL '100 days'
);

-- Delete
DELETE FROM volunteer v
WHERE EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
)
AND NOT EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
      AND t.date >= CURRENT_DATE - INTERVAL '100 days'
);

-- Display after delete: should be empty
SELECT volunteer_id,first_name
FROM volunteer v
WHERE EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
)
AND NOT EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
      AND t.date >= CURRENT_DATE - INTERVAL '100 days'
);

ROLLBACK;



-- After rollback: deleted volunteers return
SELECT volunteer_id
FROM volunteer v
WHERE EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
)
AND NOT EXISTS (
    SELECT 1
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
      AND t.date >= CURRENT_DATE - INTERVAL '100 days'
);


------------------------------------
---------- COMMIT ------------------
BEGIN;

UPDATE requestcategory
SET description = 'Critical Repairs like main pipe bursts or total electrical failure'   
WHERE category_id = 1;

COMMIT;