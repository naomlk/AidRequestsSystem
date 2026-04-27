import random
from datetime import datetime, timedelta

NUM_ROWS = 20000
OUTPUT_FILE = "massive_data.sql"

def generate_data():
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- MASSIVE DATA GENERATION - CORRECT ORDER: REQ -> DEL -> TREAT\n")
        f.write("SET session_replication_role = 'replica';\n\n")
        
        for i in range(1, NUM_ROWS + 1):
            date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 850))).date()
            f_id = random.randint(200000000, 399999999) 
            cat_id = random.randint(1, 4)
            stat_id = random.randint(1, 4)
            priority = random.randint(1, 5)
            lat = round(random.uniform(31.0, 33.0), 6)
            lon = round(random.uniform(34.0, 36.0), 6)
            
            # 1. REQUEST
            sql_req = (f"INSERT INTO REQUEST (Request_id, date, image, incident_description, "
                       f"prioriry_level, ContactPerson_id, Category_id, status_id, latitude, longitude) "
                       f"VALUES ({i}, '{date}', 'req_{i}.jpg', 'Assistance needed #{i}', {priority}, "
                       f"{f_id}, {cat_id}, {stat_id}, {lat}, {lon});\n")
            f.write(sql_req)

            # 2.  DELIVERY (Optional)
            d_id = "NULL"
            if cat_id == 3: # Essential Logistics
                d_id = i
                items = random.choice(['Water Packs', 'Medical Oxygen', 'Vital Medicines', 'Food Basket'])
                qty = random.randint(1, 5)
                sql_del = (f"INSERT INTO DELIVERY (delivery_id, date, status, item_type, quantity, Request_id) "
                           f"VALUES ({d_id}, '{date}', 'Delivered', '{items}', {qty}, {i});\n")
                f.write(sql_del)

            # 3.TREATMENT 
            start_hour = random.randint(7, 19)
            start_min = random.randint(0, 59)
            duration = random.randint(30, 120)
            start_time_dt = datetime.strptime(f"{start_hour}:{start_min}", "%H:%M")
            end_time_dt = start_time_dt + timedelta(minutes=duration)
            v_id = random.randint(200000000, 399999999)
            
            sql_treat = (f"INSERT INTO TREATMENT (treatment_id, date, start_time, completion_time, "
                         f"feedback_notes, photo_after, delivery_id, volunteer_id, request_id) "
                         f"VALUES ({i}, '{date}', '{start_time_dt.strftime('%H:%M:%S')}', "
                         f"'{end_time_dt.strftime('%H:%M:%S')}', 'Mission #{i} completed', "
                         f"'after_{i}.jpg', {d_id}, {v_id}, {i});\n")
            f.write(sql_treat)

        f.write("\nSET session_replication_role = 'origin';\n")

    print(f"Success! Script updated ")

if __name__ == "__main__":
    generate_data()