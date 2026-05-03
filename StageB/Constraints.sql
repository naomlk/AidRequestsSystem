
-------------------------
-- REQUEST TABLE --------
-------------------------
-- priority level is an integer between 1 and 5
ALTER TABLE request
ADD CONSTRAINT chk_prioriry_level
CHECK (prioriry_level BETWEEN 1 AND 5);




-------------------------
-- LOCATION TABLE -------
-------------------------

ALTER TABLE location
ADD CONSTRAINT chk_coordinates
CHECK (
    latitude BETWEEN 29.0 AND 34.0 
    AND 
    longitude BETWEEN 34.0 AND 36.0
);

-------------------------
-- TREATMENT TABLE ------
-------------------------

-- verify there isnt an event with long duration >= 24 hours
ALTER TABLE treatment
ADD CONSTRAINT chk_treatment_duration
CHECK (
    completion_time IS NULL
    OR completion_time - start_time <= INTERVAL '24 hours'
);
-- check if the finish time > start time
ALTER TABLE treatment
ADD CONSTRAINT chk_treatment_time_order
CHECK (
    completion_time IS NULL OR completion_time >= start_time
);

