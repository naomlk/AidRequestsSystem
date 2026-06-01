-- COMMANDS FOR INTEGRATION

/* ============================================================
   1. MODIFICATIONS TO THE a_volunteer TABLE
   ============================================================ */

-- Keep the is_active column instead of availability_status.
-- If availability_status still exists, convert its values into is_active.

UPDATE public.a_volunteer
SET is_active = CASE
    WHEN availability_status = 'Busy' THEN 'Y'
    WHEN availability_status = 'Available' THEN 'N'
    ELSE availability_status= 'N'
END
WHERE availability_status IN ('Busy', 'Available');


-- Drop availability_status after transferring the information into is_active.

ALTER TABLE public.a_volunteer
DROP COLUMN availability_status;


-- Add the columns coming from b_volunteer.

ALTER TABLE public.a_volunteer
ADD COLUMN recruitment_date DATE;

ALTER TABLE public.a_volunteer
ADD COLUMN email VARCHAR(20);

ALTER TABLE public.a_volunteer
ADD COLUMN is_active VARCHAR(1);
-- Group B used CHAR/VARCHAR with Y or N values.
-- We could also have used a BOOLEAN.


-- Add a primary key on volunteer_id so that the B tables
-- can reference a_volunteer. -- In our backup, we had removed it.

ALTER TABLE public.a_volunteer    -- when i give the name a_volunteer ( /b_volunteer)  to volunteer of
ADD CONSTRAINT a_volunteer_pkey      -- each group i had a conflict with this constraint so i had to drop one
PRIMARY KEY (volunteer_id);		-- and recreate it now



/* ============================================================
   2. MODIFICATION OF b_skill AND ADDITION OF NEW SKILLS
   ============================================================ */

-- To transfer the skills, the skill_name field must be longer.

ALTER TABLE public.b_skill
ALTER COLUMN skill_name TYPE VARCHAR(60);


-- Add the new skills starting from skill_id = 16.

INSERT INTO public.b_skill
(skill_id, description, requires_certificate, difficulty_level, skill_name)
VALUES
(
    16,
    'Specialist in opening heavy-duty locked doors, reinforced rooms and MAMAD shelters during emergencies.',
    'Y',
    5,
    'Heavy Duty Locksmith (MAMAD Specialist)'
),
(
    17,
    'General repairs and home maintenance tasks such as fixing doors, furniture, minor damages and basic household issues.',
    'N',
    2,
    'General Home Maintenance'
),
(
    18,
    'Provides immediate first aid assistance until professional medical help arrives.',
    'Y',
    4,
    'First Aid Responder'
),
(
    19,
    'Delivers water, medicine and basic medical supplies to families or people in need.',
    'N',
    2,
    'Water & Medical Supply Delivery'
),
(
    20,
    'Uses hydraulic tools for emergency opening, lifting, cutting or rescue-related tasks.',
    'Y',
    5,
    'Hydraulic Tools Expert'
),
(
    21,
    'Handles and operates heavy equipment for rescue, transport or emergency support tasks.',
    'Y',
    5,
    'Heavy Equipment Handling'
),
(
    22,
    'Emergency locksmith specialized in opening elevators, locked rooms and trapped access situations.',
    'Y',
    5,
    'Emergency Locksmith (Elevators/Rooms)'
),
(
    23,
    'Certified electrician able to handle electrical faults, power issues and emergency repairs.',
    'Y',
    4,
    'Certified Electrician'
),
(
    24,
    'Professional plumber specialized in pipe bursts, leaks and urgent plumbing repairs.',
    'Y',
    4,
    'Professional Plumber (Pipe Bursts)'
);



/* ============================================================
   3. TRANSFER OF VOLUNTEERS FROM b_volunteer TO a_volunteer
   ============================================================ */

-- Insert into a_volunteer the volunteers that exist in b_volunteer
-- but do not exist in a_volunteer.

BEGIN;

