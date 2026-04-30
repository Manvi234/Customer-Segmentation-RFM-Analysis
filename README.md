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

## 👥 Customer Segmentation Strategy (RFM Analysis)

Using a custom-built **RFM (Recency, Frequency, Monetary)** model, the customer base was segmented into five distinct categories to enable targeted marketing strategies and improve retention, engagement, and customer lifetime value.

### Segments Overview

| Segment | Customer Count | Description |
|---------|---------------|-------------|
| **At Risk** | 22,558 | Previously high-value customers who have become inactive and show churn risk |
| **Loyal Customers** | 19,307 | Frequent buyers with consistent spending behavior and strong brand affinity |
| **Hibernating** | 15,880 | Low engagement, low purchase frequency customers who have drifted away |
| **Champions** | 15,792 | Highest-value customers with strong loyalty, frequency, and spending patterns |
| **Others** | 22,558 | New or infrequent shoppers currently in early discovery/purchase stages |

---

### 📌 Strategic Business Actions

#### 🔴 At Risk Customers
- Deploy personalized **win-back campaigns**
- Offer limited-time discounts such as:
  - *"We Miss You"* promotions
  - cart recovery incentives
  - targeted coupon campaigns  

**Goal:** Prevent churn and reactivate historically valuable users.

---

#### 🟢 Champions
- Launch premium retention programs:
  - exclusive early product access
  - VIP customer support
  - tiered rewards & loyalty perks  

**Goal:** Maximize Customer Lifetime Value (LTV) and retention.

---

#### 🟡 Loyal Customers
- Introduce **referral programs** and advocacy incentives  
- Reward customer referrals with:
  - store credits
  - discounts
  - exclusive perks  

**Goal:** Turn loyal customers into acquisition channels.

---

#### ⚫ Hibernating Customers
- Run automated low-cost re-engagement flows:
  - reminder emails
  - product recommendations
  - abandoned interest campaigns  

**Goal:** Reactivate users efficiently without high CAC spend.

---

#### 🔵 Others
- Focus on onboarding and first-purchase conversion:
  - educational content
  - welcome offers
  - first-order discounts  

**Goal:** Move new/infrequent shoppers into the Loyal Customer segment.

---

### 🎯 Business Impact
This segmentation framework enables:
- smarter marketing budget allocation  
- improved retention strategy  
- reduced churn risk  
- stronger customer lifetime value optimization  
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
