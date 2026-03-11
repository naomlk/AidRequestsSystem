
-- 1. Insert into Users first (Parent table)
-- Note: 'VOLONTEER' is changed to 'VOLUNTEER' to match English standards
INSERT INTO users (user_id, email, password_hash, user_type) 
VALUES 
(209727361, 'ochrith@email.com', 'hash_secure_123', 'VOLUNTEER'),
(345887640, 'naomi@email.com', 'hash_secure_456', 'VOLUNTEER');

-- 2. Insert into Volunteers (Child table)
-- We use the same user_id to link the profiles
INSERT INTO volunteers (volunteer_id, first_name, last_name, phone_number, equipment_notes) 
VALUES 
(209727361, 'Oshrit', 'Perez', '050-111-2233', 'Has jumper cables and a car jack. Available weekends.'),
(345887640, 'Naomi', 'Malka', '054-999-8877', 'Professional toolset. Specialized in door unlocking.');

-- 3. Insert some test Families (The People in Need)
INSERT INTO families (full_name, phone_number, is_vulnerable)
VALUES 
('Cohen Family', '052-555-0011', FALSE),
('Levy Family', '058-444-2233', TRUE); -- Vulnerable (e.g., stuck with a baby)

-- 4. Insert a test Location
INSERT INTO locations (city, street, neighborhood)
VALUES ('Jerusalem', 'Jaffa Street', 'City Center');

-- 5. Create a test Request
-- This links the Cohen Family to a Flat Tire problem
INSERT INTO requests (family_id, type_id, status_id, location_id, vehicle_info, incident_description)
VALUES (1, 2, 1, 1, 'Silver Toyota Corolla', 'Stuck in the parking lot with a flat tire.');

commit;
