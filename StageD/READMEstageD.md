## EXEMPLE 1:

This program finds treatments that are already completed, while their related requests are still marked as **In Progress**.

In our database:

```text
status_id = 2 → In Progress
status_id = 3 → Closed
```


So, when a treatment has a `completion_time`, the request should be updated to `Closed`.

---

### 1. Manual check

First, we check if such treatments exist:

```sql
SELECT *    
FROM public.a_treatment t
JOIN public.a_request r
    ON r.request_id = t.request_id
WHERE t.completion_time IS NOT NULL
  AND r.status_id = 2;
```

**Result:** Image 1 shows completed treatments whose requests are still in progress.
<img width="1384" height="141" alt="RESULT1" src="https://github.com/user-attachments/assets/bb43471b-8b1e-47d1-a350-7682098a0a09" />

---

### 2. Function check

Then, we call the function that returns a cursor with the same data:

```sql
SELECT get_completed_treatments_not_closed();

FETCH ALL FROM completed_treatments_cursor;
```

**Result:** Image 2 shows that the function returns the expected treatments.
<img width="730" height="144" alt="RESULT2" src="https://github.com/user-attachments/assets/02f0c709-7027-4ad1-bf01-6826428cb0cb" />

---

### 3. Procedure

The procedure calls the function, receives the cursor, and reads it line by line.

For each treatment found, it updates the related request:

```sql
UPDATE public.a_request
SET status_id = 3
WHERE request_id = treatment_record.request_id;
```

It also prints a `NOTICE` message for each request that was closed.

This procedure uses:

```text
REFCURSOR, RECORD, LOOP, FETCH, UPDATE, RAISE NOTICE, EXCEPTION
```

**Result:** Image 3 shows that the procedure ran successfully.
<img width="668" height="124" alt="result3 of call procedure" src="https://github.com/user-attachments/assets/77c26077-b5b2-43f6-8c3b-b0565c3a9ddb" />

---

### 4. Final check

After calling:

```sql
CALL close_requests_from_completed_treatments();
```

we run the first query again.

**Result:** Image 4 shows no remaining rows, meaning all completed treatments now have their requests closed.

<img width="763" height="152" alt="result 4 no result after proceure calls" src="https://github.com/user-attachments/assets/97120ce3-4762-40f7-b645-0fba42dbedbc" />



finir trigge r -ajouter une requete-pusi un taritement et voir commen tle trigger agit



## EXEMPLE 2:

This program scans the database to find and fix data anomalies regarding volunteer availability. It identifies volunteers who are incorrectly marked as busy ('Y') despite having no active missions, and safely resets their status back to available ('N').

### 1. Function check : get_busy_volunteers_with_no_active_treatment

This function acts as the detector. It opens an explicit reference cursor (REFCURSOR) to query and isolate all volunteers whose status is set to busy (is_active = 'Y'), but who currently have no ongoing assignments (where completion_time IS NULL) in the treatments table.
This function uses:
REFCURSOR, EXPLICIT CURSOR, SELECT NOT EXISTS, EXCEPTION 

<img width="985" height="170" alt="image" src="https://github.com/user-attachments/assets/5ab82ddd-93ea-4288-8843-1f8681fdf9af" />

<img width="957" height="371" alt="image" src="https://github.com/user-attachments/assets/4c2cf816-a4bf-40a1-a56b-d9e6806252b0" />

### 2. Procedure : reset_volunteer_availability

This procedure is the fixer. It takes the list of blocked volunteers found by the function, loops through them one by one, and updates their status back to available ('N'). It prints a confirmation message for each volunteer and shows the total number of fixed profiles at the end.
This procedure uses:
REFCURSOR, RECORD, LOOP, FETCH, UPDATE (DML), RAISE NOTICE, EXCEPTION 

<img width="1055" height="186" alt="image" src="https://github.com/user-attachments/assets/ed426cd5-9dd4-41a1-9e17-f40ce5399127" />

We can see that it worked successfully; the table is now empty.  

<img width="1185" height="229" alt="image" src="https://github.com/user-attachments/assets/800a9319-22c3-409f-acda-22654b60a8e8" />

