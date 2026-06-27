# 📦 Pharmaceutical Commercial Analytics & Predictive Demand Engine

An end-to-end predictive analytics architecture and operational deployment engine designed for pharmaceutical supply chain optimization. This system utilizes machine learning to forecast regional drug demand, isolates critical stockout risks via automated constraints logic, and exposes real-time data across high-performance web logs and strategic executive dashboards.

---

## 🖼️ Interface & Asset Previews

### 🔍 Interactive Feature Breakdown: Dynamic Risk Isolation & Drill-Down

The repository showcases two operational states of the strategic Power BI dashboard, demonstrating real-time data cross-filtering and analytical responsiveness:

1. **Enterprise Macro View (State 1 - Global Distribution):**
   * Shows a macro-level snapshot across all clinical networks, computing a total requirement pool of **153.07K Units Demanded** against a pipeline prediction model threshold of **146.06K Units**. 
   * The system aggregates an institutional alert baseline of **1,225 active shortage metrics**, mapping out wide-scale corporate pipeline distribution.
    ![Enterprise Macro View]![alt text](<Global Distribution State.png>)

2. **Targeted Micro Filter View (State 2 - Isolated Risk Constraints):**
   * Demonstrates the dashboard's interactive slicing capabilities. When an analyst targets specific regional vectors, the entire canvas dynamically cross-filters down to **32.54K Total Units Demanded** and **31.20K Predicted Units**.
   * The Active Shortage Alerts card instantly recalculates to isolate exactly **264 high-risk local disruptions**, while the hospital matrix narrows down specifically to target urgent allocation exceptions across the *Max Super Speciality* clinical hub network.
   ![Targeted Micro Filter View]![alt text](<Isolated Risk Constraints State.png>)

#### 3. Operational Performance Layer (Static HTML Web Interface)
A lightweight execution grid compiled natively via Python to handle high-throughput warehousing records without the performance footprint of heavy runtime graphics. This interface formats operational target parameters and highlights logistical alerts directly on the floor level.

![Operational Web Interface Layout](<visual_dashboard.png>)
---

## 🚀 Key Architectural Highlights
* **Predictive Core:** Trained an ensemble **Random Forest Regressor** using Scikit-learn to forecast future inventory demand, optimizing stability across multi-dimensional categorical features.
* **Data Warehouse:** Engineered a localized enterprise layer utilizing **SQLite**, executing advanced analytical window functions (`LAG()`, `DENSE_RANK()`) to compute temporal delta trends and client densities.
* **Decoupled Dual-UI Presentation:**
  1. **Operational Layer:** A zero-server, high-performance static HTML compiler that streams warehouse records and dynamically styles priority allocations.
  2. **Strategic Executive Layer:** A Power BI corporate dashboard streaming live insights via an **ODBC Gateway Data Link**.

---

## 📊 System Architecture Flow
The engine functions across a modular data-to-insight workflow pipeline:

```text
[generate_data.py] ➔ [database_setup.py] ➔ [demand_forecast.py] ➔ [dashboard.py]
 (Raw CSV Engine)       (SQLite Schema)       (Random Forest ML)    (HTML Compiler)
        │                                                                   │
        └───────────────➔ [pharma_warehouse.db] 💡 ─────────────────────────┤
                                 │                                          ▼
                                 └─(ODBC Link)──➔ [Power BI Executive Terminal (.pbix)]


                                 📂 Repository File Mapping

PHARMA_ANALYTICS_PROJECT/
│
├── .venv/                                           # Python Virtual Environment
│
├── generate_data.py                                 # Simulates baseline transactional data
├── database_setup.py                                # Initializes SQLite structures & schemas
├── demand_forecast.py                               # Trains Scikit-Learn Random Forest Regressor
├── dashboard.py                                     # Compiles analysis models into visual grids
│
├── pharma_raw_data.csv                              # Ingested transactional core CSV dataset
├── pharma_warehouse.db                              # Active SQLite local enterprise warehouse
│
├── Pharmaceutical Commercial Analytics & Predictive Demand Engine.pbix # Strategic Power BI Asset
│
├── predicted.png                                    # Model performance validation visualization
├── quality.png                                      # Quality analysis metrics layout capture
├── shortage_alerts.png                              # Critical risk anomaly interface breakdown
└── visual_dashboard.html                            # Compiled high-contrast web dashboard layer

🛠️ Tech Stack & Dependencies
Core Language: Python 3.11+

Data Engineering & ML: Pandas, NumPy, Scikit-learn, SQLite3

Analytics & Visualization: Power BI Desktop, Advanced DAX, Native HTML5 / CSS3

⚙️ Core Operational UI Engine (dashboard.py)
The system handles backend compilation by dynamically reading pipeline forecasts and binding variables into an enterprise-grade responsive wrapper grid:

Automated Risk Exception Matrix: Systematically flags operational targets breaching a strict safety threshold metric of 110 units, isolating high-risk regional shortfalls.

Data-Driven UI Compiling: Loops through analytical logs to bind dynamic, high-contrast conditional execution markers directly into the grid layer.

📈 Strategic Analytics Terminal (Power BI Assets)
The companion Power BI asset transforms backend forecasting metrics into operational dashboards engineered explicitly for Life Sciences consulting workflows:

High-visibility Executive KPI Cards isolating Total Demanded Volumes vs. Predictive Pipelines.

Combined Actual vs. Forecast Validation Plots tracking model accuracy over historical trend paths.

A granular Hospital Deficit Allocation Table mapping supply shortfalls across major medical hubs (e.g., Apollo Medical Center, Max Super Speciality).

🎯 Commercial Value (For Life Sciences Consultancies)
Supply Chain Resiliency: Empowers commercial operations managers to redirect inventory streams proactively to critical zones prior to local regional stockouts.

Sales Targeting: Provides account representatives with precise predictive analytics to align distribution cycles tightly with hospital procurement patterns.

Low-Overhead Engineering: Bypasses heavy infrastructure footprints via lean static pipelines, allowing high-performance field execution.
