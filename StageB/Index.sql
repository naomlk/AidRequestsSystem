---------------- INDEX ---------------
--------------------------------------



--1)index sur ttes les ligne
CREATE INDEX idx_treatment_volunteer
ON treatment(volunteer_id);
-- important car a chaque fois ou on fait where t.volunteer_id=v.volunteer_id  alors on aura deja
-- un index ds la table de treatment qui va nous donner ttes les lignes par volontaires comme
-- volontaire 1 = ligne 1,22,3
-- volontaire 2 =lignes 6,9,10
-- volontaire 3 =lignes 8,11,12
-- et donc quand je cherche where t.volunteer_id=v.volunteer_id  alors il va psser chaaue elem,nt de v.voluntter
-- et cherhcehr ds les ligne que lindex renvoient de treatment si le volunteer_id corepond


--2)
CREATE INDEX idx_volunteer_status_location
ON volunteer(availability_status, latitude, longitude);
-- ca va nous aider pour les requetes qui cherchent des volontaires dispo ds un perimetre donne autour
-- de la requete donc on voudra ts les volontaires "Available" et leur coordonnes pour faire el calcul et donc
-- si lindex nous renvoie un B-tree  style                           STATUS
--                                                  'Aailable'       ' Busy'     'Offline'
--                                                     /\
--                                    longitude    38      11:5
--                                                / | \
--          longitude:latitude                 10  45 85

--3)
CREATE INDEX idx_treatment_volunteer_date
ON treatment(volunteer_id, date);


-- example in use:
--WHERE t.volunteer_id = v.volunteer_id
-- AND t.date >= ...