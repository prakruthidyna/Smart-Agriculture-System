# 🌱 Smart Agriculture System

## 📌 Project Overview
The Smart Agriculture System is a Python-based project that uses MongoDB to manage agricultural data efficiently. It focuses on agricultural data validation and storage, helping organize farm-related readings in a structured database.

## 🎯 Objectives
- Manage agricultural data efficiently.
- Validate incoming agricultural records.
- Identify valid and invalid records.
- Store validated data in MongoDB.
- Maintain structured agricultural information for further analysis.

## 🛠️ Technologies Used
- **Programming Language:** Python
- **Database:** MongoDB
- **Library:** PyMongo
- **Development Environment:** Visual Studio Code

## 📂 Project Structure

```text
Smart-Agriculture-System/
│
├── smart_agriculture.py
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/prakruthidyna/Smart-Agriculture-System.git
```

### 2. Navigate to Project Directory

```bash
cd Smart-Agriculture-System
```

### 3. Install Required Library

```bash
pip install pymongo
```

### 4. Configure MongoDB

Make sure MongoDB is running and configure the database connection in the Python script.

Database Name: `agriculture_db`

Collection Name: `farm_readings`

### 5. Run the Project

```bash
python smart_agriculture.py
```

## 📊 Sample Execution Output

```text
MongoDB Connected Successfully!

Database: agriculture_db
Collection: farm_readings

========== DATA VALIDATION ==========

Total Records: 5
Valid Records: 5
Invalid Records: 0

Agricultural Data Insertion Completed!
```

## 🚀 Key Features
- MongoDB database connectivity.
- Agricultural data validation.
- Record classification into valid and invalid data.
- Automated insertion of agricultural records.
- Structured database management.

## 🔮 Future Enhancements
- Real-time agricultural sensor data collection.
- Weather monitoring and prediction.
- Soil moisture analysis.
- Crop recommendation system.
- Interactive dashboard for agricultural data visualization.

## 👩‍💻 Author

**Prakruthi BR**

GitHub: https://github.com/prakruthidyna

---

⭐ If you find this project interesting, feel free to explore the repository!