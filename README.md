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

Version 1 (JOIN) is much more efficient than Version 2 (Subquery).
Speed: Version 1 processes all data in one single operation, while Version 2 repeats the search 20,000 times (once for every row).
Performance: PostgreSQL is optimized to handle JOINs much faster, making it the professional choice for projects with Massive Data. 

### 2. Critical Pending Requests (Priority 4 & 5) 
Description: A vital operational query that lists all high-priority emergency requests that haven't been handled yet.

<img width="1146" height="256" alt="image" src="https://github.com/user-attachments/assets/ab5f3ced-ddeb-4e8a-b3b9-815f9b175b61" />
<img width="1170" height="276" alt="image" src="https://github.com/user-attachments/assets/0c8eb688-f1b3-4f97-a20a-88d6d5d28c47" />
<img width="564" height="269" alt="image" src="https://github.com/user-attachments/assets/9bd64db9-8fcf-42ba-8bd4-a612e618a812" />

Version 1 (JOIN) is generally more efficient than Version 2.
Logic: Version 1 connects the two tables directly. Version 2 performs a "search within a search," which adds an extra step for the database engine.
Execution: PostgreSQL is highly optimized for JOINs. It can find the "Pending" status and filter the requests simultaneously, making it faster for large amounts of data.
Readability: Version 1 is the standard way to write relational queries. Version 2 is more rigid and can fail if there are ever two statuses with the same name. 




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

Version 1 (WHERE) is much more efficient than Version 2 (EXCEPT).
Simplicity: Version 1 performs a single, direct check on one column. Version 2 forces the database to run two separate queries and then compare the results to find differences.
Resources: Version 1 is very fast and uses minimal memory. Version 2 is much heavier because it has to sort and "subtract" one list from another, which is unnecessary work for this task.
Best Practice: Using a simple filter (WHERE) is the standard way to retrieve data based on a condition. EXCEPT is usually reserved for more complex comparisons between different tables. 


### 5. Top Performing Volunteers (Above Average Activity) 
Description: An analytical query using a subquery to find volunteers whose number of completed missions is higher than the general average.

<img width="1165" height="257" alt="image" src="https://github.com/user-attachments/assets/34378d1b-cf8b-4f22-8240-9e5535e59a19" />
<img width="658" height="258" alt="image" src="https://github.com/user-attachments/assets/f755995b-8202-4b01-9660-de0ac8c37ab8" />



### 6. Monthly Requests Summary 
Description: Provides a high-level overview of the workload per month and year, allowing the organization to see seasonal trends in aid requests.

<img width="1117" height="285" alt="image" src="https://github.com/user-attachments/assets/bcb74688-2990-43ba-ae12-ea2468e3ecc8" />
<img width="476" height="268" alt="image" src="https://github.com/user-attachments/assets/0eb94255-fab7-4ebd-84ec-3d63d8c325f3" />



### 7. Geographic Distribution by City 
Description: This query analyzes the distribution of aid requests across different cities. By joining the LOCATION, REQUEST, and REQUESTCATEGORY tables, it displays the volume of requests for specific types of aid in each urban area.

<img width="1048" height="274" alt="image" src="https://github.com/user-attachments/assets/3322b86d-3b74-4bfa-93eb-5feb56ad7483" />
<img width="718" height="262" alt="image" src="https://github.com/user-attachments/assets/5fc36b03-bfef-4b31-983b-e725ffabfa45" />


### 8. Top Volunteers by Request Category 
Description: An advanced query using a CTE (Common Table Expression) to identify the "lead volunteer" for each specific category (e.g., the person who did the most plumbing vs. the most logistics).

<img width="974" height="593" alt="image" src="https://github.com/user-attachments/assets/dfe49e9b-61f5-4b4d-8466-658f40f0fe2a" />
<img width="700" height="269" alt="image" src="https://github.com/user-attachments/assets/33cde85a-3e65-44b1-b206-6cb1177a45a9" />


## Delete queries 

### 1. Removing Inactive Volunteers (No Activity for 1 Year)
Description: Identifies and removes volunteers with no recorded activity in the last 12 months to ensure a high-quality, active database. 

<img width="1566" height="306" alt="image" src="https://github.com/user-attachments/assets/9f40ab31-fed0-4790-9532-afae6e0de486" />
<img width="1220" height="393" alt="image" src="https://github.com/user-attachments/assets/82b4624a-0c66-4e54-b8f2-e90848ec4036" />
<img width="1562" height="295" alt="image" src="https://github.com/user-attachments/assets/5a5419d6-4117-4612-98e9-25ce75d44df6" />



