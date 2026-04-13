import random
from datetime import datetime, timedelta

NUM_ROWS = 20000
OUTPUT_FILE = "massive_data.sql"

def generate_data():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- MASSIVE DATA GENERATION - REALISTIC VALUES\n\n")
        
        for i in range(1, NUM_ROWS + 1):
            date = (datetime(2026, 1, 1) + timedelta(days=random.randint(0, 100))).date()
            f_id = random.randint(1, 500)
            cat_id = random.randint(1, 4)
            stat_id = random.randint(1, 4)
            priority = random.randint(1, 5)
            lat = round(random.uniform(31.0, 33.0), 6)
            lon = round(random.uniform(34.0, 36.0), 6)
            
            # 1. REQUEST INSERT
            sql_req = (f"INSERT INTO REQUEST (Request_id, date, image, incident_description, "
                       f"prioriry_level, ContactPerson_id, Category_id, treatment_id, status_id, latitude, longitude) "
                       f"VALUES ({i}, '{date}', 'req_{i}.jpg', 'Assistance needed #{i}', {priority}, "
                       f"{f_id}, {cat_id}, {i}, {stat_id}, {lat}, {lon});\n")
            f.write(sql_req)

            # 2. RANDOM TIMES
            start_hour = random.randint(7, 19)
            start_min = random.randint(0, 59)
            duration = random.randint(30, 120) # Intervention entre 30min et 2h
            
            start_time = datetime.strptime(f"{start_hour}:{start_min}", "%H:%M")
            end_time = start_time + timedelta(minutes=duration)
            
            # 3. LOGIC FOR DELIVERY_ID
            # On ne met un delivery_id que si c'est la catégorie 3 (Essential Logistics)
            # On suppose que delivery_id correspond au Request_id pour la cohérence
            d_id = i if cat_id == 3 else "NULL"
            
            v_id = random.randint(1, 500)
            
            # 4. TREATMENT INSERT
            sql_treat = (f"INSERT INTO TREATMENT (treatment_id, date, start_time, completion_time, "
                         f"feedback_notes, photo_after, delivery_id, volunteer_id) "
                         f"VALUES ({i}, '{date}', '{start_time.strftime('%H:%M:%S')}', "
                         f"'{end_time.strftime('%H:%M:%S')}', 'Mission #{i} completed successfully', "
                         f"'after_{i}.jpg', {d_id}, {v_id});\n")
            f.write(sql_treat)

    print(f"Success! {OUTPUT_FILE} created with varied times and smart delivery IDs.")

if __name__ == "__main__":
    generate_data()