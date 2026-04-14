# 📊 EDA-Tool: A Web-Based Automated Exploratory Data Analysis System

## 🧠 Abstract

Exploratory Data Analysis (EDA) is a fundamental step in data-driven research and machine learning pipelines. However, traditional EDA requires significant programming expertise and manual effort.
This project presents a **web-based automated EDA system** that enables users to upload datasets (CSV format) and instantly generate statistical summaries, visualizations, and analytical insights.

The system is designed using a modern lightweight architecture combining FastAPI, Jinja2 templating, and SQLite, providing a scalable and user-friendly platform for both academic and practical data analysis tasks.

---

## 🎯 Objectives

* To automate the EDA process for structured datasets
* To reduce dependency on manual coding for data analysis
* To provide real-time visualization and statistical summaries
* To build a scalable framework for future integration with machine learning models

---

## 🏗️ System Architecture

The system follows a modular architecture:

* **Presentation Layer:** HTML, Bootstrap, Jinja2
* **Application Layer:** FastAPI (RESTful APIs)
* **Data Processing Layer:** Pandas, NumPy
* **Persistence Layer:** SQLite

---

## ⚙️ Methodology

The system performs the following automated analytical steps:

### 1. Data Ingestion

* CSV file upload and validation
* Encoding handling and format checking

### 2. Data Profiling

* Dataset dimensions (rows, columns)
* Data types identification
* Summary statistics generation

### 3. Missing Value Analysis

* Detection of null values
* Percentage-based analysis
* Optional handling strategies (future work)

### 4. Univariate Analysis

* Distribution analysis for numerical features
* Frequency distribution for categorical features

### 5. Bivariate and Multivariate Analysis

* Correlation matrix computation
* Feature relationship visualization

### 6. Outlier Detection

* Statistical methods (IQR-based detection)
* Visualization via boxplots

### 7. Visualization

* Histogram, bar chart, boxplot
* Correlation heatmap

---

## 🛠️ Technologies Used

* **Backend:** FastAPI
* **Frontend:** HTML, Bootstrap, Jinja2
* **Database:** SQLite
* **Data Analysis:** Pandas, NumPy
* **Visualization:** Plotly / Matplotlib

---

## 📁 Project Structure

```id="2plgcb"
eda_tool/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── services/
│   │   ├── eda.py
│   │   ├── plots.py
│   │
│   ├── routers/
│   │   └── upload.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── upload.html
│   │   ├── dashboard.html
│   │
│   ├── static/
│
├── uploads/
├── reports/
├── eda.db
└── README.md
```

---

## ▶️ Installation & Execution

```id="v9y6rj"
git clone https://github.com/your-username/eda-tool.git
cd eda-tool

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Access the system at:

```
http://127.0.0.1:8000
```

---

## 📊 Experimental Workflow

```id="f1q5o9"
Dataset Upload → Data Profiling → Visualization → Insight Generation
```

---

## 🔬 Research Contributions

* Development of a **lightweight automated EDA framework**
* Integration of **web-based interactive analytics**
* Reduction of manual preprocessing effort
* Foundation for **AutoML and intelligent data pipelines**

---

## ⚖️ Limitations

* বর্তমানে শুধুমাত্র CSV format supported
* Large-scale dataset (millions of rows) handling সীমিত
* Automated insight generation এখনো rule-based

---

## 🔮 Future Work

* 🤖 AI-driven insight generation
* 📊 Integration with machine learning models (AutoML)
* 📄 Automated report generation (PDF/HTML)
* ☁️ Cloud-based deployment and scalability
* 🔐 Role-based access control (RBAC)

---

## 📚 Potential Research Extensions

This system can be extended toward:

* Intelligent Data Preprocessing Systems
* Automated Machine Learning Pipelines
* Real-Time Data Analytics Platforms
* Edge-based Data Processing Systems

---

## 📜 License

This project is licensed under the MIT License.

---

## ⭐ Acknowledgment

This work is inspired by modern data analysis tools and automated analytics frameworks, aiming to bridge the gap between research and practical implementation.

---
