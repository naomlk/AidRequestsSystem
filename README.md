# Project Report: Family Aid Request Management System - Yedidim

Submitters: Naomi Malka & Oshrit Peretz  
System: Yedidim  
Module: Family Assistance Unit  

## Stage 1
## Introduction
The "Yedidim" Family Aid System is a specialized branch of the broader Yedidim organization, dedicated to providing immediate logistical and humanitarian support to families in crisis. This system centralizes the management of urgent requests, enabling efficient family registration and strategic volunteer deployment based on professional skills and real-time geographic data. By tracking every request from inception to completion, the platform ensures that vital assistance is delivered precisely where it is needed most.

A core focus of this system is to support vulnerable families during times of war, national crises, or severe hardship. During these challenging periods, the system prioritizes essential maintenance and logistical aid to ensure the safety and well-being of those who lack the resources to cope with emergency infrastructure failures or supply shortages.

The system is designed to handle four critical categories of assistance:

Rescue & Emergency (חילוץ ותגובה מיידית):
Examples: Rescuing people trapped in elevators or a child locked inside a room/house.

Shelter & MAMD Security (אבטחת מרחב מוגן ותחזוקה - ממ"ד):
Importance: Critical during security alerts and war.
Examples: Rescuing individuals trapped inside a residential shelter (MAMD) due to a jammed door, or repairing heavy steel doors and windows that fail to operate correctly.

Essential Logistics - Deliveries (לוגיסטיקה חיונית - משלוחים):
Note: This category specifically activates the Delivery entity.
Context: Vital during lockdowns or conflict when families cannot leave their homes.
Examples: Urgent delivery of water packs (6x1.5L) or medical equipment (oxygen tanks, emergency medications).

Urgent Home Maintenance (תחזוקת בית דחופה):
Context: Humanitarian aid for families with infants or medical needs facing total utility failure.
Examples: Main pipe bursts or total electrical failure in the home.

Core Functionalities:
To ensure operational excellence, the system provides real-time monitoring and control over the status of aid requests. It manages the logistical documentation for all deliveries associated with specific incidents and records volunteer actions in the field—including precise timestamps and qualitative feedback notes—to guarantee the highest standard of service for every family served.

## User Interface (UI)
<img width="1918" height="874" alt="image" src="https://github.com/user-attachments/assets/56e186fa-1aa2-4d56-b0d1-a74ae6dec616" />
<img width="1919" height="865" alt="image" src="https://github.com/user-attachments/assets/75ed4896-9e63-49b0-95ff-03be5448e482" />
<img width="1913" height="874" alt="image" src="https://github.com/user-attachments/assets/60273847-0ea7-4c43-8cac-0be7eab27510" />
<img width="1919" height="870" alt="image" src="https://github.com/user-attachments/assets/78478b7f-0eb5-4c40-9b32-a343f18878a8" />
<img width="1919" height="831" alt="image" src="https://github.com/user-attachments/assets/cda3d205-c4e1-43c8-a01b-dc6044be96fe" />


## ERD - Entity Relationship Diagram
<img width="1418" height="669" alt="image" src="https://github.com/user-attachments/assets/3ae6ce8d-b7cc-4da6-a6ee-0d385e563343" />

## DSD - Data Structure Diagram
<img width="3744" height="1605" alt="DSD" src="https://github.com/user-attachments/assets/dc9c6669-e33e-496a-9459-e3bdfb694adb" />


## Data Insertion Methods
We utilized three distinct methods to populate the database:

 Manual INSERT Commands : Used for static reference tables such as STATUS and REQUESTCATEGORY. 
<img width="1381" height="418" alt="image" src="https://github.com/user-attachments/assets/5fafb2c5-7958-4ad9-b543-a5e82dd07ded" />


External Data Generation (Mockaroo): Used to generate 500 realistic records for the FAMILY, LOCATION, and VOLUNTEER tables.
<img width="485" height="146" alt="image" src="https://github.com/user-attachments/assets/1513bc0d-f9fe-4fa2-a800-e6398ea06741" />
<img width="1716" height="453" alt="image" src="https://github.com/user-attachments/assets/cc34d80c-33b6-4052-8e68-a204efb7d010" />



Automated Python Scripting : A custom Python script (generate_data.py) was developed to generate 20,000 records for both the REQUEST and TREATMENT tables. Also for DELIVERY table but not as many lines.  This method ensured logical consistency between foreign keys across the massive dataset.
<img width="1426" height="962" alt="image" src="https://github.com/user-attachments/assets/564c08ea-63c5-46a8-808a-187e288517bf" />
<img width="1841" height="796" alt="image" src="https://github.com/user-attachments/assets/1918378e-4bd7-49a9-8ccb-fb27ea3805c4" />


## Backup 
<img width="1301" height="73" alt="image" src="https://github.com/user-attachments/assets/4691529b-8f7e-4bcd-af61-8f93e031b298" />
<img width="1104" height="33" alt="image" src="https://github.com/user-attachments/assets/857ad52c-5f94-4070-b5c7-93e3e3f8f625" />
<img width="388" height="298" alt="image" src="https://github.com/user-attachments/assets/8e07045a-cdaf-45f2-9e49-bfbfcf836d8f" />


## Stage 2 

## Queries Documentation 

### 1. Top 15 Families by Number of Requests 
Description: This query identifies the families that have requested assistance the most. It helps the organization prioritize support for families with recurring needs.
   
<img width="1195" height="333" alt="image" src="https://github.com/user-attachments/assets/911ebd1d-33fa-47ec-b4da-0c688550b7a2" /> 
<img width="1181" height="332" alt="image" src="https://github.com/user-attachments/assets/b98c4b9d-5076-40de-9220-5a8c8ca2bf5e" /> 
<img width="611" height="264" alt="image" src="https://github.com/user-attachments/assets/a643c422-0ca2-4d88-acfc-f96e9f9c78e4" />

Version 1 (JOIN) is better because it processes all data in one single operation, making it much faster and more professional. Version 2 (Subquery) is inefficient because it forces the database to repeat the search 500 times (once for every family) like a slow loop. Using the JOIN version ensures the Yedidim system is scalable and follows engineering best practices for handling large amounts of data.


### 2. 2026 Northern Region Service Requests 
Description: This query retrieves all assistance requests submitted within the Northern region of Israel during the current year. It filters locations by latitude (32.3°N and above) and joins with the city database to provide a clear overview of recent emergency activity in northern urban centers.

<img width="1242" height="280" alt="image" src="https://github.com/user-attachments/assets/95e05c2b-836c-4aa8-951c-e349d711e755" />
<img width="1443" height="380" alt="image" src="https://github.com/user-attachments/assets/5fd34a6c-a0ef-44c9-a9de-9c621f646734" />

<img width="992" height="373" alt="image" src="https://github.com/user-attachments/assets/fc0dda1e-7f70-4845-bbc3-e80548889a06" />

Version 1 (JOIN) is the professional standard because it links the tables using a composite key (Latitude + Longitude) in a single, fluid operation, allowing PostgreSQL to quickly filter the Northern region and dates simultaneously.

Version 2 (Subquery) is less efficient because for every single request found in 2026, the database must stop and perform a manual search in the Location table to find the city name. This creates a "bottleneck" that slows down the system as the number of requests grows.

By using Version 1, you ensure that the Yedidim system can handle high traffic in the Northern region without performance lag, following the same scalability principles as your previous queries.


### 3. Filtered Treatments by Specific Date Range 
Description: Retrieves all completed interventions within a specific month. Useful for generating monthly activity reports.

<img width="1179" height="250" alt="image" src="https://github.com/user-attachments/assets/4fcecb99-f2cf-48c6-9f3a-5122a15caca1" /> 
<img width="1166" height="251" alt="image" src="https://github.com/user-attachments/assets/20ee4813-73e4-4305-b0bc-b0922d45f69e" /> 
<img width="713" height="275" alt="image" src="https://github.com/user-attachments/assets/362ce76e-2282-4e9b-8e81-0b66fceedebb" />

Version 1 (BETWEEN) is much more efficient than Version 2 (EXTRACT).
Indexing: Version 1 allows the database to use an Index on the date column, which makes the search nearly instant.
Speed: In Version 2, the database must calculate the month and year for every single one of your 20,000 rows, which is much slower and uses more CPU.
Performance: Version 1 points directly to a specific "block" of time, while Version 2 forced the database to scan the entire table.


### 4. Volunteers Without Equipment 
Description: Lists volunteers who do not have their own tools. This helps coordinators know who needs to be supplied with equipment before a mission.

<img width="1188" height="287" alt="image" src="https://github.com/user-attachments/assets/4677707c-fb48-43f3-b2b7-08befd63428b" /> 
<img width="1188" height="280" alt="image" src="https://github.com/user-attachments/assets/9196f030-042a-4cbc-8b74-c104cbeff2c1" /> 
<img width="755" height="265" alt="image" src="https://github.com/user-attachments/assets/3252e5ce-9d22-4a8a-9677-3b139e12fd9d" />

Version 1 (WHERE) is the professional choice because it performs a direct filter in a single pass over the table. Version 2 (EXCEPT) is inefficient because it forces the database to perform two separate queries (one to get everyone and one to get those with equipment) and then calculate the difference between the two sets. For the Yedidim project, Version 1 is much faster and uses far less memory than the mathematical set operation in Version 2.


### 5. Elite Volunteer Service Report (>100km) 
Description: This query lists unique volunteers who have completed high-effort missions exceeding 100km.

<img width="1211" height="679" alt="image" src="https://github.com/user-attachments/assets/d5f0d698-2d72-4828-a2ea-2be8b8767912" />

<img width="895" height="298" alt="image" src="https://github.com/user-attachments/assets/cc604c0d-125b-44b6-a913-9904717209a1" />



### 6. Top Performing Volunteers (Above Average Activity) 
Description: An analytical query using a subquery to find volunteers whose number of completed missions is higher than the general average.

<img width="1165" height="257" alt="image" src="https://github.com/user-attachments/assets/34378d1b-cf8b-4f22-8240-9e5535e59a19" /> 
<img width="658" height="258" alt="image" src="https://github.com/user-attachments/assets/f755995b-8202-4b01-9660-de0ac8c37ab8" />



### 7. Monthly Requests Summary 
Description: Provides a high-level overview of the workload per month and year, allowing the organization to see seasonal trends in aid requests.

<img width="1117" height="285" alt="image" src="https://github.com/user-attachments/assets/bcb74688-2990-43ba-ae12-ea2468e3ecc8" /> 
<img width="476" height="268" alt="image" src="https://github.com/user-attachments/assets/0eb94255-fab7-4ebd-84ec-3d63d8c325f3" />



### 8. Geographic Distribution by City 
Description: This query analyzes the distribution of aid requests across different cities. By joining the LOCATION, REQUEST, and REQUESTCATEGORY tables, it displays the volume of requests for specific types of aid in each urban area.

<img width="1191" height="283" alt="image" src="https://github.com/user-attachments/assets/909351f7-8a1c-4375-af64-b20184375db5" />

<img width="725" height="303" alt="image" src="https://github.com/user-attachments/assets/a0bcc968-067f-4b85-976c-0dd706c0e54a" />










## Delete queries 

### 1. Removing Inactive Volunteers (No Activity for 1 Year)
Description: Identifies and removes volunteers with no recorded activity in the last 12 months to ensure a high-quality, active database. 

<img width="1566" height="306" alt="image" src="https://github.com/user-attachments/assets/9f40ab31-fed0-4790-9532-afae6e0de486" /> 
<img width="1220" height="393" alt="image" src="https://github.com/user-attachments/assets/82b4624a-0c66-4e54-b8f2-e90848ec4036" /> 

<img width="1562" height="295" alt="image" src="https://github.com/user-attachments/assets/5a5419d6-4117-4612-98e9-25ce75d44df6" /> 

### 2. Deleting not used locations
Description: Purges orphaned geographic records from the LOCATION table that are no longer associated with any registered family or service request. 

<img width="1237" height="346" alt="image" src="https://github.com/user-attachments/assets/79ecf89c-bd15-4257-b125-0e09b242b089" />
<img width="846" height="513" alt="image" src="https://github.com/user-attachments/assets/cd6152d9-8a97-4686-b1be-848f8163964a" />
<img width="1212" height="350" alt="image" src="https://github.com/user-attachments/assets/56d02deb-758c-45d4-9d6e-d6087231b534" />


### 3. Deleting cancelled requests
Description: Purges cancelled requests with no associated treatment records
<img width="1533" height="279" alt="image" src="https://github.com/user-attachments/assets/25e37adb-bb82-4df3-ae7d-81812a01c3a4" />
<img width="935" height="519" alt="image" src="https://github.com/user-attachments/assets/b3d04d88-9844-4668-b75d-302a8267e328" />
<img width="1565" height="255" alt="image" src="https://github.com/user-attachments/assets/6819c5d8-f7a5-4be6-b8ac-1509846ec8c7" />

## Update queries 

### 1. Request Priority Escalation
Description: Increases the priority level of pending requests older than 2 days.
<img width="1569" height="276" alt="image" src="https://github.com/user-attachments/assets/9da74140-9742-4283-bfba-4f78239914e4" />
<img width="1249" height="320" alt="image" src="https://github.com/user-attachments/assets/94dd6066-9ecd-422e-9704-e08a67dbe8d2" />
<img width="1497" height="286" alt="image" src="https://github.com/user-attachments/assets/a1664fc0-16a0-4c5c-b42d-2ca99c6ce6ab" />

### 2. Updates the request status to Completed
Description: Updates the request status to 3 (Completed) for all missions that have a recorded completion time in the treatment table. 

<img width="1561" height="247" alt="image" src="https://github.com/user-attachments/assets/5978763b-645b-4dd0-af69-4e841ab284f8" />
<img width="1559" height="287" alt="image" src="https://github.com/user-attachments/assets/7ef9e1fe-d2e0-453d-97f4-f782877ec5bb" />
<img width="1240" height="434" alt="image" src="https://github.com/user-attachments/assets/837e0813-cfb7-440b-bab2-8f4076dce5db" />
<img width="1560" height="291" alt="image" src="https://github.com/user-attachments/assets/ddecbc3e-435c-4834-9001-d73ff9819ced" />


### 3. Updates the count of treatment of volunteers
Description: Updates each volunteer’s mission counter by calculating the total number of treatments they have completed.
<img width="1370" height="185" alt="Capture d’écran 2026-04-28 095244" src="https://github.com/user-attachments/assets/d0a42e80-fa60-4bde-89d6-52f4861be85a" />
<img width="1370" height="185" alt="Capture d’écran 2026-04-28 095244" src="https://github.com/user-attachments/assets/c8e89683-f75a-4906-b255-f8723a48cb07" />
<img width="805" height="166" alt="Capture d’écran 2026-04-28 095125" src="https://github.com/user-attachments/assets/f0edf925-9208-4389-bc4e-599f00b7ee68" />



## Commit And Rollback
The purpose of this section is to demonstrate the difference between the ROLLBACK and COMMIT commands in PostgreSQL transactions.

# Rollback
Description: we perform data modifications (UPDATE and DELETE) and then use ROLLBACK to cancel these changes and restore the database to its previous state.

1.Update

<img width="613" height="129" alt="image" src="https://github.com/user-attachments/assets/94e6492a-065b-425b-bd93-bd42d2fca646" />
<img width="946" height="473" alt="image" src="https://github.com/user-attachments/assets/3e992d26-ca30-4a93-8e06-3e989eb7b921" />
<img width="763" height="189" alt="image" src="https://github.com/user-attachments/assets/6881fbef-b3d1-4f3a-b722-9c0840748b81" />
Before the UPDATE, we observe the original values.After the UPDATE, the coordinates are modified.After ROLLBACK, the data returns to its original state.
<img width="961" height="161" alt="image" src="https://github.com/user-attachments/assets/3715edd9-244a-4886-89be-6c8eaeb31950" />
There is no line with the values we changed with Rollback because he not saved them

2.Delete

We first identify inactive volunteers ( volunteers that not worked 100 days ago) .
<img width="677" height="345" alt="image" src="https://github.com/user-attachments/assets/091daaf2-451e-480d-aff9-15d643491656" />
Then we delete them.
<img width="813" height="446" alt="image" src="https://github.com/user-attachments/assets/f5ffe4d6-f257-4b91-bccd-90949658d5ee" />
After deletion, they no longer appear in the query.
<img width="921" height="490" alt="image" src="https://github.com/user-attachments/assets/13fba19e-322e-4f15-a8b9-095f126334ba" />

After ROLLBACK, they reappear.
<img width="1005" height="607" alt="image" src="https://github.com/user-attachments/assets/93b90a91-f2ed-4802-a9b4-2f0d9516b77b" />

# Commit
Description: we perform an update and use COMMIT to permanently save the changes.
Before changes:

<img width="878" height="168" alt="image" src="https://github.com/user-attachments/assets/ed2e2ee8-1aca-479e-bd12-e4abdd1a1ff2" />

The UPDATE modifies the description of a category ('repairs instead of 'Repairs').

<img width="819" height="210" alt="image" src="https://github.com/user-attachments/assets/07b55ac6-ecfa-4740-b6a3-8d2b9cafe918" />
Running the query again will still show the updated value.
<img width="910" height="297" alt="image" src="https://github.com/user-attachments/assets/c4ec49d7-5e9a-4be8-961f-8b2d4edb9567" />

## Indexes
The goal of this section is to improve query performance by adding indexes on frequently used columns, and to analyze their impact using execution time comparisons.

Index 1: 
This index improves queries that: join treatment with volunteer ,search treatments of a specific volunteer
Before saving the index:
<img width="1010" height="611" alt="image" src="https://github.com/user-attachments/assets/73ca0904-4211-4498-b039-89ae8b914d08" />

<img width="602" height="137" alt="image" src="https://github.com/user-attachments/assets/a744256a-7361-47e4-b074-53f4a670bccf" />
Execution time is improved:
<img width="905" height="326" alt="image" src="https://github.com/user-attachments/assets/73ce6ca7-a044-432f-bfca-1828cd0ed4e5" />

Index 2:


The purpose of this index is to improve the performance of queries that filter volunteers based on:their availability (status), their geographic position (latitude, longitude)
Many queries involve:
selecting available volunteers,finding volunteers close to a specific location
before
<img width="908" height="683" alt="image" src="https://github.com/user-attachments/assets/a39216e8-c601-40b3-9b03-bc73b6273e17" />


```sql
CREATE INDEX idx_volunteer_status_location
ON volunteer(availability_status, latitude, longitude);

```
after
<img width="899" height="118" alt="image" src="https://github.com/user-attachments/assets/c736239c-f766-4184-a83a-ed95c7484adb" />
<img width="845" height="65" alt="image" src="https://github.com/user-attachments/assets/4ea4a334-f25e-4554-a8d6-2a31d25f1b90" />


Index 3:

The purpose of this index is to improve the performance of queries that filter treatments based on: a specific volunteer (volunteer_id),a time condition (date).
In our system, many queries involve analyzing volunteer activity over time, for example: finding treatments performed by a volunteer in a given period,identifying active or inactive volunteers,filtering treatments based on recent dates

<img width="548" height="145" alt="image" src="https://github.com/user-attachments/assets/1e7ab400-698b-4ac9-89cc-033312b47518" />
<img width="694" height="69" alt="image" src="https://github.com/user-attachments/assets/555666f2-2e6c-4181-b2ef-9a15b9776450" />

<img width="529" height="119" alt="image" src="https://github.com/user-attachments/assets/196a421d-fd05-4a00-91f6-2a0efb08595f" />

Query with index gives us the result in 1744 ms:
<img width="687" height="69" alt="image" src="https://github.com/user-attachments/assets/fde026bc-4637-4d39-8457-92c1ac8428ff" />

## Constraints

In this part, we added new constraints to the database using `ALTER TABLE`.
For each constraint, we describe the change and then show an example of an invalid insertion/update that violates the constraint.

---

## 1. Request priority level constraint

#### Change made

The `request` table now has a constraint that verifies that the priority level is between 1 and 5.

```sql
ALTER TABLE request
ADD CONSTRAINT chk_prioriry_level
CHECK (prioriry_level BETWEEN 1 AND 5);
```

```sql

INSERT INTO request (request_id,date,image,incident_description, prioriry_level,contactperson_id,category_id,status_id,
latitude,longitude)

VALUES (0,'2025-10-10',null,'not',9,0,1,1,10,10);
```

<img width="727" height="133" alt="image" src="https://github.com/user-attachments/assets/f80b60c9-6089-43e4-b0a1-e149bdf57e5c" />
This insertion fails because 9 is not between 1 and 5.

## 2. Location coordinates constraint
#### Change made

The location table now has a constraint that verifies that the coordinates are inside the valid range of Israel.
```sql
ALTER TABLE location
ADD CONSTRAINT chk_coordinates
CHECK (
    latitude BETWEEN 29.0 AND 34.0 
    AND 
    longitude BETWEEN 34.0 AND 36.0
);
```
Try insert latitude,longitude
```sql
INSERT INTO location (latitude,longitude,city,street,house_number)
VALUES (0,0,'haifa','moshe',55)
```
<img width="686" height="130" alt="image" src="https://github.com/user-attachments/assets/bc62bd8f-8fbd-4aa5-9690-6acd42779141" />

## 3. Treatment time order constraint
#### Change made

The treatment table now has a constraint that verifies that the completion time is not before the start time.
```sql
ALTER TABLE treatment
ADD CONSTRAINT chk_treatment_time_order
CHECK (
    completion_time IS NULL OR completion_time >= start_time
);
```
Invalid data test

```sql
INSERT INTO treatment(treatment_id,date,start_time,completion_time,feedback_notes,photo_after,delivery_id,volunteer_id,request_id)
VALUES (0,'2025-05-05','08:00','07:00','no',null,0,1,0)
```
This insertion fails because the completion time is earlier than the start time.
<img width="774" height="103" alt="image" src="https://github.com/user-attachments/assets/1cfeb77b-6377-4a93-b648-1d6eff585500" />

## Stage 3 Integration

---
#1  **Creating the Tables from the Backup**


To rebuild the received database, we read each `CREATE TABLE` command in the backup file.

Each `CREATE TABLE` command allowed us to identify one table, its columns, the data type of each column, and the basic constraints defined on it, such as `NOT NULL`, `CHECK`, and `UNIQUE`.

For example, from a `CREATE TABLE volunteer` command, we could understand that the database contains a `volunteer` table, with fields such as `volunteer_id`, `first_name`, `last_name`, `phone`, `email`, and other volunteer-related information.
 ```sql
CREATE TABLE public.volunteer (
    first_name character varying(20) NOT NULL,  --    <-- constraint 
    phone integer NOT NULL,
    birthday date NOT NULL,
    email text NOT NULL,
    city character varying(30) NOT NULL,
    volunteer_id integer NOT NULL,
    recruitment_date date NOT NULL,
    last_name character varying(20) NOT NULL,
    is_active character(1) NOT NULL,    --    <-- constraint 
    CONSTRAINT check_phone_positive CHECK ((phone > 0)),   
    CONSTRAINT volunteer_birthday_check CHECK ((birthday < CURRENT_DATE)),   --    <-- constraint 
    CONSTRAINT volunteer_check CHECK ((recruitment_date >= birthday)),
    CONSTRAINT volunteer_is_active_check CHECK ((is_active = ANY (ARRAY['Y'::bpchar, 'N'::bpchar]))),
    CONSTRAINT volunteer_recruitment_date_check CHECK ((recruitment_date <= CURRENT_DATE))
);
 ```


Then, by reading the `ALTER TABLE` commands, we identified the primary keys and foreign keys of each table. This allowed us to understand the relationships between the tables and reconstruct the database structure.
 ```sql
ALTER TABLE ONLY public.volunteer
    ADD CONSTRAINT volunteer_email_key UNIQUE (email);
 ```

 ```sql
ALTER TABLE ONLY public.volunteer
    ADD CONSTRAINT volunteer_phone_key UNIQUE (phone);
 ```

 ```sql
ALTER TABLE ONLY public.volunteer
    ADD CONSTRAINT volunteer_pkey PRIMARY KEY (volunteer_id);
 ```
In this way, the backup was used not only to create the tables in PostgreSQL, but also to analyze the structure of the received system.
( PK = UNIQUE+NOT NULL
 UNIQUE = can be null) 

### DSD:

<img width="1670" height="646" alt="image" src="https://github.com/user-attachments/assets/96a53e46-b243-4beb-8c93-86ef2910f9f3" />




---
### 2 . Algorithm : FROM DSD to ERD

1. Relation 1:N
  We first analyzed the foreign key references between the tables.

When a table contains a foreign key that points to another table, we used this dependency to identify the relationship between the two entities.

For example, the `availability` table contains the foreign key `volunteer_id`, which references the `volunteer` table.  
This means that each availability record belongs to one volunteer, while one volunteer can have several availability records.

Therefore, we created a `1:N` relationship between:

`volunteer` → `availability`
<img width="568" height="236" alt="oneToMany" src="https://github.com/user-attachments/assets/29479c31-b9be-4597-ac7f-3fc94d8367c7" />

To:
<img width="1164" height="307" alt="Capture d’écran 2026-05-17 154342" src="https://github.com/user-attachments/assets/399bd6e1-2963-4c40-9cb8-ee78ec8ef52a" />

2.  Relation N:M

For example, the `volunteer_skill` table contains two foreign keys: `volunteer_id`, which references `volunteer`, and `skill_id`, which references `skill`.

This means that one volunteer can have many skills, and one skill can belong to many volunteers.
<img width="915" height="269" alt="N-M" src="https://github.com/user-attachments/assets/63007b80-0cc3-4551-a01b-9096cc4821ab" />

Therefore, we created an `M:N` relationship between `volunteer` and `skill`.
<img width="774" height="117" alt="Capture d’écran 2026-05-17 155536" src="https://github.com/user-attachments/assets/7453b37c-8669-4fac-9fe2-5a70ab69b89b" />

3. Weak Entities
We identified weak entities by looking for tables with a composite primary key that includes a foreign key.  
For example, `Scheduled` depends on `training`, since its primary key includes `training_id`.
<img width="877" height="266" alt="Capture d’écran 2026-05-17 160117" src="https://github.com/user-attachments/assets/7f8b1afe-a1cd-4720-9a82-0f901aabcc02" />
So "scheduled" become an weak entity:
<img width="393" height="363" alt="Capture d’écran 2026-05-17 160139" src="https://github.com/user-attachments/assets/1d76b5ad-604e-43f9-ba96-2572398d6439" />


**ERD of the other group:**
<img width="1600" height="685" alt="erdgroupb" src="https://github.com/user-attachments/assets/e42a0454-24aa-496e-b6de-b2e172075efc" />

**ERD combined:**
<img width="1640" height="699" alt="image" src="https://github.com/user-attachments/assets/b02c1b52-7e37-424b-98d7-74634ac2448e" />

**DSD combined:**
<img width="1650" height="681" alt="image" src="https://github.com/user-attachments/assets/cbc3aa1e-5cb5-4997-92bb-87feaa651b7a" />


## Adjustments Made for the Integration

### POINT 1 -->  Volunteer Table



During the integration phase, we decided to keep `a_volunteer` as the final volunteer table in the integrated database.  
This decision was made because the volunteer entity already existed in our original system and was connected to the main entities of our project, such as requests and treatments.

### 1. Keeping `is_active` instead of `availability_status`

The table `a_volunteer` originally contained an `availability_status` field with values such as `Busy` and `Available`.  
In order to match the structure received from group B, we replaced this information with the field `is_active`, which stores values as `Y` or `N`.

The values were converted as follows:

- `Busy` became `Y`
- `Available` became `N`

After the conversion, the column `availability_status` was removed from `a_volunteer`.

### 2. Adding missing volunteer attributes

The table `b_volunteer` contained additional volunteer information that did not exist in our original `a_volunteer` table.  
Therefore, we added the following columns to `a_volunteer`:

```sql
ALTER TABLE public.a_volunteer
ADD COLUMN recruitment_date DATE;

ALTER TABLE public.a_volunteer
ADD COLUMN email VARCHAR(20);

ALTER TABLE public.a_volunteer
ADD COLUMN is_active VARCHAR(1);
````

The `is_active` column uses `Y` and `N`, following the representation used in the database of group B.

### 3. Defining `volunteer_id` as the main identifier

Since `a_volunteer` became the final volunteer table, its `volunteer_id` had to be used as the official identifier of volunteers in the integrated database.
For that reason, we added a primary key constraint on `volunteer_id`:

```sql
ALTER TABLE public.a_volunteer
ADD CONSTRAINT a_volunteer_pkey
PRIMARY KEY (volunteer_id);
```

This was necessary because other tables from group B, such as `b_volunteer_skill`, `b_volunteer_training`, and `b_availability`, needed to reference the final volunteer table.

### 4. Transferring volunteers from `b_volunteer` to `a_volunteer`

After checking that there were no duplicate `volunteer_id` values between the two tables, we copied the volunteers from `b_volunteer` into `a_volunteer`.

Only volunteers that did not already exist in `a_volunteer` were inserted:

```sql
INSERT INTO public.a_volunteer (
    volunteer_id,
    first_name,
    last_name,
    email,
    recruitment_date,
    is_active
)
SELECT
    bv.volunteer_id,
    bv.first_name,
    bv.last_name,
    bv.email,
    bv.recruitment_date,
    bv.is_active
FROM public.b_volunteer bv
WHERE NOT EXISTS (
    SELECT 1
    FROM public.a_volunteer av
    WHERE av.volunteer_id = bv.volunteer_id
);
```

This allowed us to merge the volunteer data from both systems into one final volunteer table.

### 5. Redirecting volunteer-related tables to `a_volunteer`

Some tables from group B originally referenced `b_volunteer`.
Since `a_volunteer` became the final volunteer table, we redirected these foreign keys to reference `a_volunteer(volunteer_id)` instead.

The affected tables were:

* `b_volunteer_skill`
* `b_volunteer_training`
* `b_availability`

For example, the constraint of `b_volunteer_skill` was changed from referencing `b_volunteer` to referencing `a_volunteer`:

```sql
ALTER TABLE public.b_volunteer_skill
DROP CONSTRAINT volunteer_skill_volunteer_id_fkey;

ALTER TABLE public.b_volunteer_skill
ADD CONSTRAINT fk_b_volunteer_skill_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);
```

The same logic was applied to the other volunteer-related tables.

### 6. Moving volunteer skills to `b_volunteer_skill`

In our original table, some volunteers had a `skill_type` field directly inside `a_volunteer`.
In the integrated database, skills are stored in a separate table, `b_skill`, and the connection between volunteers and skills is stored in `b_volunteer_skill`.


To migrate the data correctly, we matched each volunteer’s `skill_type` with the corresponding `skill_name` in `b_skill`.  
Then, we extracted the matching `skill_id` and inserted the pair `(volunteer_id, skill_id)` into `b_volunteer_skill`.

We also used a verification query before insertion to check which skills matched successfully, and another query to detect any `skill_type` values that did not exist in `b_skill`.

This allowed us to preserve the volunteers’ skill information while adapting it to the integrated database structure.
```sql
INSERT INTO b_volunteer_skill (volunteer_id, skill_id)
SELECT 
    v.volunteer_id,
    s.skill_id
FROM volunteer v
JOIN b_skill s
    ON LOWER(TRIM(v.skill_type)) = LOWER(TRIM(s.skill_name))
WHERE v.skill_type IS NOT NULL
  AND NOT EXISTS (
      SELECT 1
      FROM b_volunteer_skill vs
      WHERE vs.volunteer_id = v.volunteer_id
        AND vs.skill_id = s.skill_id
  );
```

Before merge: 88 rows 
After add our 500 volunteers --> 588  שורות 
<img width="341" height="564" alt="Capture d’écran 2026-05-25 154233" src="https://github.com/user-attachments/assets/3c6a1da3-c568-4a53-8d2d-2538d337518b" />
After this transfer, the column `skill_type` was removed from `a_volunteer`, because the relationship between volunteers and skills is now represented properly using the relationship table `b_volunteer_skill`.

### POINT 2 -->   `b_volunteer_training` table 

This table stores volunteer training information from group B.

### Changes made

- The foreign key on `volunteer_id` was redirected.
- It originally referenced `b_volunteer`.
- It now references `a_volunteer`.



Training records still need to exist, but they must reference the final volunteer table used in the integrated database.

---

### POINT 3 -->  `b_availability`  Table 

This table stores volunteer availability information.



- The foreign key on `volunteer_id` was redirected to `a_volunteer(volunteer_id)`.

Availability is still relevant after the integration, but it must be connected to the final volunteer entity, `a_volunteer`.

---
### POINT 4 -->  `b_type Table


The table `b_type` represented call types in group B.

The IDs were shifted:

```text
1 → 5
2 → 6
3 → 7
4 → 8
5 → 9
6 → 10


We also matched the other system's call types (b_type) into our categories (a_requestcategory):

Adding Missing Categories: We inserted three specific emergency types from their system (Flat Tire Assistance, Locked Vehicle, and Child Locked In Car) into our table using IDs 5, 6, and 7.

Category Alignment: This allowed us to successfully map every migrated call to a relevant category in our system without losing any context.
<img width="1526" height="336" alt="image" src="https://github.com/user-attachments/assets/e72fc2c9-200c-49b9-9380-73d0b92407c2" />

```
### POINT 5 -->   b_call to a_request Integration
The table b_call from the new system lacked many mandatory attributes that were required by our centralized a_request table. Because of this structural gap, we had to implement specific fallbacks and logical mappings during the migration:

Placeholder Family Account: We created a generic family profile (ID: 999999) to link all migrated calls, ensuring no data was lost due to missing family relationships.

New Request IDs: We generated unique request IDs starting at 20006 using ROW_NUMBER() to avoid any ID conflicts.

Smart Priority Levels: We scanned the call descriptions; if a text contained the word 'URGENT', it was automatically set to a high priority (5), otherwise it defaulted to a normal level (2).

Status & Category Mapping: We used CASE WHEN statements to translate and match the status strings (Closed, InProgress) and category IDs from their system into our active system codes.

Default Locations: Standard latitude and longitude coordinates were added to satisfy the required geographic fields.

INSERT INTO public.a_family (contactperson_id, contactperson_name, phone_number, number_of_members, special_features)
VALUES (999999, 'Clients Groupe B', '0500000000', null, null)
ON CONFLICT (contactperson_id) DO NOTHING;


INSERT INTO public.a_request (
    request_id, 
    date, 
    incident_description, 
    prioriry_level, 
    contactperson_id, 
    category_id, 
    status_id, 
    latitude,
    longitude
)
SELECT 
   
    20005 + ROW_NUMBER() OVER (ORDER BY bc.call_date, bc.phone) AS request_id,
    
    bc.call_date AS date,
    bc.description AS incident_description,
    
    CASE 
        WHEN bc.description LIKE '%URGENT%' THEN 5 
        ELSE 2 
    END AS prioriry_level,
    
    999999 AS contactperson_id, -- On utilise l'ID de notre famille générique créée juste au-dessus !
    
    CASE 
        WHEN bc.type_id = 5 THEN 5
        WHEN bc.type_id = 6 THEN 6
        WHEN bc.type_id = 7 THEN 1
        WHEN bc.type_id = 8 THEN 7
        WHEN bc.type_id = 9 THEN 1
        WHEN bc.type_id = 10 THEN 1
        ELSE 1
    END AS category_id,

    CASE 
        WHEN bc.status = 'Closed' THEN 3
        WHEN bc.status = 'InProgress' THEN 2
        WHEN bc.status = 'Cancelled' THEN 4
        ELSE 1 
    END AS status_id,
    
    31.255810 AS latitude,
    34.816400 AS longitude

FROM public.b_call bc;

COMMIT;


### POINT 6 --> Linking Skills to Categories
We structured the skills table (b_skill) by grouping individual skills into logical categories (b_category):

Structural Change: We added a category_id column to b_skill as a foreign key pointing to b_category.

Smart Classification: We used UPDATE commands with LIKE and IN filters to automatically classify every skill into its correct category (e.g., matching language skills to Category 1, vehicle maintenance to Category 2, and locksmithing to Category 3).


### POINT 7 --> Cleaning Duplicate Skills
We noticed that some skills from both groups overlapped and meant the exact same thing. To clean up the data, we filtered and merged them:

Merging Assignments: We redirected the duplicate volunteer skill links in b_volunteer_skill to the most precise skill ID (replacing 10 with 18, 22 with 16, and 8 with 12).

Primary Key Safety: Before updating, we used a DELETE query to clear any pairs that would cause a duplicate primary key error.

Removing Duplicates: Once all volunteer links were updated, we safely deleted the redundant skill IDs (10, 22, and 8) from the b_skill table.

DELETE FROM public.b_volunteer_skill 
WHERE skill_id = 10 
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 18);

