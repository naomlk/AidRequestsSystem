ALTER TABLE a_volunteer
DROP COLUMN availability_status;
--poru farder is_active


-- renommer availabiluty

ALTER TABLE a_volunteer
RENAME COLUMN availability_status TO is_active;

ALTER TABLE a_volunteer
ADD COLUMN recruitment_date DATE ;


ALTER TABLE a_volunteer
ADD COLUMN email VARCHAR(20) ;


ALTER TABLE a_volunteer
ADD COLUMN  is_active VARCHAR(1);    -- elles ont mis char en mode Y or N ( on aurait pu mettre BOOL.)
  

-- piru el transfert des skill il f	aut un champ de var plu slong onc on change avant 
ALTER TABLE public.b_skill
ALTER COLUMN skill_name TYPE VARCHAR(60);


--et ensuite 


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




-- ajouter les volont de b_volunteer ds a_volunterr


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





ALTER TABLE public.b_volunteer_skill
DROP CONSTRAINT volunteer_skill_volunteer_id_fkey;



-- poruplus de securite on ajoute 
ALTER TABLE public.a_volunteer
ADD CONSTRAINT a_volunteer_pkey
PRIMARY KEY (volunteer_id);



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

ALTER TABLE a_volunteer
DROP COLUMN skill_type;






BEGIN;

ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT volunteer_training_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;


BEGIN;

ALTER TABLE public.b_availability
DROP CONSTRAINT availability_pkey;

ALTER TABLE public.b_availability
ADD CONSTRAINT availability_pkey
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;


-- fusionenr call et request  poru ensuite fusionner b_type et request category 
BEGIN;

ALTER TABLE public.b_call
DROP CONSTRAINT call_type_id_fkey;

ALTER TABLE public.b_call
ADD CONSTRAINT fk_b_call_b_type
FOREIGN KEY (type_id)
REFERENCES public.b_type(type_id)
ON UPDATE CASCADE;

COMMIT;

BEGIN;

-- étape temporaire : 1-6 deviennent 1001-1006
UPDATE public.b_type
SET type_id = type_id + 1000
WHERE type_id BETWEEN 1 AND 6;

-- étape finale : 1001-1006 deviennent 5-10
UPDATE public.b_type
SET type_id = type_id - 996
WHERE type_id BETWEEN 1001 AND 1006;

COMMIT;

--trabsfert de ts les b_call --> a_request



ALTER TABLE public.a_family
DROP CONSTRAINT family_number_of_members_check;



CREATE TEMP TABLE call_family_mapping (
    call_id INTEGER PRIMARY KEY,
    family_id INTEGER NOT NULL
);
INSERT INTO call_family_mapping (call_id, family_id)
SELECT
    bc.call_id,
    nextval(pg_get_serial_sequence('public.a_family', 'family_id'))
FROM public.b_call bc;