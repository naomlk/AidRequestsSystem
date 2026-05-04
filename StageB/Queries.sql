--Top 15 Families by Number of Requests
--version 1
SELECT f.ContactPerson_id, f.ContactPerson_name, COUNT(r.Request_id) as total_req
FROM FAMILY f
JOIN REQUEST r ON f.ContactPerson_id = r.ContactPerson_id
GROUP BY f.ContactPerson_id, f.ContactPerson_name
ORDER BY total_req DESC LIMIT 15;

--version 2
SELECT f.ContactPerson_id, f.ContactPerson_name, 
       (SELECT COUNT(*) FROM REQUEST r WHERE r.ContactPerson_id = f.ContactPerson_id) as total_req
FROM FAMILY f
ORDER BY total_req DESC LIMIT 15;


-- 2026 Northern Region Service Requests
--version 1
SELECT 
    r.request_id, 
    r.latitude, 
    r.longitude, 
    l.city, 
    r.date
FROM REQUEST r
JOIN LOCATION l ON r.latitude = l.latitude AND r.longitude = l.longitude
WHERE r.latitude >= 32.3
  AND r.date >= '2026-01-01'
ORDER BY r.date DESC;
--version 2
SELECT 
    r.request_id, 
    r.latitude, 
    r.longitude, 
    (SELECT l.city 
     FROM LOCATION l 
     WHERE l.latitude = r.latitude 
       AND l.longitude = r.longitude) AS city,
    r.date
FROM REQUEST r
WHERE r.latitude >= 32.3
  AND r.date >= '2026-01-01'
ORDER BY r.date DESC;



--Filtered Treatments by Specific Date Range
-- Version 1 
SELECT treatment_id, date, feedback_notes, volunteer_id
FROM TREATMENT
WHERE date BETWEEN '2026-03-01' AND '2026-03-31'
ORDER BY date ASC;

-- Version 2 
SELECT treatment_id, date, feedback_notes, volunteer_id
FROM TREATMENT
WHERE EXTRACT(MONTH FROM date) = 3 
  AND EXTRACT(YEAR FROM date) = 2026
ORDER BY date ASC;


--Volunteers Without Equipment
--version 1
SELECT 
    first_name, 
    last_name, 
    phone_number
FROM VOLUNTEER
WHERE has_equipment = false
ORDER BY last_name ASC;

--version 2
SELECT first_name, last_name, phone_number
FROM VOLUNTEER
EXCEPT                                              --EXCEPT = MINUS
SELECT first_name, last_name, phone_number
FROM VOLUNTEER
WHERE has_equipment = true
ORDER BY last_name ASC;


--Elite Volunteer Service Report (>100km)
SELECT DISTINCT ON (v.volunteer_id)
    v.volunteer_id,
    l_v.city AS starting_city,
    l_r.city AS destination_city,
    ROUND((6371 * acos(
        cos(radians(r.latitude)) * cos(radians(v.latitude)) * 
        cos(radians(v.longitude) - radians(r.longitude)) + 
        sin(radians(r.latitude)) * sin(radians(v.latitude))
    ))::numeric, 2) AS distance_km
FROM VOLUNTEER v
JOIN TREATMENT t ON v.volunteer_id = t.volunteer_id
JOIN REQUEST r ON t.request_id = r.request_id
JOIN LOCATION l_v ON v.latitude = l_v.latitude AND v.longitude = l_v.longitude
JOIN LOCATION l_r ON r.latitude = l_r.latitude AND r.longitude = l_r.longitude
WHERE (6371 * acos(
        cos(radians(r.latitude)) * cos(radians(v.latitude)) * 
        cos(radians(v.longitude) - radians(r.longitude)) + 
        sin(radians(r.latitude)) * sin(radians(v.latitude))
    )) > 100
ORDER BY v.volunteer_id ASC;



--Top Performing Volunteers (Above Average Activity)
SELECT first_name, last_name, counter
FROM VOLUNTEER
WHERE counter > (SELECT AVG(counter) FROM VOLUNTEER)
ORDER BY counter DESC;


--Monthly Requests Summary
SELECT 
    TO_CHAR(date, 'Month') as month_name, 
    EXTRACT(YEAR FROM date) as year_nb, 
    COUNT(*) as nb_requests
FROM REQUEST
GROUP BY year_nb, month_name, EXTRACT(MONTH FROM date)
ORDER BY year_nb DESC, EXTRACT(MONTH FROM date) DESC;


--Geographic Distribution of Requests by City
SELECT l.city, c.category_name, COUNT(r.Request_id) as total_requests
FROM LOCATION l
JOIN REQUEST r ON l.latitude = r.latitude AND l.longitude = r.longitude
JOIN REQUESTCATEGORY c ON r.category_id = c.category_id
GROUP BY l.city, c.category_name
ORDER BY l.city , total_requests DESC ;


--Critical Pending Requests (Priority 4 & 5)
--version 1
SELECT r.Request_id, r.date, r.incident_description
FROM REQUEST r
JOIN STATUS s ON r.status_id = s.status_id
WHERE s.status_label = 'Pending' AND r.prioriry_level >= 4;