INSERT INTO public.a_volunteer (
    volunteer_id,
    first_name,
    last_name,
    email,
    recruitment_date,
    is_active
)
SELECT
    bv.volunteer_id,
    bv.first_name,
    bv.last_name,
    bv.email,
    bv.recruitment_date,
    bv.is_active
FROM public.b_volunteer bv
WHERE NOT EXISTS (
    SELECT 1
    FROM public.a_volunteer av
    WHERE av.volunteer_id = bv.volunteer_id
);

COMMIT;



/* ============================================================
   4. REDIRECTION OF b_volunteer_skill TO a_volunteer
   ============================================================ */

-- Old constraint: b_volunteer_skill.volunteer_id references b_volunteer.
-- New constraint: b_volunteer_skill.volunteer_id references a_volunteer.

BEGIN;

ALTER TABLE public.b_volunteer_skill
DROP CONSTRAINT volunteer_skill_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_skill
ADD CONSTRAINT fk_b_volunteer_skill_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;



/* ============================================================
   5. TRANSFER OF SKILLS FROM a_volunteer TO b_volunteer_skill
   ============================================================ */

-- For each volunteer in a_volunteer who has a skill_type,
-- find the matching skill_id in b_skill,
-- then insert the relationship into b_volunteer_skill.

INSERT INTO public.b_volunteer_skill (volunteer_id, skill_id)
SELECT
    av.volunteer_id,
    bs.skill_id
FROM public.a_volunteer av
JOIN public.b_skill bs
    ON bs.skill_name = av.skill_type
WHERE av.skill_type IS NOT NULL
  AND av.skill_type <> ''
  AND NOT EXISTS (
      SELECT 1
      FROM public.b_volunteer_skill bvs
      WHERE bvs.volunteer_id = av.volunteer_id
        AND bvs.skill_id = bs.skill_id
  );


-- After the transfer, drop skill_type from a_volunteer
-- because skills are now stored in b_volunteer_skill.

ALTER TABLE public.a_volunteer
DROP COLUMN skill_type;



/* ============================================================
   6. REDIRECTION OF b_volunteer_training TO a_volunteer
   ============================================================ */

-- Old constraint: b_volunteer_training.volunteer_id references b_volunteer.
-- New constraint: b_volunteer_training.volunteer_id references a_volunteer.

BEGIN;

ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT volunteer_training_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;



/* ============================================================
   7. MODIFICATION OF b_availability (the previous keys were not correct)
   ============================================================ */

BEGIN;

ALTER TABLE public.b_availability DROP CONSTRAINT IF EXISTS availability_pkey;
ALTER TABLE public.b_availability DROP CONSTRAINT IF EXISTS availability_volunteer_id_fkey;

ALTER TABLE public.b_availability
ADD CONSTRAINT b_availability_pkey PRIMARY KEY (day_of_week, start_time, volunteer_id);

ALTER TABLE public.b_availability
ADD CONSTRAINT b_availability_volunteer_id_fkey
FOREIGN KEY (volunteer_id) REFERENCES public.a_volunteer(volunteer_id);

COMMIT;


/* ============================================================
   8. PREPARATION FOR MERGING b_call INTO a_request
   ============================================================ */

-- b_call references b_type.
-- Recreate the constraint with ON UPDATE CASCADE so that the IDs
-- of b_type can be modified and automatically updated in b_call.

BEGIN;

ALTER TABLE public.b_call
DROP CONSTRAINT call_type_id_fkey;

ALTER TABLE public.b_call
ADD CONSTRAINT fk_b_call_b_type
FOREIGN KEY (type_id)
REFERENCES public.b_type(type_id)
ON UPDATE CASCADE;

COMMIT;



/* ============================================================
   9. SHIFTING THE IDs OF b_type
   ============================================================ */

