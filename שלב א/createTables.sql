-- ======================================================
-- STEP 1: INDEPENDENT TABLES (Parent Tables)
-- These tables do not have foreign keys.
-- ======================================================

-- Stores the various states of a request (e.g., Pending, In Progress, Completed)
CREATE TABLE STATUS (
    status_id INT PRIMARY KEY,
    status_label VARCHAR(50) NOT NULL
);


CREATE TABLE REQUESTCATEGORY (
    Category_id INT PRIMARY KEY,
    Category_name VARCHAR(100) NOT NULL,
    description TEXT,
    required_skills VARCHAR(255)
);


CREATE TABLE LOCATION (
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    city VARCHAR(100) NOT NULL,
    street VARCHAR(100),
    house_number INT,
    PRIMARY KEY (latitude, longitude)
);

-- Information about the families receiving aid
CREATE TABLE FAMILY (
    ContactPerson_id INT PRIMARY KEY,
    ContactPerson_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    -- Constraint: A family must have at least one member
    number_of_members INT CHECK (number_of_members > 0),
    special_features TEXT
);

-- ======================================================
-- STEP 2: TABLES WITH DEPENDENCIES
-- These tables reference the parent tables above.
-- ======================================================

-- Volunteers who provide help
CREATE TABLE VOLUNTEER (
    volunteer_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    has_equipment BOOLEAN,
    availability_status VARCHAR(50),
    counter INT DEFAULT 0, -- Tracks the number of missions completed
    skill_type VARCHAR(100),
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    FOREIGN KEY (latitude, longitude) REFERENCES LOCATION(latitude, longitude)
);

-- The central request table
CREATE TABLE REQUEST (
    Request_id INT PRIMARY KEY,
    date DATE NOT NULL,
    image VARCHAR(255), -- Path or URL to the incident photo
    incident_description TEXT,
    -- Constraint: Priority must be between 1 (Low) and 5 (Critical)
    prioriry_level INT CHECK (prioriry_level BETWEEN 1 AND 5),
    ContactPerson_id INT REFERENCES FAMILY(ContactPerson_id),
    Category_id INT REFERENCES REQUESTCATEGORY(Category_id),
    status_id INT REFERENCES STATUS(status_id),
    --treatment_id INT REFERENCES TREATMENT(treatment_id),
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    FOREIGN KEY (latitude, longitude) REFERENCES LOCATION(latitude, longitude)
);

-- Tracks physical items being sent to a family
CREATE TABLE DELIVERY (
    delivery_id INT PRIMARY KEY,
    date DATE NOT NULL,
    status VARCHAR(50),
    item_type VARCHAR(100),
    -- Constraint: Quantity cannot be zero or negative
    quantity INT CHECK (quantity > 0),
    Request_id INT REFERENCES REQUEST(Request_id)
);

-- Records the actual action taken by a volunteer
CREATE TABLE TREATMENT (
    treatment_id INT PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME,
    completion_time TIME,
    feedback_notes TEXT,
    photo_after VARCHAR(255),
    delivery_id INT REFERENCES DELIVERY(delivery_id),
    volunteer_id INT REFERENCES VOLUNTEER(volunteer_id),
    request_id INT REFERENCES REQUEST(request_id)
);


-- ======================================================
-- STEP 1: INDEPENDENT TABLES (Parent Tables)
-- These tables do not have foreign keys.
-- ======================================================

-- Stores the various states of a request (e.g., Pending, In Progress, Completed)
CREATE TABLE STATUS (
    status_id INT PRIMARY KEY,
    status_label VARCHAR(50) NOT NULL
);


CREATE TABLE REQUESTCATEGORY (
    Category_id INT PRIMARY KEY,
    Category_name VARCHAR(100) NOT NULL,
    description TEXT,
    required_skills VARCHAR(255)
);


CREATE TABLE LOCATION (
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    city VARCHAR(100) NOT NULL,
    street VARCHAR(100),
    house_number INT,
    PRIMARY KEY (latitude, longitude)
);

-- Information about the families receiving aid
CREATE TABLE FAMILY (
    ContactPerson_id INT PRIMARY KEY,
    ContactPerson_name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20),
    -- Constraint: A family must have at least one member
    number_of_members INT CHECK (number_of_members > 0),
    special_features TEXT
);

-- ======================================================
-- STEP 2: TABLES WITH DEPENDENCIES
-- These tables reference the parent tables above.
-- ======================================================

-- Volunteers who provide help
CREATE TABLE VOLUNTEER (
    volunteer_id INT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    has_equipment BOOLEAN,
    availability_status VARCHAR(50),
    counter INT DEFAULT 0, -- Tracks the number of missions completed
    skill_type VARCHAR(100),
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    FOREIGN KEY (latitude, longitude) REFERENCES LOCATION(latitude, longitude)
);

-- The central request table
CREATE TABLE REQUEST (
    Request_id INT PRIMARY KEY,
    date DATE NOT NULL,
    image VARCHAR(255), -- Path or URL to the incident photo
    incident_description TEXT,
    -- Constraint: Priority must be between 1 (Low) and 5 (Critical)
    prioriry_level INT CHECK (prioriry_level BETWEEN 1 AND 5),
    ContactPerson_id INT REFERENCES FAMILY(ContactPerson_id),
    Category_id INT REFERENCES REQUESTCATEGORY(Category_id),
    status_id INT REFERENCES STATUS(status_id),
    --treatment_id INT REFERENCES TREATMENT(treatment_id),
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    FOREIGN KEY (latitude, longitude) REFERENCES LOCATION(latitude, longitude)
);

-- Tracks physical items being sent to a family
CREATE TABLE DELIVERY (
    delivery_id INT PRIMARY KEY,
    date DATE NOT NULL,
    status VARCHAR(50),
    item_type VARCHAR(100),
    -- Constraint: Quantity cannot be zero or negative
    quantity INT CHECK (quantity > 0),
    Request_id INT REFERENCES REQUEST(Request_id)
);

-- Records the actual action taken by a volunteer
CREATE TABLE TREATMENT (
    treatment_id INT PRIMARY KEY,
    date DATE NOT NULL,
    start_time TIME,
    completion_time TIME,
    feedback_notes TEXT,
    photo_after VARCHAR(255),
    delivery_id INT REFERENCES DELIVERY(delivery_id),
    volunteer_id INT REFERENCES VOLUNTEER(volunteer_id),
    request_id INT REFERENCES REQUEST(Request_id) 

);
