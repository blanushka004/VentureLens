# 🚀 VentureLens

## 🌐 Live Demo

🚀 **VentureLens Live App:**  
https://venturelens-ndwamgacaumbbxxlwtn99m.streamlit.app/

💻 **GitHub Repository:**  
https://github.com/blanushka004/VentureLens

### Startup Ecosystem Intelligence & Decision Support Platform

VentureLens is an interactive analytics and decision-support platform for exploring the Indian startup ecosystem.

It combines **PostgreSQL, ETL pipelines, multidimensional analytics, OLAP operations, funding forecasting, startup evaluation, investor intelligence, and a natural-language analytics assistant** in a Streamlit application.

Unlike a traditional dashboard that only displays historical charts, VentureLens allows users to explore ecosystem data, compare startups and industries, analyze investors, forecast funding trends, and evaluate their own startup ideas.

---

## 🎯 Problem Statement

Startup ecosystem data is often fragmented across funding reports, investor databases, industry reports, and individual company records.

Entrepreneurs and analysts may want to answer questions such as:

- Which industries attract the most funding?
- Which startup hubs are growing?
- Who are the most active investors?
- Which startups have the strongest funding momentum?
- How is startup funding changing over time?
- What could future funding activity look like?
- How promising is a new startup idea based on its characteristics?

VentureLens brings these analyses into a single interactive platform.

---

## ✨ Key Features

### 📊 Executive Intelligence

Provides a high-level view of the startup ecosystem including:

- Total startups
- Total funding
- Funding rounds
- Active investors
- Leading industries
- Leading startup cities
- Funding trends

---

### 🏢 Startup Ecosystem Analysis

Explore startup activity across:

- Industries
- Locations
- Funding history
- Funding momentum
- Recently funded startups
- Most active startups

---

### 💰 Funding Intelligence

Analyze:

- Yearly funding trends
- Monthly and quarterly funding
- Funding-stage distribution
- Average funding size
- Largest funding rounds
- Year-over-year growth

---

### 🧠 Industry Intelligence

Compare industries using:

- Total funding
- Startup count
- Funding rounds
- Market share
- Historical funding trends
- Industry growth

---

### 🏦 Investor Intelligence

Explore investor behavior including:

- Most active investors
- Investor portfolios
- Industry preferences
- Geographic reach
- Investment activity by year
- Diversified investors
- Co-investment relationships

---

### 🌍 Geographic Intelligence

Analyze startup hubs using:

- Startup concentration
- Funding concentration
- Industry distribution
- Investor activity
- City-level funding growth
- Average startup funding

---

### 🔎 Startup Explorer

Explore individual startups and compare their:

- Funding history
- Industry
- Location
- Funding rounds
- Funding momentum
- Relative ecosystem position

---

## 🚀 Startup Evaluation Engine

One of VentureLens' core decision-support features allows users to evaluate their own startup idea.

Users provide information such as:

- Industry
- City
- Startup stage
- Team size
- Founder experience
- Revenue
- User traction
- Funding requirement
- Market size
- Competition level
- Business model

VentureLens then produces an analytical assessment containing:

- **Venture Potential Score**
- **Success Potential Estimate**
- **Funding Readiness**
- **Risk Assessment**
- **Strengths**
- **Weaknesses**
- **Recommended actions**
- **Potential investor matches**

The evaluation combines user-provided startup characteristics with signals derived from the VentureLens startup ecosystem dataset.

> The score is intended as a decision-support estimate and not a guarantee of startup success.

---

## 🤖 VentureLens Intelligence Assistant

VentureLens includes a natural-language analytics interface that routes user questions to the appropriate analytics or forecasting functionality.

Example questions:

```text
Which industries received the highest funding?

Who are the most active investors?

Which startups raised the most funding?

What is the funding outlook for the next three years?

Which sectors currently dominate the ecosystem?
```

The assistant queries the VentureLens analytics layer instead of returning hard-coded ecosystem statistics.

---

## 🔮 Funding Forecasting

VentureLens includes a baseline machine-learning forecasting module using historical yearly startup funding.

The forecasting engine:

1. Aggregates historical funding by year
2. Prepares time-series features
3. Trains a Linear Regression baseline model
4. Generates future funding estimates
5. Calculates projected change and historical trend indicators

The forecast is designed as a **baseline analytical projection**, not a guaranteed financial prediction.

---

## 🧊 OLAP Analytics

VentureLens demonstrates multidimensional analytical operations commonly used in business intelligence systems.

Supported operations include:

