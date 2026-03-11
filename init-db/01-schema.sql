-- ============================================================
-- VOLUNTEER MANAGEMENT SYSTEM DATABASE SCRIPT
-- ============================================================

-- 1. Reference Tables (Configuration)
CREATE TABLE request_types (
    type_id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) NOT NULL -- e.g., 'Battery', 'Flat Tire', 'Locked Car'
);

CREATE TABLE statuses (
    status_id SERIAL PRIMARY KEY,
    status_label VARCHAR(50) NOT NULL -- 'Pending', 'Assigned', 'In Progress', 'Completed'
);

-- 2. Locations
-- Centralized table for tracking where the help is needed
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    street VARCHAR(150),
    neighborhood VARCHAR(100),
    latitude DECIMAL(9,6), 
    longitude DECIMAL(9,6)
);

-- 3. Organizations & Volunteers
CREATE TABLE organizations (
    organization_id SERIAL PRIMARY KEY,
    org_name VARCHAR(200) DEFAULT 'Yedidim',
    branch_region VARCHAR(100), -- e.g., 'Jerusalem District', 'Tel Aviv'
    contact_phone VARCHAR(20)
);

CREATE TABLE volunteers (
    volunteer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    equipment_notes TEXT -- e.g., 'Has jack and professional booster'
);

-- 4. Families / Citizens (The Requesters)
CREATE TABLE families (
    family_id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    is_vulnerable BOOLEAN DEFAULT FALSE -- High priority for elderly or kids in car
);

-- 5. THE CORE: Assistance Requests
-- This table links the person in need to the specific problem and location
CREATE TABLE requests (
    request_id SERIAL PRIMARY KEY,
    family_id INT NOT NULL REFERENCES families(family_id) ON DELETE CASCADE,
    type_id INT NOT NULL REFERENCES request_types(type_id),
    status_id INT NOT NULL DEFAULT 1 REFERENCES statuses(status_id),
    location_id INT NOT NULL REFERENCES locations(location_id),
    organization_id INT REFERENCES organizations(organization_id),
    
    vehicle_info VARCHAR(255), -- e.g., 'Blue Mazda 3, Plate 12-345-67'
    incident_description TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Interventions (Deliveries of Help)
-- Tracks which volunteer handled which request
CREATE TABLE deliveries (
    delivery_id SERIAL PRIMARY KEY,
    request_id INT NOT NULL REFERENCES requests(request_id) ON DELETE CASCADE,
    volunteer_id INT NOT NULL REFERENCES volunteers(volunteer_id),
    
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    arrival_time TIMESTAMP,
    completion_time TIMESTAMP,
    
    outcome_summary TEXT, -- e.g., 'Fixed on site', 'Referred to mechanic'
    
    CONSTRAINT unique_active_delivery UNIQUE (request_id, volunteer_id)
);

-- ============================================================
-- INITIAL DATA SEEDING (English)
-- ============================================================

INSERT INTO statuses (status_label) VALUES 
('Pending'), ('Assigned'), ('In Progress'), ('Completed'), ('Cancelled');

INSERT INTO request_types (type_name) VALUES 
('Battery Jumpstart'), ('Flat Tire (Puncture)'), ('Locked Car (Child Inside)'), 
('Locked Car (Keys Inside)'), ('Out of Fuel'), ('Stuck Elevator');

INSERT INTO organizations (org_name, branch_region) VALUES 
('Yedidim', 'Jerusalem District'), ('Yedidim', 'Central District');

-- ============================================================
-- USEFUL QUERIES
-- ============================================================

-- View all pending applications for a specific organization's missions:
/*
SELECT 
    v.first_name, 
    v.last_name, 
    m.title AS mission_title, 
    a.applied_at, 
    s.status_label
FROM applications a
JOIN volunteers v ON a.volunteer_id = v.volunteer_id
JOIN missions m ON a.mission_id = m.mission_id
JOIN application_statuses s ON a.status_id = s.status_id
WHERE m.organization_id = 1 AND s.status_label = 'Pending';
*/