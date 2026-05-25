

/* ============================================================
   1. MODIFICATIONS DE LA TABLE a_volunteer
   ============================================================ */

-- On garde la colonne is_active au lieu de availability_status.
-- Si availability_status existe encore, on convertit ses valeurs dans is_active.

UPDATE public.a_volunteer
SET is_active = CASE
    WHEN availability_status = 'Busy' THEN 'Y'
    WHEN availability_status = 'Available' THEN 'N'
    ELSE availability_status= 'N'
END
WHERE availability_status IN ('Busy', 'Available');


-- Supprimer availability_status après avoir transféré l’information dans is_active.

ALTER TABLE public.a_volunteer
DROP COLUMN availability_status;


-- Ajouter les colonnes venant de b_volunteer.

ALTER TABLE public.a_volunteer
ADD COLUMN recruitment_date DATE;

ALTER TABLE public.a_volunteer
ADD COLUMN email VARCHAR(20);

ALTER TABLE public.a_volunteer
ADD COLUMN is_active VARCHAR(1);
-- Le groupe B utilisait CHAR/VARCHAR avec les valeurs Y ou N.
-- On aurait aussi pu utiliser un BOOLEAN.


-- Ajouter une clé primaire sur volunteer_id pour permettre aux tables B
-- de référencer a_volunteer.

ALTER TABLE public.a_volunteer
ADD CONSTRAINT a_volunteer_pkey
PRIMARY KEY (volunteer_id);



/* ============================================================
   2. MODIFICATION DE b_skill ET AJOUT DES NOUVELLES COMPÉTENCES
   ============================================================ */

-- Pour transférer les skills, il faut un champ skill_name plus long.

ALTER TABLE public.b_skill
ALTER COLUMN skill_name TYPE VARCHAR(60);


-- Ajout des nouveaux skills à partir de skill_id = 16.

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
   3. TRANSFERT DES VOLONTAIRES DE b_volunteer VERS a_volunteer
   ============================================================ */

-- Ajouter dans a_volunteer les volontaires présents dans b_volunteer
-- mais absents de a_volunteer.

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
   4. REDIRECTION DE b_volunteer_skill VERS a_volunteer
   ============================================================ */

-- Ancienne contrainte : b_volunteer_skill.volunteer_id référence b_volunteer.
-- Nouvelle contrainte : b_volunteer_skill.volunteer_id référence a_volunteer.

BEGIN;

ALTER TABLE public.b_volunteer_skill
DROP CONSTRAINT volunteer_skill_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_skill
ADD CONSTRAINT fk_b_volunteer_skill_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;



/* ============================================================
   5. TRANSFERT DES SKILLS DE a_volunteer VERS b_volunteer_skill
   ============================================================ */

-- Pour chaque volontaire de a_volunteer qui possède skill_type,
-- on cherche le skill_id correspondant dans b_skill,
-- puis on insère la relation dans b_volunteer_skill.

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


-- Après le transfert, on supprime skill_type de a_volunteer
-- car les skills sont maintenant stockés dans b_volunteer_skill.

ALTER TABLE public.a_volunteer
DROP COLUMN skill_type;



/* ============================================================
   6. REDIRECTION DE b_volunteer_training VERS a_volunteer
   ============================================================ */

-- Ancienne contrainte : b_volunteer_training.volunteer_id référence b_volunteer.
-- Nouvelle contrainte : b_volunteer_training.volunteer_id référence a_volunteer.

BEGIN;

ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT volunteer_training_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;



/* ============================================================
   7. MODIFICATION DE b_availability (c etait pas les bonnes clés)
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
   8. PRÉPARATION DE LA FUSION ENTRE b_call ET a_request
   ============================================================ */

-- b_call référence b_type.
-- On recrée la contrainte avec ON UPDATE CASCADE pour pouvoir modifier les IDs
-- de b_type et mettre à jour automatiquement b_call.

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
   9. DÉCALAGE DES IDs DE b_type
   ============================================================ */

-- Objectif :
-- 1 -> 5
-- 2 -> 6
-- 3 -> 7
-- 4 -> 8
-- 5 -> 9
-- 6 -> 10
--
-- On passe par une étape temporaire pour éviter les conflits d’IDs.

BEGIN;

-- Étape temporaire : 1-6 deviennent 1001-1006.
UPDATE public.b_type
SET type_id = type_id + 1000
WHERE type_id BETWEEN 1 AND 6;

-- Étape finale : 1001-1006 deviennent 5-10.
UPDATE public.b_type
SET type_id = type_id - 996
WHERE type_id BETWEEN 1001 AND 1006;

COMMIT;



/* ============================================================
   10. TRANSFERT DE b_call VERS a_request
   ============================================================ */

-- Avant le transfert, on supprime la contrainte sur number_of_members
-- car les lignes créées depuis b_call auront number_of_members = 0.

ALTER TABLE public.a_family
DROP CONSTRAINT family_number_of_members_check;



