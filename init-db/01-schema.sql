-- ============================================================
-- YEDIDIM: FAMILY SUPPORT & LOGISTICS DATABASE SCRIPT (GROUP 3)
-- ============================================================

-- 1. Reference Tables (Configuration)
CREATE TABLE request_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL, 
    description TEXT,
    required_skills VARCHAR(255) -- e.g., 'Locksmith', 'Heavy Lifting'
);

CREATE TABLE statuses (
    status_id SERIAL PRIMARY KEY,
    status_label VARCHAR(50) NOT NULL -- 'Pending', 'Assigned', 'In Progress', 'Completed'
);

-- 2. Locations (Centralized for Families & Volunteers)
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    street VARCHAR(150),
    house_number VARCHAR(20),
    coordinates POINT, -- Stores Latitude and Longitude
    latitude DECIMAL(9,6), -- Optionnel si tu préfères deux colonnes séparées
    longitude DECIMAL(9,6)
);

-- 3. Volunteers (Human Resources)
CREATE TABLE volunteers (
    volunteer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    availability_status VARCHAR(50) DEFAULT 'Available', -- 'Available', 'Busy', 'Offline'
    has_equipment BOOLEAN DEFAULT FALSE,
    skill_type VARCHAR(255), -- e.g., 'Plumber', 'Serrurier', 'First Aid'
    counter INT DEFAULT 0, -- Total interventions completed
    location_id INT REFERENCES locations(location_id) -- Link to their base area
);

-- 4. Families (The Requesters)
CREATE TABLE families (
    family_id SERIAL PRIMARY KEY,
    last_name VARCHAR(150) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address TEXT, -- Display address
    number_of_members INT DEFAULT 1,
    special_features TEXT -- e.g., 'Elderly', 'Reservist Family', 'Evacuee'
);

-- 5. THE CORE: Assistance Requests
CREATE TABLE requests (
    request_id SERIAL PRIMARY KEY,
    family_id INT NOT NULL REFERENCES families(family_id) ON DELETE CASCADE,
    category_id INT NOT NULL REFERENCES request_categories(category_id),
    status_id INT NOT NULL DEFAULT 1 REFERENCES statuses(status_id),
    location_id INT NOT NULL REFERENCES locations(location_id),
    
    priority_level INT DEFAULT 3, -- 1 (Low) to 5 (Critical)
    incident_description TEXT,
    image_url VARCHAR(255), -- Link to a photo of the emergency
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Logistics: Deliveries (Water, Medicine, etc.)
CREATE TABLE deliveries (
    delivery_id SERIAL PRIMARY KEY,
    request_id INT NOT NULL REFERENCES requests(request_id) ON DELETE CASCADE,
    item_type VARCHAR(100), -- e.g., 'Water Packs', 'Oxygen Tank'
    quantity INT DEFAULT 1,
    delivery_date DATE,
    status VARCHAR(50) DEFAULT 'Pending' -- 'In Prep', 'Out for Delivery', 'Delivered'
);

-- 7. Interventions (The actual Action)
CREATE TABLE treatments (
    treatment_id SERIAL PRIMARY KEY,
    request_id INT NOT NULL REFERENCES requests(request_id) ON DELETE CASCADE,
    volunteer_id INT NOT NULL REFERENCES volunteers(volunteer_id),
    delivery_id INT REFERENCES deliveries(delivery_id), -- Optional, only if it's a delivery
    
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_time TIMESTAMP,
    photo_after VARCHAR(255), -- Proof of completion
    feedback_notes TEXT
);

-- ============================================================
-- INITIAL DATA SEEDING (English)
-- ============================================================

INSERT INTO statuses (status_label) VALUES 
('Pending'), ('Assigned'), ('In Progress'), ('Completed'), ('Cancelled');

INSERT INTO request_categories (category_name, description, required_skills) VALUES 
('Stuck Elevator', 'Rescue mission for people trapped in elevators', 'Elevator Training'),
('Emergency Home Opening', 'Unlocking doors for locked-in children or elderly', 'Locksmith'),
('MAMD Security', 'Helping elderly close/open heavy shelter doors', 'Physical Strength'),
('Water Supply', 'Delivery of water packs to families without supply', 'Heavy Lifting'),
('Medical Equipment', 'Urgent delivery of oxygen tanks or medication', 'Medical Awareness');