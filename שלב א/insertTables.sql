-- METHOD 1: Manual Inserts
-- Static data for Status and Categories
INSERT INTO STATUS (status_id, status_label) VALUES 
(1, 'Pending'), (2, 'In Progress'), (3, 'Completed'), (4, 'Cancelled');

INSERT INTO REQUESTCATEGORY (Category_id, Category_name, description) VALUES 
(1, 'Rescue & Emergency', 'Immediate response for trapped individuals (elevators, locked rooms)'),
(2, 'Shelter & MAMD Security', 'Maintenance and rescue related to MAMD/Shelter steel doors and windows'),
(3, 'Essential Logistics', 'Urgent delivery of water packs, medical oxygen, and vital medicines'),
(4, 'Urgent Home Maintenance', 'Critical repairs like main pipe bursts or total electrical failure');

commit;