-- ============================================================
-- TEST DATA (INSERT)
-- ============================================================

-- 1. Insert a Family (e.g., Naomi's test data)
INSERT INTO families (last_name, phone_number, number_of_members, special_features)
VALUES ('Cohen', '052-555-0011', 5, 'Reservist Family - Father in Milouim');

-- 2. Insert a Location for the request
INSERT INTO locations (city, street, house_number, latitude, longitude)
VALUES ('Jerusalem', 'Jaffa Street', '42', 31.7833, 35.2167);

-- 3. Create a Volunteer (Top Performer)
INSERT INTO volunteers (first_name, last_name, phone_number, availability_status, skill_type, counter)
VALUES ('Oshrit', 'Perez', '050-111-2233', 'Available', 'Heavy Lifting, First Aid', 12);

-- 4. Create a Request for Water Delivery
INSERT INTO requests (family_id, category_id, status_id, location_id, priority_level, incident_description)
VALUES (1, 1, 1, 1, 4, 'Family without water due to local pipe burst. Need 3 packs.');

-- 5. Link a Delivery to that Request
INSERT INTO deliveries (request_id, item_type, quantity, delivery_date)
VALUES (1, 'Water Packs (6x1.5L)', 3, CURRENT_DATE);

commit;