// ajout du telephone dans volunteer pour les b 
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



/*j ai ajouter les call a la liste des request avec des valeurs simples pour les attributs qui manquaient*/
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
    
    999999 AS contactperson_id, -- On utilise l'ID de notre famille générique créée juste au-dessus !
    
    -- Équivalence stricte de tes catégories
    CASE 
        WHEN bc.type_id = 5 THEN 5
        WHEN bc.type_id = 6 THEN 6
        WHEN bc.type_id = 7 THEN 1
        WHEN bc.type_id = 8 THEN 7
        WHEN bc.type_id = 9 THEN 1
        WHEN bc.type_id = 10 THEN 1
        ELSE 1
    END AS category_id,

    -- Équivalence de tes statuts ID
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


/*suppression de la colonne request_id dans delivery car ce n est plus une clé etrangere
  (demande de la prof)*/
ALTER TABLE public.a_delivery 
DROP COLUMN request_id;


/*volunteer_id dans treatment n etait pas une cle etrangere , j ai rectifié ca*/
BEGIN;

ALTER TABLE public.a_treatment
ADD CONSTRAINT treatment_volunteer_id_fkey
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;    


/*j ai arrangé les clés*/
BEGIN;

ALTER TABLE public.b_scheduled 
DROP CONSTRAINT IF EXISTS scheduled_pkey;

ALTER TABLE public.b_scheduled 
ADD CONSTRAINT scheduled_pkey PRIMARY KEY (training_id, meeting_date);

COMMIT;



/*j ai ajouté la colonne category_id dans b_skill*/
ALTER TABLE public.b_skill 
ADD COLUMN IF NOT EXISTS category_id INTEGER;

ALTER TABLE public.b_skill
ADD CONSTRAINT skill_category_id_fkey
FOREIGN KEY (category_id)
REFERENCES public.b_category(category_id);


/*j ai rempli la colonne category_id en fonction du skill_name*/
BEGIN;

-- 1. Catégorie 1 : Language (English, French, Hebrew, Arabic...)
UPDATE public.b_skill
SET category_id = 1
WHERE skill_name LIKE '%speaking' 
   OR skill_name IN ('English', 'French', 'Hebrew', 'Arabic');

-- 2. Catégorie 2 : Vehicle (Tire, Mechanics, Vehicle, Hydraulic Tools Expert...)
UPDATE public.b_skill
SET category_id = 2
WHERE skill_name IN ('Tire', 'Mechanics', 'Vehicle', 'Hydraulic Tools Expert', 'Water & Medical Supply Delivery');

-- 3. Catégorie 3 : Locksmith (Unlock, Locksmith, Heavy Duty Locksmith...)
UPDATE public.b_skill
SET category_id = 3
WHERE skill_name IN ('Unlock', 'Locksmith', 'Heavy Duty Locksmith (MAMAD Speciali...');

-- 4. Catégorie 4 : Rescue (Elevator rescue, Emergency Locksmith (Elevators/Rooms)...)
UPDATE public.b_skill
SET category_id = 4
WHERE skill_name IN ('Elevator', 'Elevator rescue', 'Emergency Locksmith (Elevators/Rooms)');

-- 5. Catégorie 5 : Technical (Radio, Technical, Certified Electrician, Professional Plumber...)
UPDATE public.b_skill
SET category_id = 5
WHERE skill_name IN ('Radio', 'Technical', 'Certified Electrician', 'Professional Plumber (Pipe Bursts)', 'General Home Maintenance', 'Navigation');

-- 6. Catégorie 6 : Emergency (FirstAid, First Aid Responder, Emergency...)
UPDATE public.b_skill
SET category_id = 6
WHERE skill_name IN ('FirstAid', 'First Aid Responder', 'Emergency', 'Heavy Equipment Handling');

COMMIT;  



BEGIN;


/* suppression de skill qui se repetent*/

-- 1. Remplacement de l'ID 10 par 18
-- On supprime d'abord le 10 si le bénévole a déjà le 18 pour éviter le doublon de clé primaire
DELETE FROM public.b_volunteer_skill 
WHERE skill_id = 10 
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 18);

-- Puis on met à jour les autres
UPDATE public.b_volunteer_skill 
SET skill_id = 18 
WHERE skill_id = 10;


-- 2. Remplacement de l'ID 22 par 16
DELETE FROM public.b_volunteer_skill 
WHERE skill_id = 22 
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 16);

UPDATE public.b_volunteer_skill 
SET skill_id = 16 
WHERE skill_id = 22;


-- 3. Remplacement de l'ID 8 par 12
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
   11. SUPPRESSION DES TABLES DEVENUES INUTILES
   ============================================================ */

DROP TABLE b_volunteer_call;

DROP TABLE b_call;

DROP TABLE b_skill_category;

DROP TABLE b_type;


-- avant de suppimer b_volunteer
BEGIN;

ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT IF EXISTS fk_volunteer_training_volunteer;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;

DROP TABLE public.b_volunteer;







