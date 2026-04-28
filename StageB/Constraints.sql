
-------------------------
-- REQUEST TABLE --------
-------------------------
-- priority level is an integer between 1 and 5
ALTER TABLE request
ADD CONSTRAINT chk_priority_level
CHECK (priority_level BETWEEN 1 AND 5);




-------------------------
-- LOCATION TABLE -------
-------------------------

ALTER TABLE location
ADD CONSTRAINT chk_coordinates
CHECK (latitude BETWEEN -200 AND 200 AND longitude BETWEEN -380 AND 380);

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


ALTER TABLE treatment
ADD CONSTRAINT chk_treatment_completed_has_completion_time
CHECK (
    (status_id = 3 AND completion_time IS NOT NULL)     -- completed treatment and finish time
    OR
    (status_id <> 3)          -- or not completed treatment and finish time is optional
);