-- Goal:
-- 1 -> 5
-- 2 -> 6
-- 3 -> 7
-- 4 -> 8
-- 5 -> 9
-- 6 -> 10
--
-- Use a temporary step to avoid ID conflicts.

BEGIN;

-- Temporary step: 1-6 become 1001-1006.
UPDATE public.b_type
SET type_id = type_id + 1000
WHERE type_id BETWEEN 1 AND 6;

-- Final step: 1001-1006 become 5-10.
UPDATE public.b_type
SET type_id = type_id - 996
WHERE type_id BETWEEN 1001 AND 1006;

COMMIT;



/* ============================================================
   10. TRANSFER OF b_call INTO a_request
   ============================================================ */

-- Before the transfer, drop the constraint on number_of_members
-- because rows created from b_call will have number_of_members = 0.

ALTER TABLE public.a_family
DROP CONSTRAINT family_number_of_members_check;



// Add the phone number to volunteer for the B records.
BEGIN;

UPDATE public.a_volunteer av
SET phone_number = CAST(bv.phone AS VARCHAR(20))
FROM public.b_volunteer bv
WHERE av.volunteer_id = bv.volunteer_id
  AND (av.phone_number IS NULL OR av.phone_number = '');

COMMIT;


--



INSERT INTO public.a_requestcategory (category_id, category_name, description)
VALUES
    (    5,  'Flat Tire Assistance',
        'Emergency roadside support for changing flat tires, providing a spare tire, or inflating wheels safely.'
    ),
    (   6,  'Locked Vehicle',
        'Professional locksmith assistance to safely unlock vehicles when keys are lost, damaged, or left inside.'
    ),
    (   7, 'Child Locked In Car',
        'CRITICAL EMERGENCY: Immediate rescue response for children or infants accidentally trapped inside a locked vehicle.'
    );



/* I added the calls to the request list using simple values for the missing attributes. */
INSERT INTO public.a_family (contactperson_id, contactperson_name, phone_number, number_of_members, special_features)
VALUES (999999, 'Clients Groupe B', '0500000000', null, null)
ON CONFLICT (contactperson_id) DO NOTHING;


INSERT INTO public.a_request (
    request_id,
    date,
    incident_description,
    prioriry_level,
    contactperson_id,
    category_id,
    status_id,
    latitude,
    longitude
)
SELECT

    20005 + ROW_NUMBER() OVER (ORDER BY bc.call_date, bc.phone) AS request_id,

    bc.call_date AS date,
    bc.description AS incident_description,

    CASE
        WHEN bc.description LIKE '%URGENT%' THEN 5
        ELSE 2
    END AS prioriry_level,

    999999 AS contactperson_id, -- Use the ID of the generic family created just above.

    -- Exact mapping of the categories.
    CASE
        WHEN bc.type_id = 5 THEN 5
        WHEN bc.type_id = 6 THEN 6
        WHEN bc.type_id = 7 THEN 1
        WHEN bc.type_id = 8 THEN 7
        WHEN bc.type_id = 9 THEN 1
        WHEN bc.type_id = 10 THEN 1
        ELSE 1
    END AS category_id,

    -- Mapping of the status IDs.
    CASE
        WHEN bc.status = 'Closed' THEN 3
        WHEN bc.status = 'InProgress' THEN 2
        WHEN bc.status = 'Cancelled' THEN 4
        ELSE 1
    END AS status_id,

    31.255810 AS latitude,
    34.816400 AS longitude

FROM public.b_call bc;

COMMIT;


/* Drop the request_id column from delivery because it is no longer a foreign key
   according to the teacher's instruction. */
ALTER TABLE public.a_delivery
DROP COLUMN request_id;


/* volunteer_id in treatment was not a foreign key; I fixed it here. */
BEGIN;

ALTER TABLE public.a_treatment
ADD CONSTRAINT treatment_volunteer_id_fkey
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;


/* I fixed the keys. */
BEGIN;

