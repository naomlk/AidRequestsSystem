from pathlib import Path

tables = [
    "availability",
    "call",
    "catagory",
    "scheduled",
    "skill",
    "skill_category",
    "training",
    "type",
    "volunteer",
    "volunteer_call",
    "volunteer_skill",
    "volunteer_training"
]

input_file = Path("backup_groupB.sql")
output_file = Path("backup_groupB_clean.sql")

sql = input_file.read_text(encoding="utf-8")

for table in tables:   #changer ttes les tables
    sql = sql.replace(f"public.{table}", f"public.b_{table}")

# éviter de recréer public si ta base l’a déjà
sql = sql.replace("CREATE SCHEMA public;", "-- CREATE SCHEMA public;")    # pas compris pourquoi et cest quoi
sql = sql.replace("ALTER SCHEMA public OWNER TO pg_database_owner;", "-- ALTER SCHEMA public OWNER TO pg_database_owner;")

output_file.write_text(sql, encoding="utf-8")

print("Backup modifié créé :", output_file)