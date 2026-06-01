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