UPDATE public.b_volunteer_skill 
SET skill_id = 18 
WHERE skill_id = 10;

DELETE FROM public.b_volunteer_skill 
WHERE skill_id = 22 
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 16);

UPDATE public.b_volunteer_skill 
SET skill_id = 16 
WHERE skill_id = 22;

DELETE FROM public.b_volunteer_skill 
WHERE skill_id = 8 
  AND volunteer_id IN (SELECT volunteer_id FROM public.b_volunteer_skill WHERE skill_id = 12);

UPDATE public.b_volunteer_skill 
SET skill_id = 12 
WHERE skill_id = 8;

DELETE FROM public.b_skill 
WHERE skill_id IN (10, 22, 8);



### POINT 8 --> Removing Redundant Tables
After successfully merging all the data, several tables from the other system became obsolete. We cleaned up the database by dropping them:

Direct Deletions: We safely dropped b_volunteer_call, b_call, b_skill_category, and b_type since their records were already fully integrated into our core tables.

DROP TABLE b_volunteer_call;
DROP TABLE b_call;
DROP TABLE b_skill_category;
DROP TABLE b_type;

Safely Removing b_volunteer: Before dropping the duplicate volunteer table, we rewired the training links in b_volunteer_training to point directly to our main a_volunteer table to maintain referential integrity. Once the links were updated, b_volunteer was successfully dropped.

