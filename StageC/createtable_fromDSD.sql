CREATE TABLE LOCATION
(
  latitude INT NOT NULL,
  longitude INT NOT NULL,
  street INT NOT NULL,
  city INT NOT NULL,
  house_number INT NOT NULL,
  PRIMARY KEY (latitude, longitude),
  UNIQUE (longitude)
);

CREATE TABLE VOLUNTEER
(
  first_name INT NOT NULL,
  last_name INT NOT NULL,
  volunteer_id INT NOT NULL,
  phone_number INT NOT NULL,
  email INT NOT NULL,
  current_status INT NOT NULL,
  has_equipment INT NOT NULL,
  counter INT NOT NULL,
  recruitment_date INT NOT NULL,
  latitude INT NOT NULL,
  longitude INT NOT NULL,
  PRIMARY KEY (volunteer_id),
  FOREIGN KEY (latitude, longitude) REFERENCES LOCATION(latitude, longitude)
);

CREATE TABLE AVAILABILITY
(
  day_of_week INT NOT NULL,
  start_time INT NOT NULL,
  end_time INT NOT NULL,
  prefered_region INT NOT NULL,
  volunteer_id INT NOT NULL,
  PRIMARY KEY (day_of_week, start_time, volunteer_id),
  FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id)
);

CREATE TABLE SKILL
(
  requires_certificate INT NOT NULL,
  description INT NOT NULL,
  skill_name INT NOT NULL,
  skill_id INT NOT NULL,
  difficulty_level INT NOT NULL,
  PRIMARY KEY (skill_id)
);

CREATE TABLE CATEGORY
(
  category_id INT NOT NULL,
  category_name INT NOT NULL,
  skill_id INT NOT NULL,
  PRIMARY KEY (category_id),
  FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id)
);

CREATE TABLE TRAINING
(
  training_id INT NOT NULL,
  training_name INT NOT NULL,
  description INT NOT NULL,
  duration_hours INT NOT NULL,
  max_participants INT NOT NULL,
  PRIMARY KEY (training_id)
);

CREATE TABLE SCHEDULED
(
  meeting_date INT NOT NULL,
  start_time INT NOT NULL,
  end_time INT NOT NULL,
  address INT NOT NULL,
  training_id INT NOT NULL,
  PRIMARY KEY (meeting_date, training_id),
  FOREIGN KEY (training_id) REFERENCES TRAINING(training_id)
);

CREATE TABLE REQUESTCATEGORY
(
  Category_id INT NOT NULL,
  Category_name INT NOT NULL,
  description INT NOT NULL,
  required_skills INT NOT NULL,
  PRIMARY KEY (Category_id)
);

CREATE TABLE FAMILY
(
  ContactPerson_id INT NOT NULL,
  phone_number INT NOT NULL,
  ContactPerson_name INT NOT NULL,
  special_features INT NOT NULL,
  number_of_members INT NOT NULL,
  PRIMARY KEY (ContactPerson_id)
);

CREATE TABLE STATUS
(
  status_id INT NOT NULL,
  status_label INT NOT NULL,
  PRIMARY KEY (status_id)
);

CREATE TABLE REQUEST
(
  Request_id INT NOT NULL,
  prioriry_level INT NOT NULL,
  incident_description INT NOT NULL,
  image INT NOT NULL,
  date INT NOT NULL,
  Category_id INT NOT NULL,
  ContactPerson_id INT NOT NULL,
  status_id INT NOT NULL,
  latitude INT NOT NULL,
  longitude INT NOT NULL,
  PRIMARY KEY (Request_id),
  FOREIGN KEY (Category_id) REFERENCES REQUESTCATEGORY(Category_id),
  FOREIGN KEY (ContactPerson_id) REFERENCES FAMILY(ContactPerson_id),
  FOREIGN KEY (status_id) REFERENCES STATUS(status_id),
  FOREIGN KEY (latitude, longitude) REFERENCES LOCATION(latitude, longitude)
);

CREATE TABLE DELIVERY
(
  delivery_id INT NOT NULL,
  date INT NOT NULL,
  status INT NOT NULL,
  item_type INT NOT NULL,
  quantity INT NOT NULL,
  PRIMARY KEY (delivery_id)
);

CREATE TABLE TREATMENT
(
  treatment_id INT NOT NULL,
  start_time INT NOT NULL,
  completion_time INT NOT NULL,
  feedback_notes INT NOT NULL,
  photo_after INT NOT NULL,
  date INT NOT NULL,
  Request_id INT NOT NULL,
  delivery_id INT NOT NULL,
  volunteer_id INT NOT NULL,
  PRIMARY KEY (treatment_id),
  FOREIGN KEY (Request_id) REFERENCES REQUEST(Request_id),
  FOREIGN KEY (delivery_id) REFERENCES DELIVERY(delivery_id),
  FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id)
);

CREATE TABLE HAS_SKILL
(
  skill_id INT NOT NULL,
  volunteer_id INT NOT NULL,
  PRIMARY KEY (skill_id, volunteer_id),
  FOREIGN KEY (skill_id) REFERENCES SKILL(skill_id),
  FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id)
);

CREATE TABLE VOLUNTEER_TRAINING
(
  volunteer_id INT NOT NULL,
  training_id INT NOT NULL,
  PRIMARY KEY (volunteer_id, training_id),
  FOREIGN KEY (volunteer_id) REFERENCES VOLUNTEER(volunteer_id),
  FOREIGN KEY (training_id) REFERENCES TRAINING(training_id)
);