
from pymongo import MongoClient

# MongoDB Atlas Connection
MONGO_URI = "mongodb+srv://agri_user:Prakruthi@cluster0.jejwokl.mongodb.net/?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)

    # Test connection
    client.admin.command("ping")
    print("MongoDB Connected Successfully!")

    # Database and Collection
    db = client["agriculture_db"]
    readings = db["farm_readings"]

    print("Database:", db.name)
    print("Collection:", readings.name)

    # Agricultural Dataset
    agriculture_data = [
        {"farm_id": "F01", "crop": "Rice", "location": "Bangalore",
         "soil_moisture": 37, "temperature": 28, "rainfall_mm": 12,
         "yield_tonnes": 4.5},

        {"farm_id": "F02", "crop": "Ragi", "location": "Tumkur",
         "soil_moisture": 24, "temperature": 30, "rainfall_mm": 8,
         "yield_tonnes": 2.0},

        {"farm_id": "F03", "crop": "Maize", "location": "Mysore",
         "soil_moisture": 40, "temperature": 29, "rainfall_mm": 15,
         "yield_tonnes": 3.6},

        {"farm_id": "F04", "crop": "Rice", "location": "Mandya",
         "soil_moisture": 38, "temperature": 27, "rainfall_mm": 20,
         "yield_tonnes": 4.5},

        {"farm_id": "F05", "crop": "Ragi", "location": "Hassan",
         "soil_moisture": 19, "temperature": 34, "rainfall_mm": 5,
         "yield_tonnes": 1.9}
    ]

    valid_data = []
    invalid_data = []

    for record in agriculture_data:

        if not isinstance(record["farm_id"], str) or not record["farm_id"].strip():
            invalid_data.append(record)
            continue

        if not isinstance(record["crop"], str) or not record["crop"].strip():
            invalid_data.append(record)
            continue

        if not isinstance(record["location"], str) or not record["location"].strip():
            invalid_data.append(record)
            continue

        if (not isinstance(record["soil_moisture"], (int, float))
                or isinstance(record["soil_moisture"], bool)
                or not 0 <= record["soil_moisture"] <= 100):
            invalid_data.append(record)
            continue

        if (not isinstance(record["temperature"], (int, float))
                or isinstance(record["temperature"], bool)):
            invalid_data.append(record)
            continue

        if (not isinstance(record["rainfall_mm"], (int, float))
                or isinstance(record["rainfall_mm"], bool)
                or record["rainfall_mm"] < 0):
            invalid_data.append(record)
            continue

        if (not isinstance(record["yield_tonnes"], (int, float))
                or isinstance(record["yield_tonnes"], bool)
                or record["yield_tonnes"] < 0):
            invalid_data.append(record)
            continue

        valid_data.append(record)
            # Display Validation Results
    print("\n========== DATA VALIDATION ==========")
    print("Total Records:", len(agriculture_data))
    print("Valid Records:", len(valid_data))
    print("Invalid Records:", len(invalid_data))

    # Insert missing records without duplicating existing records
    for record in valid_data:
        readings.update_one(
            {"farm_id": record["farm_id"]},
            {"$setOnInsert": record},
            upsert=True
        )

    print("\nAgricultural Data Insertion Completed!")
    print("Total Records in Database:", readings.count_documents({}))
    # STEP 8: AGRICULTURAL DATA ANALYSIS

    print("\n========== AGRICULTURAL DATA ANALYSIS ==========")

    # 1. Overall Average Statistics
    overall_stats = list(readings.aggregate([
        {
            "$group": {
                "_id": None,
                "average_moisture": {"$avg": "$soil_moisture"},
                "average_temperature": {"$avg": "$temperature"},
                "average_yield": {"$avg": "$yield_tonnes"}
            }
        }
    ]))

    print("\n1. OVERALL AVERAGE STATISTICS")

    for data in overall_stats:
        print("Average Soil Moisture:",
              round(data["average_moisture"], 2), "%")
        print("Average Temperature:",
              round(data["average_temperature"], 2), "°C")
        print("Average Crop Yield:",
              round(data["average_yield"], 2), "tonnes")

    # 2. Crop-wise Average Yield
    crop_stats = readings.aggregate([
        {
            "$group": {
                "_id": "$crop",
                "average_yield": {"$avg": "$yield_tonnes"},
                "total_farms": {"$sum": 1}
            }
        }
    ])

    print("\n2. CROP-WISE AVERAGE YIELD")

    for crop in crop_stats:
        print(
            crop["_id"],
            "- Average Yield:",
            round(crop["average_yield"], 2),
            "tonnes, Farms:",
            crop["total_farms"]
        )

    # 3. Low Soil Moisture Alerts
    low_moisture = readings.find(
        {"soil_moisture": {"$lt": 25}}
    )

    print("\n3. LOW SOIL MOISTURE ALERTS")

    for farm in low_moisture:
        print(
            "Farm:", farm["farm_id"],
            "| Crop:", farm["crop"],
            "| Soil Moisture:", farm["soil_moisture"], "%"
        )
    # STEP 9: DATA FILTERING AND SEARCH

    print("\n========== DATA FILTERING AND SEARCH ==========")

    # 1. Search by Farm ID
    print("\n1. SEARCH BY FARM ID")

    farm = readings.find_one({"farm_id": "F01"})

    if farm:
        print("Farm ID:", farm["farm_id"])
        print("Crop:", farm["crop"])
        print("Location:", farm["location"])
        print("Soil Moisture:", farm["soil_moisture"], "%")
    else:
        print("Farm not found!")

    # 2. Search by Crop Name
    print("\n2. SEARCH BY CROP NAME")

    crop_records = readings.find({"crop": "Rice"})

    for record in crop_records:
        print(
            "Farm:", record["farm_id"],
            "| Crop:", record["crop"],
            "| Yield:", record["yield_tonnes"], "tonnes"
        )

    # 3. Search by Location
    print("\n3. SEARCH BY LOCATION")

    location_records = readings.find({"location": "Tumkur"})

    for record in location_records:
        print(
            "Farm:", record["farm_id"],
            "| Location:", record["location"],
            "| Crop:", record["crop"]
        )
            # STEP 11: DISPLAY ALL AGRICULTURAL RECORDS

    print("\n========== ALL AGRICULTURAL RECORDS ==========")

    all_records = readings.find()

    print("{:<10} {:<10} {:<15} {:<15} {:<12}".format(
        "Farm ID", "Crop", "Location", "Moisture", "Temperature"
    ))

    print("-" * 65)

    for record in all_records:
        print("{:<10} {:<10} {:<15} {:<15} {:<12}".format(
            record["farm_id"],
            record["crop"],
            record["location"],
            str(record["soil_moisture"]) + "%",
            str(record["temperature"]) + "°C"
        ))
                # STEP 12: USER INPUT-BASED UPDATE

    print("\n========== UPDATE AGRICULTURAL RECORD ==========")

    farm_id = input("Enter Farm ID to update: ")
    new_moisture = float(input("Enter new soil moisture (%): "))

    if 0 <= new_moisture <= 100:

        update_result = readings.update_one(
            {"farm_id": farm_id},
            {"$set": {"soil_moisture": new_moisture}}
        )

        if update_result.matched_count > 0:
            print("Farm record updated successfully!")
            print("Modified Records:", update_result.modified_count)
        else:
            print("Farm ID not found.")

    else:
        print("Invalid soil moisture. Enter a value between 0 and 100.")
                # STEP 13: USER INPUT-BASED DELETE

    print("\n========== DELETE AGRICULTURAL RECORD ==========")

    farm_id_to_delete = input("Enter Farm ID to delete: ")

    confirm = input("Are you sure you want to delete this record? (yes/no): ")

    if confirm.lower() == "yes":

        delete_result = readings.delete_one(
            {"farm_id": farm_id_to_delete}
        )

        if delete_result.deleted_count > 0:
            print("Farm record deleted successfully!")
        else:
            print("Farm ID not found.")

    else:
        print("Delete operation cancelled.")

            # STEP 14: VERIFY UPDATE AND DELETE OPERATIONS

    print("\n========== VERIFY DATABASE CHANGES ==========")

    updated_record = readings.find_one({"farm_id": "F02"})

    if updated_record:
        print("F02 Soil Moisture:", updated_record["soil_moisture"], "%")

    deleted_record = readings.find_one({"farm_id": "F05"})

    if deleted_record is None:
        print("F05 record successfully deleted.")
    else:
        print("F05 record still exists.")
            # STEP 15: FINAL DATABASE SUMMARY

    print("\n========== FINAL DATABASE SUMMARY ==========")

    total_records = readings.count_documents({})

    print("Database Name:", db.name)
    print("Collection Name:", readings.name)
    print("Total Remaining Records:", total_records)

    print("\nProject Execution Completed Successfully!")
    client.close()

except Exception as e:
    print("Error:", e)