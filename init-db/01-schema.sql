-- ============================================================
-- VOLUNTEER MANAGEMENT SYSTEM DATABASE SCRIPT
-- ============================================================

-- 1. Reference Tables (Statuses and Skills)
CREATE TABLE application_statuses (
    status_id SERIAL PRIMARY KEY,
    status_label VARCHAR(50) UNIQUE NOT NULL -- 'Pending', 'Approved', 'Rejected', 'Withdrawn', 'Completed'
);

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(100) UNIQUE NOT NULL -- 'First Aid', 'IT Support', 'Teaching', 'Cooking', etc.
);

-- 2. User Management
-- Base table for login credentials
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    phone_number VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_type VARCHAR(20) CHECK (user_type IN ('VOLUNTEER', 'ORGANIZATION', 'ADMIN'))
);

-- Profile specific to Volunteers
CREATE TABLE volunteers (
    volunteer_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    availability_notes TEXT, -- e.g., 'Weekends only', 'Evenings'
    bio TEXT
);

-- Profile specific to Organizations (NGOs, Charities)
CREATE TABLE organizations (
    organization_id INT PRIMARY KEY REFERENCES users(user_id) ON DELETE CASCADE,
    organization_name VARCHAR(200) NOT NULL,
    description TEXT,
    website_url VARCHAR(255),
    verification_status BOOLEAN DEFAULT FALSE
);

-- 3. Missions (Opportunities)
CREATE TABLE missions (
    mission_id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(organization_id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(150),
    start_date DATE NOT NULL,
    end_date DATE,
    volunteers_needed INT DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Junction Tables (Skill Matching)
CREATE TABLE volunteer_skills (
    volunteer_id INT REFERENCES volunteers(volunteer_id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE,
    proficiency_level VARCHAR(50), -- 'Beginner', 'Intermediate', 'Expert'
    PRIMARY KEY (volunteer_id, skill_id)
);

CREATE TABLE mission_requirements (
    mission_id INT REFERENCES missions(mission_id) ON DELETE CASCADE,
    skill_id INT REFERENCES skills(skill_id) ON DELETE CASCADE,
    is_mandatory BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (mission_id, skill_id)
);

-- 5. THE CORE: Volunteer Applications (Requests Management)
CREATE TABLE applications (
    application_id SERIAL PRIMARY KEY,
    volunteer_id INT NOT NULL REFERENCES volunteers(volunteer_id) ON DELETE CASCADE,
    mission_id INT NOT NULL REFERENCES missions(mission_id) ON DELETE CASCADE,
    status_id INT NOT NULL DEFAULT 1 REFERENCES application_statuses(status_id),
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    motivation_letter TEXT,
    org_feedback TEXT, -- Internal notes from the organization
    processed_at TIMESTAMP, -- When the status was last updated by the org
    
    -- Constraint: A volunteer cannot apply to the same mission twice
    CONSTRAINT unique_application UNIQUE (volunteer_id, mission_id)
);

-- 6. Audit Trail (History of status changes)
CREATE TABLE application_history (
    history_id SERIAL PRIMARY KEY,
    application_id INT REFERENCES applications(application_id) ON DELETE CASCADE,
    old_status_id INT REFERENCES application_statuses(status_id),
    new_status_id INT REFERENCES application_statuses(status_id),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by_user_id INT REFERENCES users(user_id)
);

-- ============================================================
-- INITIAL DATA SEEDING (Example Data)
-- ============================================================

INSERT INTO application_statuses (status_label) VALUES 
('Pending'), ('Approved'), ('Rejected'), ('Withdrawn'), ('Completed');

INSERT INTO skills (skill_name) VALUES 
('Logistics'), ('Medical Care'), ('Translation'), ('Social Media'), ('Event Planning');

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