--version 2
SELECT Request_id, date, incident_description
FROM REQUEST
WHERE prioriry_level >= 4 
AND status_id = (SELECT status_id FROM STATUS WHERE status_label = 'Pending');



--Removing Inactive Volunteers (No Activity for 1 Year)
DELETE FROM VOLUNTEER
WHERE volunteer_id NOT IN (
    SELECT DISTINCT volunteer_id 
    FROM TREATMENT 
    WHERE date > CURRENT_DATE - INTERVAL '1 year'
);

--Deleting not used locations
DELETE FROM LOCATION
WHERE (latitude, longitude) NOT IN (
    SELECT latitude, longitude FROM VOLUNTEER
)
AND (latitude, longitude) NOT IN (
    SELECT latitude, longitude FROM REQUEST
);


--Deleting cancelled requests
DELETE FROM REQUEST
WHERE status_id = 4
AND Request_id NOT IN (SELECT request_id FROM TREATMENT);



-- Update: Increases the priority level of pending requests older than 2 days.
UPDATE REQUEST
SET prioriry_level = prioriry_level + 1
WHERE status_id = 1 
  AND date < CURRENT_DATE - INTERVAL '2 days'
  AND prioriry_level < 5;

--Updates the request status to 3 (Completed)
UPDATE REQUEST
SET status_id = 3
WHERE Request_id IN (
    SELECT request_id 
    FROM TREATMENT 
    WHERE completion_time IS NOT NULL
);


--update treatment's count of each volunteer
UPDATE volunteer v
SET counter = (
    SELECT COUNT(*)
    FROM treatment t
    WHERE t.volunteer_id = v.volunteer_id
);



/* a ajouter si on remet la base de donnees a zero
UPDATE request r
SET contactperson_id = (
    SELECT contactperson_id 
    FROM family 
    WHERE r.request_id IS NOT NULL 
    ORDER BY random() 
    LIMIT 1
);

UPDATE treatment t
SET volunteer_id = (
    SELECT volunteer_id 
    FROM volunteer 
    WHERE t.treatment_id IS NOT NULL
    ORDER BY random() 
    LIMIT 1
);


-- 1. On désactive les triggers de contraintes
SET session_replication_role = 'replica';

-- 2. ICI tu lances ton UPDATE de LOCATION (le gros bloc avec les CASE WHEN)
-- 3. ICI tu lances tes deux UPDATE de synchronisation pour REQUEST et VOLUNTEER

-- 4. On remet tout en ordre
SET session_replication_role = 'origin';

UPDATE LOCATION
SET 
    latitude = CASE 
        WHEN city = 'Ashdod' THEN 31.8044 + (random() * 0.03)
        WHEN city = 'Beer Sheva' THEN 31.2522 + (random() * 0.04)
        WHEN city = 'Bnei Brak' THEN 32.0833 + (random() * 0.01)
        WHEN city = 'Haifa' THEN 32.7940 + (random() * 0.04)
        WHEN city = 'Holon' THEN 32.0158 + (random() * 0.02)
        WHEN city = 'Jerusalem' THEN 31.7683 + (random() * 0.05)
        WHEN city = 'Netanya' THEN 32.3215 + (random() * 0.03)
        WHEN city = 'Petah Tikva' THEN 32.0840 + (random() * 0.03)
        WHEN city = 'Rishon LeZion' THEN 31.9730 + (random() * 0.03)
        WHEN city = 'Tel Aviv' THEN 32.0853 + (random() * 0.05)
        ELSE latitude 
    END,
    longitude = CASE 
        WHEN city = 'Ashdod' THEN 34.6553 + (random() * 0.03)
        WHEN city = 'Beer Sheva' THEN 34.7915 + (random() * 0.04)
        WHEN city = 'Bnei Brak' THEN 34.8333 + (random() * 0.01)
        WHEN city = 'Haifa' THEN 34.9896 + (random() * 0.04)
        WHEN city = 'Holon' THEN 34.7874 + (random() * 0.02)
        WHEN city = 'Jerusalem' THEN 35.2137 + (random() * 0.05)
        WHEN city = 'Netanya' THEN 34.8532 + (random() * 0.03)
        WHEN city = 'Petah Tikva' THEN 34.8878 + (random() * 0.03)
        WHEN city = 'Rishon LeZion' THEN 34.7925 + (random() * 0.03)
        WHEN city = 'Tel Aviv' THEN 34.7818 + (random() * 0.05)
        ELSE longitude
    END;



UPDATE REQUEST r
SET latitude = l.latitude, 
    longitude = l.longitude
FROM (
    SELECT latitude, longitude, row_number() OVER () as rn 
    FROM LOCATION
) l
WHERE r.request_id % (SELECT COUNT(*) FROM LOCATION) = l.rn - 1;



UPDATE VOLUNTEER v
SET latitude = l.latitude, 
    longitude = l.longitude
FROM (
    SELECT latitude, longitude, row_number() OVER () as rn 
    FROM LOCATION
) l
WHERE v.volunteer_id % (SELECT COUNT(*) FROM LOCATION) = l.rn - 1;

UPDATE VOLUNTEER
SET has_equipment = (CASE 
    WHEN volunteer_id % 5 IN (0, 1, 2, 3) THEN true 
    ELSE false 
END);



*/