BEGIN;
ALTER TABLE public.b_volunteer_training
DROP CONSTRAINT IF EXISTS fk_volunteer_training_volunteer;

ALTER TABLE public.b_volunteer_training
ADD CONSTRAINT fk_b_volunteer_training_a_volunteer
FOREIGN KEY (volunteer_id)
REFERENCES public.a_volunteer(volunteer_id);
COMMIT;

DROP TABLE public.b_volunteer;



## View from Department A 
This view, named v_my_department_requests, consolidates all operational information regarding emergency and assistance requests received by the organization. This view integrates 5 different tables using database relations (JOIN):

Requests (a_request): The core table from which the request ID, incident date, problem description, and priority level are extracted.

Request Categories (a_requestcategory): Used to display the explicit name of the incident type instead of a numeric ID.

Statuses (a_status): Used to display the current handling state of the request in plain text.

Locations (a_location): Allows mapping each request to its specific city based on geographic coordinates.

Families / Contact Persons (a_family): Allows fetching the direct phone number of the applicant so that dispatchers can establish immediate contact during critical emergencies.

<img width="1036" height="475" alt="image" src="https://github.com/user-attachments/assets/f59425a3-106e-4611-ae2f-0d539027dc70" />

<img width="1572" height="654" alt="image" src="https://github.com/user-attachments/assets/25cb8d45-32a5-4e63-847a-cf9771c6c02f" />


