INSERT INTO volunteers (
    volunteer_id, 
    first_name, 
    last_name, 
    date_of_birth, 
    availability_notes, 
    bio
) 
VALUES (
    209727361, 
    'Ochrith', 
    'Perez', 
    '2002-03-22', 
    'Weekends only', 
    'Enthusiastic volunteer with a passion for helping.'
);


INSERT INTO users (user_id, email, password_hash, type_utilisateur) 
VALUES (209727361, 'ochrith@email.com', 'password123', 'VOLONTEER');


commit;