- **Roll-up**
- **Drill-down**
- **Slice**
- **Dice**
- **Pivot**

Analysis can be performed across dimensions such as:

```text
Year
Month
City
Industry
Startup
Funding Stage
```

---

## 📄 Reporting

VentureLens includes a reporting layer that combines information from:

- Executive analytics
- Funding intelligence
- Startup intelligence
- Industry analytics
- Investor analytics
- Geographic analytics
- Forecasting
- Automated insights

Reports can be generated from the analyzed ecosystem data for further review and presentation.

---

## 🏗️ System Architecture

```text
Indian Startup Funding Dataset
            │
            ▼
      ETL Pipeline
 Extract → Transform → Load
            │
            ▼
       PostgreSQL
            │
     ┌──────┴───────┐
     │              │
 Analytics        OLAP
     │              │
     └──────┬───────┘
            │
            ▼
   Forecasting Engine
            │
            ▼
    Intelligence Layer
      ├─ Insights
      ├─ Venture Agent
      ├─ Startup Evaluator
      ├─ Investor Matcher
      └─ Recommendation Engine
            │
            ▼
      Streamlit UI
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| Database | PostgreSQL |
| ORM / Database Access | SQLAlchemy |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Machine Learning | Scikit-learn |
| Analytics | SQL + Python |
| Forecasting | Linear Regression |
| Data Engineering | ETL Pipeline |
| Version Control | Git & GitHub |

---

## 📁 Project Structure

```text
VentureLens/
│
├── app.py
├── requirements.txt
│
├── data/
│   └── raw/
│
├── database/
│   ├── connection.py
│   ├── models.py
│   └── init_db.py
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── analytics/
│   ├── overview.py
│   ├── startup_analysis.py
│   ├── funding_analysis.py
│   ├── industry_analysis.py
│   ├── investor_analysis.py
│   ├── geographic_analysis.py
│   └── olap_queries.py
│
├── forecasting/
│   └── funding_generator.py
│
├── ai/
│   ├── insights.py
│   ├── venture_agent.py
│   ├── startup_evaluator.py
│   ├── startup_scoring.py
│   ├── investor_matcher.py
│   └── recommendation_engine.py
│
├── reports/
│   └── report_generator.py
│
├── components/
│   ├── sidebar.py
│   ├── metrics.py
│   └── charts.py
│
└── pages/
    ├── 1_Executive_Overview.py
    ├── 2_Startup_Ecosystem.py
    ├── 3_Funding_Intelligence.py
    ├── 4_Industry_Intelligence.py
    ├── 5_Investor_Intelligence.py
    ├── 6_Geographic_Intelligence.py
    ├── 7_Startup_Explorer.py
    ├── 8_OLAP_Analytics.py
    ├── 9_AI_Insights.py
    ├── 10_Funding_Forecast.py
    ├── 11_Reports_Export.py
    └── 12_Startup_Evaluator.py
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/blanushka004/VentureLens.git
cd VentureLens
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Configuration

Create a PostgreSQL database for VentureLens.

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/venturelens_db
```

Never commit the `.env` file to GitHub.

Initialize the database and run the ETL pipeline as required by your local setup.

---

## ▶️ Running VentureLens

Start the application with:

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 🧪 Testing

The repository contains tests for multiple layers of the application.

Example:

```bash
python test_system.py
```

Additional tests cover:

```text
Analytics
Startup Analysis
Funding & Industry Analysis
Investor Analysis
Geographic Analysis
OLAP Analytics
Streamlit Components
```

---

## 🌐 Deployment

VentureLens is designed to be deployed using:

```text
GitHub
   ↓
Streamlit Community Cloud
   ↓
Cloud PostgreSQL
```

The production database connection should be stored using deployment secrets rather than committed to the repository.

---

## ⚠️ Disclaimer

Startup evaluation scores, funding forecasts, opportunity indicators, and recommendations generated by VentureLens are analytical estimates based on available data and user-provided information.

They should not be interpreted as guarantees of startup success, company valuation, investment returns, or professional financial advice.

---

## 👩‍💻 Author

**Lakshmi Anushka Bokka**

Computer Science & Business Systems  
Aspiring Software Engineer

GitHub: **@blanushka004**

---

## ⭐ Project Goal

VentureLens was built to move beyond traditional static startup dashboards.

The goal is to combine:

**Data Engineering + Database Systems + Business Intelligence + Machine Learning + Interactive Analytics + Decision Support**

into a single startup ecosystem intelligence platform.
