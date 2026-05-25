//View 1

DROP VIEW IF EXISTS public.v_my_department_requests;

CREATE VIEW public.v_my_department_requests AS
SELECT 
    r.request_id,
    r.date AS request_date,
    r.incident_description,
    r.prioriry_level,
    c.category_name,
    s.status_label,
    l.city AS request_city,
    f.phone_number AS contact_phone 
FROM public.a_request r
JOIN public.a_requestcategory c ON r.category_id = c.category_id
JOIN public.a_status s ON r.status_id = s.status_id
JOIN public.a_location l ON r.latitude = l.latitude AND r.longitude = l.longitude
JOIN public.a_family f ON r.contactperson_id = f.contactperson_id; 

SELECT * FROM public.v_my_department_requests ;

SELECT 
    request_id AS "ID",
    request_date AS "Date",
    request_city AS "City",
    category_name AS "Request type",
    prioriry_level AS "Urgency",
    contact_phone AS "Contact Phone"
FROM public.v_my_department_requests
WHERE prioriry_level >= 4 
  AND EXTRACT(MONTH FROM request_date) = 4
ORDER BY request_date DESC;

SELECT 
    TO_CHAR(request_date, 'Day') AS "Day of the Week",
    COUNT(*) AS "Total Requests",
    ROUND(AVG(prioriry_level), 2) AS "Average Priority",
    COUNT(CASE WHEN prioriry_level >= 4 THEN 1 END) AS "Of Which Critical Emergencies"
FROM public.v_my_department_requests
GROUP BY EXTRACT(ISODOW FROM request_date), TO_CHAR(request_date, 'Day')
ORDER BY EXTRACT(ISODOW FROM request_date) ASC;


//View 2

DROP VIEW IF EXISTS public.v_received_department_skills;

CREATE VIEW public.v_received_department_skills AS
SELECT 
    v.volunteer_id,
    v.first_name || ' ' || v.last_name AS volunteer_full_name,
    v.phone_number AS volunteer_phone,
    s.skill_name,
    c.catagory_name
FROM public.a_volunteer v
JOIN public.b_volunteer_skill vs ON v.volunteer_id = vs.volunteer_id
JOIN public.b_skill s ON vs.skill_id = s.skill_id
JOIN public.b_catagory c ON s.category_id = c.catagory_id;



SELECT 
    volunteer_full_name,
    volunteer_phone,
    catagory_name,
	skill_name
FROM public.v_received_department_skills
WHERE catagory_name LIKE '%Language%' 
  AND skill_name LIKE '%Arabic%'
ORDER BY volunteer_full_name ASC;


SELECT 
    volunteer_full_name AS "Volunteer Employee",
    COUNT(*) AS "Number of Validated Skills"
FROM public.v_received_department_skills
GROUP BY volunteer_id, volunteer_full_name
ORDER BY "Number of Validated Skills" DESC;