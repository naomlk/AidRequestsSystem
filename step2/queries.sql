-- VOLUNTEERS AVAILABLE--
SELECT volunteer_id,first_name,last_name 
FROM volunteer
WHERE availability_status == true


-- ACTIVES REQUEST ---
SELECT request_id
FROM request
WHERE  status_id == 1  -- a supposer que 1 signifie une requete active



-- VOLUNTEERS AVAILABLE FOR EACH REQUEST ACTIVE
SELECT v.volunteer_id, v.first_name, v.last_name
FROM volunteer v
JOIN request r ON v.request_id = r.request_id
WHERE r.status_id = 1
AND SQRT(POWER(v.longitude - r.longitude, 2) 
       + POWER(v.latitude - r.latitude, 2)) < 50;
