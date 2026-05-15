#  afaire attention


from pathlib import Path

tablesGroupB = [
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

tablesGroupA=["volunteer","treatment","request","family","delivery","status","requestcategory","location"]

input_file = Path("StageB/backup_final_stage_B.sql")
output_file = Path("backup_groupA_clean.sql")

sql = input_file.read_text(encoding="utf-16")


#REMPLACER TTES LES TABLES table->b_table  d

for table in tablesGroupA:   #changer ttes les tables
    sql = sql.replace(f"{table}", f"a_{table}")
# mais attention ca m efait des erreur car suposons qu ejai une colonne qui sapple delivery_id alors elle deviendra a_delivery_id
# et on ne doit pas touche aux colonnes des tables donc il faut ecrire el scritp au cas par acs en focntion
# de la maniere dont le backuop ets ecrit
# éviter de recréer public si ta base l’a déjà
sql = sql.replace("CREATE SCHEMA public;", "-- CREATE SCHEMA public;")    # pas compris pourquoi et cest quoi
sql = sql.replace("ALTER SCHEMA public OWNER TO pg_database_owner;", "-- ALTER SCHEMA public OWNER TO pg_database_owner;")

output_file.write_text(sql, encoding="utf-8")   # ici il faut changer en focntion de la version du backup file

print("Backup modifié créé :", output_file)