ALTER TABLE public.b_scheduled
DROP CONSTRAINT IF EXISTS scheduled_pkey;

ALTER TABLE public.b_scheduled
ADD CONSTRAINT scheduled_pkey PRIMARY KEY (training_id, meeting_date);

COMMIT;



/* I added the category_id column to b_skill. */
ALTER TABLE public.b_skill
ADD COLUMN IF NOT EXISTS category_id INTEGER;

ALTER TABLE public.b_skill
ADD CONSTRAINT skill_category_id_fkey
FOREIGN KEY (category_id)
REFERENCES public.b_category(category_id);


/* I filled the category_id column based on skill_name. */
BEGIN;

-- 1. Category 1: Language (English, French, Hebrew, Arabic...)
UPDATE public.b_skill
SET category_id = 1
WHERE skill_name LIKE '%speaking'
   OR skill_name IN ('English', 'French', 'Hebrew', 'Arabic');

-- 2. Category 2: Vehicle (Tire, Mechanics, Vehicle, Hydraulic Tools Expert...)
UPDATE public.b_skill
SET category_id = 2
WHERE skill_name IN ('Tire', 'Mechanics', 'Vehicle', 'Hydraulic Tools Expert', 'Water & Medical Supply Delivery');

-- 3. Category 3: Locksmith (Unlock, Locksmith, Heavy Duty Locksmith...)
UPDATE public.b_skill
SET category_id = 3
WHERE skill_name IN ('Unlock', 'Locksmith', 'Heavy Duty Locksmith (MAMAD Speciali...');

-- 4. Category 4: Rescue (Elevator rescue, Emergency Locksmith (Elevators/Rooms)...)
UPDATE public.b_skill
SET category_id = 4
WHERE skill_name IN ('Elevator', 'Elevator rescue', 'Emergency Locksmith (Elevators/Rooms)');

-- 5. Category 5: Technical (Radio, Technical, Certified Electrician, Professional Plumber...)
UPDATE public.b_skill
SET category_id = 5
WHERE skill_name IN ('Radio', 'Technical', 'Certified Electrician', 'Professional Plumber (Pipe Bursts)', 'General Home Maintenance', 'Navigation');

-- 6. Category 6: Emergency (FirstAid, First Aid Responder, Emergency...)
UPDATE public.b_skill
SET category_id = 6
WHERE skill_name IN ('FirstAid', 'First Aid Responder', 'Emergency', 'Heavy Equipment Handling');

COMMIT;



BEGIN;


/* Delete duplicated skills. */

-- 1. Replace ID 10 with 18.
-- First delete 10 when the volunteer already has 18 to avoid a primary key duplicate.
DELETE FROM public.b_volunteer_skill
WHERE skill_id = 10
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 18);

-- Then update the remaining rows.
UPDATE public.b_volunteer_skill
SET skill_id = 18
WHERE skill_id = 10;


-- 2. Replace ID 22 with 16.
DELETE FROM public.b_volunteer_skill
WHERE skill_id = 22
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 16);

UPDATE public.b_volunteer_skill
SET skill_id = 16
WHERE skill_id = 22;


-- 3. Replace ID 8 with 12.
DELETE FROM public.b_volunteer_skill
WHERE skill_id = 8
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 12);

UPDATE public.b_volunteer_skill
SET skill_id = 12
WHERE skill_id = 8;


DELETE FROM public.b_skill
WHERE skill_id IN (10, 22, 8);

COMMIT;



/* ============================================================
   11. DROP TABLES THAT ARE NO LONGER NEEDED
   ============================================================ */

DROP TABLE b_volunteer_call;

DROP TABLE b_call;

DROP TABLE b_skill_category;

DROP TABLE b_type;


-- Before dropping b_volunteer.
BEGIN;

ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT IF EXISTS fk_volunteer_training_volunteer;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;

DROP TABLE public.b_volunteer;    --After integrate all the tables we can drop the table of volunteer of the other group