### Query 1: Critical Emergency Dispatch for the Month of April

This query is designed for dispatch managers to generate a targeted report of critical requests (priority level 4 or 5) that occurred exclusively during the month of April. The query displays essential operational fields such as the incident location, problem type, and the contact phone number, sorting them from newest to oldest. This query carries significant operational value as it allows tracking severe emergencies in April.

<img width="576" height="349" alt="image" src="https://github.com/user-attachments/assets/8cec5611-b7f6-45b9-8be8-5ca1a64eabf3" />

<img width="1094" height="450" alt="image" src="https://github.com/user-attachments/assets/3bbf1db5-2f60-4a7c-9d4e-58e58f37d3ec" />


### Query 2: Statistical Analysis of Requests by Day of the Week

This analytical query aims to identify call volume trends and weekly workloads. It groups the data by the day of the week (ordered from Monday to Sunday) and calculates for each day: the total volume of requests, the average priority level, and the specific count of critical emergencies (levels 4 and 5) out of that day's total (utilizing a conditional COUNT CASE WHEN). This information is vital for the organization to optimize volunteer shifting and standby schedules ahead of high-demand days.

<img width="1074" height="287" alt="image" src="https://github.com/user-attachments/assets/38ccdd79-9d87-4a77-9ba6-3badbfe0d782" />
<img width="897" height="332" alt="image" src="https://github.com/user-attachments/assets/dc889bf0-5b02-4a9b-9fc6-e721b1aca6df" />



