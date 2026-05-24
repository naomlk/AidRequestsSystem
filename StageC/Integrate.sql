/* ============================================================
   FICHIER DES CHANGEMENTS POUR L’INTÉGRATION DES BASES
   Objectif :
   - Adapter les tables du groupe A et du groupe B
   - Transférer les données utiles
   - Rediriger certaines contraintes vers les tables finales
   ============================================================ */


/* ============================================================
   1. MODIFICATIONS DE LA TABLE a_volunteer
   ============================================================ */

-- On garde la colonne is_active au lieu de availability_status.
-- Si availability_status existe encore, on convertit ses valeurs dans is_active.

UPDATE public.a_volunteer
SET is_active = CASE
    WHEN availability_status = 'Busy' THEN 'Y'
    WHEN availability_status = 'Available' THEN 'N'
    ELSE is_active 
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
   7. MODIFICATION DE b_availability
   ============================================================ */

-- Modification de la contrainte de b_availability pour référencer a_volunteer.

BEGIN;

ALTER TABLE public.b_availability
DROP CONSTRAINT availability_pkey;

ALTER TABLE public.b_availability
ADD CONSTRAINT availability_pkey
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

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



/* ============================================================
   11. SUPPRESSION DES TABLES DEVENUES INUTILES
   ============================================================ */

DROP TABLE b_volunteer_call;

DROP TABLE b_call;


--


INSERT INTO public.a_requestcategory (
    category_id,
    category_name,
    description
)
VALUES
    (5, 'Flat Tire Assistance', NULL),
    (6, 'Locked Vehicle', NULL),
    (7, 'Stuck In Elevator', NULL),
    (8, 'Child Locked In Car', NULL),
    (9, 'Locked Home Door', NULL),
    (10, 'Search And Rescue', NULL);


-- surppiemr ces categiry car on les a deja ! 
DELETE FROM public.a_requestcategory
WHERE category_id = 7;

DELETE FROM public.a_requestcategory
WHERE category_id = 9;

DELETE FROM public.a_requestcategory
WHERE category_id = 10;


-- avant de suppimer b_volunteer
BEGIN;

ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT volunteer_training_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

COMMIT;

DELETE FROM b_volunteer;


DELETE FROM b_type;

DROP TABLE b_volunteer_call;
DROP TABLE b_call;


-- 
ALTER TABLE public.b_availability
DROP CONSTRAINT availability_volunteer_id_fkey ;


ALTER TABLE public.b_availability
ADD CONSTRAINT availability_volunteer_id_fkey
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);

--
DROP TABLE b_volunteer;

DROP TABLE b_type;
