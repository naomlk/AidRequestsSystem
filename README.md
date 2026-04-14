**Project Report: Family Aid Request Management System - Yedidim**

Submitters: Naomi Malka & Oshrit Peretz
System: Yedidim
Module: Family Assistance Unit

***Introduction***
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

User Interface (UI)
<img width="1918" height="874" alt="image" src="https://github.com/user-attachments/assets/56e186fa-1aa2-4d56-b0d1-a74ae6dec616" />
<img width="1919" height="865" alt="image" src="https://github.com/user-attachments/assets/75ed4896-9e63-49b0-95ff-03be5448e482" />
<img width="1913" height="874" alt="image" src="https://github.com/user-attachments/assets/60273847-0ea7-4c43-8cac-0be7eab27510" />
<img width="1919" height="870" alt="image" src="https://github.com/user-attachments/assets/78478b7f-0eb5-4c40-9b32-a343f18878a8" />
<img width="1919" height="831" alt="image" src="https://github.com/user-attachments/assets/cda3d205-c4e1-43c8-a01b-dc6044be96fe" />


ERD - Entity Relationship Diagram
<img width="1418" height="669" alt="image" src="https://github.com/user-attachments/assets/3ae6ce8d-b7cc-4da6-a6ee-0d385e563343" />

DSD - Data Structure Diagram
<img width="3744" height="1605" alt="DSD" src="https://github.com/user-attachments/assets/dc9c6669-e33e-496a-9459-e3bdfb694adb" />


Data Insertion Methods
We utilized three distinct methods to populate the database:

Manual INSERT Commands : Used for static reference tables such as STATUS and REQUESTCATEGORY. 
<img width="1381" height="418" alt="image" src="https://github.com/user-attachments/assets/5fafb2c5-7958-4ad9-b543-a5e82dd07ded" />


External Data Generation (Mockaroo): Used to generate 500 realistic records for the FAMILY, LOCATION, and VOLUNTEER tables.
<img width="485" height="146" alt="image" src="https://github.com/user-attachments/assets/1513bc0d-f9fe-4fa2-a800-e6398ea06741" />
<img width="1716" height="453" alt="image" src="https://github.com/user-attachments/assets/cc34d80c-33b6-4052-8e68-a204efb7d010" />



Automated Python Scripting (Method B): A custom Python script (generate_data.py) was developed to generate 20,000 records for both the REQUEST and TREATMENT tables. Also for DELIVERY table but not as many lines.  This method ensured logical consistency between foreign keys across the massive dataset.
<img width="1426" height="962" alt="image" src="https://github.com/user-attachments/assets/564c08ea-63c5-46a8-808a-187e288517bf" />
<img width="1841" height="796" alt="image" src="https://github.com/user-attachments/assets/1918378e-4bd7-49a9-8ccb-fb27ea3805c4" />


Backup 
<img width="1301" height="73" alt="image" src="https://github.com/user-attachments/assets/4691529b-8f7e-4bcd-af61-8f93e031b298" />
<img width="1104" height="33" alt="image" src="https://github.com/user-attachments/assets/857ad52c-5f94-4070-b5c7-93e3e3f8f625" />
<img width="388" height="298" alt="image" src="https://github.com/user-attachments/assets/8e07045a-cdaf-45f2-9e49-bfbfcf836d8f" />


   