## View from Department B  

The view v_received_department_skills links volunteers with their skills and categories. It combines 4 different tables using JOIN:
a_volunteer: Outlines the volunteer's full name and phone number.
b_volunteer_skill: Relational junction table linking volunteers to their skill IDs.
b_skill: Stores the explicit name of each technical capability.
b_catagory: Organizes individual skills into main groups (e.g., Technical, Language).  

<img width="856" height="367" alt="image" src="https://github.com/user-attachments/assets/40ecc33a-76a0-4edf-8930-22342e1772a5" />

<img width="1190" height="451" alt="image" src="https://github.com/user-attachments/assets/4d317184-da66-43fb-8a54-9b315cfed485" />


### Query 1: Contact List for Arabic-Speaking Volunteers  

Description: This query extracts the phone directory of volunteers who speak Arabic. It allows dispatchers to find immediate linguistic support during fieldwork.  

<img width="574" height="280" alt="image" src="https://github.com/user-attachments/assets/ad8acd83-7722-41b9-b7fb-a10f2f6b0bb8" />

<img width="985" height="303" alt="image" src="https://github.com/user-attachments/assets/2d26d537-0064-4f8c-88fc-22434a2b1604" />



### Query 2: Volunteer Versatility Ranking  

This query counts how many technical skills each volunteer possesses, sorted from highest to lowest. It helps management identify the most highly qualified and versatile team members.

<img width="612" height="200" alt="image" src="https://github.com/user-attachments/assets/cfeb83a1-7161-4c26-a75d-c75e2ed72e4b" />

<img width="553" height="346" alt="image" src="https://github.com/user-attachments/assets/5b8d0c70-c30d-4e62-b6ce-b3a9a906baa1" />
