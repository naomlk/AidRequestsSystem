-- ============================================================
-- Main Program: Completed Treatments Cleanup
-- Goal:
-- 1. Show completed treatments whose requests are still In Progress status.
-- 2. Call the procedure that closes these requests.
-- 3. Show that the treatments no longer appear after the update.
-- ============================================================

BEGIN;

-- Before: open the cursor using the function
SELECT get_completed_treatments_not_closed();

-- print all rows returned by the cursor before the procedure
FETCH ALL FROM completed_treatments_cursor;

COMMIT;


-- Call the procedure that uses the same logic and updates the requests
CALL close_requests_from_completed_treatments();


BEGIN;

-- After: open the cursor again using the function
SELECT get_completed_treatments_not_closed();

-- If the procedure worked, this should return 0 rows
FETCH ALL FROM completed_treatments_cursor;

COMMIT;