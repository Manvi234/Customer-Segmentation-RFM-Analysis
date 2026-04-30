# 📌 Customer Segmentation & RFM Analysis

## 📖 Project Overview
This project transforms over **100,000 records** from the Olist Brazilian E-Commerce Dataset into a strategic decision-making tool. By architecting a full-stack data pipeline; moving from raw SQL relational data to high-fidelity Tableau visualizations and a deployed Streamlit application, this suite provides a **360-degree view of marketplace health and customer behavior**.

---

## 🔗 Live Application
**[🚀 Live Dashboard → customer-segmentation-rfm-analysis.streamlit.app](https://customer-segmentation-rfm-analysis.streamlit.app)**

---

## 🛠️ Tech Stack

- **Database & Modeling:** SQL (SQLite) for complex joins, data cleaning, and feature engineering  
- **Programming:** Python (Pandas, NumPy) for RFM scoring, monetary binning, and preprocessing  
- **Business Intelligence:** Tableau Desktop for interactive dashboards and geographic mapping  
- **Deployment:** Streamlit for hosting the stakeholder-facing analytics portal  

---

## 📊 Key Analytics Modules

### 1. Executive Revenue Dashboard
This dashboard provides high-level business health metrics designed for executive stakeholders:

- **Geographic Distribution:** Revenue hubs across Brazil, highlighting the Southeast (SP, RJ, MG)  
- **Sales Momentum:** Monthly revenue trends with seasonal peaks (notably Black Friday - Q4)  
- **Payment Dynamics:** Payment methods (Boleto, Credit Card, Voucher) vs Average Order Value (AOV)  
- **Product Performance:** Top 10 product categories by average ticket size  

---

### 2. Customer Segmentation (RFM Analysis)
An advanced marketing analytics model categorizing customers based on:

- **Recency**
- **Frequency**
- **Monetary Value**

#### Segments:
- **Champions:** Loyal, high-spending customers  
- **At Risk:** Previously high-value but inactive customers  
- **Hibernating:** Low engagement, low frequency customers  

#### Strategic Actions:
- Loyalty rewards for Champions  
- Targeted win-back campaigns for At-Risk users  
- Cost-efficient re-engagement for Hibernating users  

---

## 🚀 Installation & Local Deployment

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/customer-segmentation-rfm-analysis.git
cd customer-segmentation-rfm-analysis
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```

---

## 📁 Project Structure
```
├── app.py                # Main Streamlit application
├── requirements.txt      # Python dependencies
├── dashboards/           # Tableau dashboard exports
│   ├── executive.twb
│   └── rfm_analysis.twb
├── data/                 # Cleaned datasets (CSV)
└── notebooks/            # SQL queries and EDA notebooks
```

---

## 🎓 Author
**Manvi Vijay Gawande**  
Data Science Professional | Master's Student at Indiana University Bloomington  
Specializing in NLP, Generative AI, and Predictive Analytics  

---

## 📜 License
This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.
