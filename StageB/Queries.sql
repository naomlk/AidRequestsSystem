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
EXCEPT
SELECT first_name, last_name, phone_number
FROM VOLUNTEER
WHERE has_equipment = true
ORDER BY last_name ASC;


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
ORDER BY total_requests DESC;


--Top Volunteers by Request Category
WITH VolunteerStats AS (
    SELECT 
        c.category_name, 
        v.first_name || ' ' || v.last_name as volunteer_name, 
        COUNT(t.treatment_id) as missions_count
    FROM VOLUNTEER v
    JOIN TREATMENT t ON v.volunteer_id = t.volunteer_id
    JOIN REQUEST r ON t.request_id = r.request_id
    JOIN REQUESTCATEGORY c ON r.category_id = c.category_id
    GROUP BY c.category_name, v.volunteer_id, v.first_name, v.last_name
)
SELECT category_name, volunteer_name, missions_count
FROM VolunteerStats vs1
WHERE missions_count = (
    SELECT MAX(missions_count) 
    FROM VolunteerStats vs2 
    WHERE vs2.category_name = vs1.category_name
)
ORDER BY category_name;


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


UPDATE REQUEST r
SET latitude = l.latitude, 
    longitude = l.longitude
FROM (
    SELECT latitude, longitude, row_number() OVER () as rn 
    FROM LOCATION
) l
WHERE r.request_id % (SELECT COUNT(*) FROM LOCATION) = l.rn - 1;

UPDATE VOLUNTEER
SET has_equipment = (CASE 
    WHEN volunteer_id % 5 IN (0, 1, 2, 3) THEN true 
    ELSE false 
END);
*/
