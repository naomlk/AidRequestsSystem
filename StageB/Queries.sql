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

/* to test the stage 3
SELECT f.contactperson_id, f.contactperson_name, COUNT(r.request_id) as total_req
FROM public.a_family f
JOIN public.a_request r ON f.contactperson_id = r.contactperson_id
GROUP BY f.contactperson_id, f.contactperson_name
ORDER BY total_req DESC LIMIT 15;*/



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
WHERE r.latitude >= 32.3    -- nord
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

/*
SELECT r.request_id, r.latitude, r.longitude, l.city, r.date
FROM public.a_request r
JOIN public.a_location l ON r.latitude = l.latitude AND r.longitude = l.longitude
WHERE r.latitude >= 32.3
  AND r.date >= '2026-01-01'
ORDER BY r.date DESC;*/



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


/*
SELECT treatment_id, date, feedback_notes, volunteer_id
FROM public.a_treatment
WHERE date BETWEEN '2026-03-01' AND '2026-03-31'
ORDER BY date ASC;*/



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


/*
SELECT first_name, last_name, phone_number
FROM public.a_volunteer
WHERE has_equipment = false
ORDER BY last_name ASC;*/



--Elite Volunteer Service Report (>100km),volunteers that go over 100 km to a request
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

/*
SELECT DISTINCT ON (v.volunteer_id)
    v.volunteer_id,
    l_v.city AS starting_city,
    l_r.city AS destination_city,
    ROUND((6371 * acos(
        cos(radians(r.latitude)) * cos(radians(v.latitude)) * cos(radians(v.longitude) - radians(r.longitude)) + 
        sin(radians(r.latitude)) * sin(radians(v.latitude))
    ))::numeric, 2) AS distance_km
FROM public.a_volunteer v
JOIN public.a_treatment t ON v.volunteer_id = t.volunteer_id
JOIN public.a_request r ON t.request_id = r.request_id
JOIN public.a_location l_v ON v.latitude = l_v.latitude AND v.longitude = l_v.longitude
JOIN public.a_location l_r ON r.latitude = l_r.latitude AND r.longitude = l_r.longitude
WHERE (6371 * acos(
        cos(radians(r.latitude)) * cos(radians(v.latitude)) * cos(radians(v.longitude) - radians(r.longitude)) + 
        sin(radians(r.latitude)) * sin(radians(v.latitude))
    )) > 100
ORDER BY v.volunteer_id ASC;*/



--Top Performing Volunteers (Above Average Activity)
SELECT first_name, last_name, counter
FROM VOLUNTEER
WHERE counter > (SELECT AVG(counter) FROM VOLUNTEER)
ORDER BY counter DESC;

/*
SELECT first_name, last_name, counter
FROM public.a_volunteer
WHERE counter > (SELECT AVG(counter) FROM public.a_volunteer)
ORDER BY counter DESC;*/



--Monthly Requests Summary         COUNT(*) compte les ligne vides alors que COUNT(request_id) non
SELECT 
    TO_CHAR(date, 'Month') as month_name, 
    EXTRACT(YEAR FROM date) as year_nb, 
    COUNT(*) as nb_requests
FROM REQUEST
GROUP BY year_nb, month_name, EXTRACT(MONTH FROM date)
ORDER BY year_nb DESC, EXTRACT(MONTH FROM date) DESC;


/*
SELECT 
    TO_CHAR(date, 'Month') as month_name, 
    EXTRACT(YEAR FROM date) as year_nb, 
    COUNT(*) as nb_requests
FROM public.a_request
GROUP BY year_nb, month_name, EXTRACT(MONTH FROM date)
ORDER BY year_nb DESC, EXTRACT(MONTH FROM date) DESC;*/



--Geographic Distribution of Requests by City
SELECT l.city, c.category_name, COUNT(r.Request_id) as total_requests
FROM LOCATION l
JOIN REQUEST r ON l.latitude = r.latitude AND l.longitude = r.longitude
JOIN REQUESTCATEGORY c ON r.category_id = c.category_id
GROUP BY l.city, c.category_name
ORDER BY l.city , total_requests DESC ;


/*
SELECT l.city, c.category_name, COUNT(r.request_id) as total_requests
FROM public.a_location l
JOIN public.a_request r ON l.latitude = r.latitude AND l.longitude = r.longitude
JOIN public.a_requestcategory c ON r.category_id = c.category_id
GROUP BY l.city, c.category_name
ORDER BY l.city, total_requests DESC;*/



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


