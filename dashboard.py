import sqlite3
import pandas as pd

def build_static_dashboard():
    # 1. DATA INGESTION: Connects to your local warehouse
    conn = sqlite3.connect('pharma_warehouse.db')
    df = pd.read_sql_query("SELECT * FROM demand_predictions", conn)
    conn.close()
    
    # 2. METRICS AGGREGATION: Computes scoreboard counters
    total_actual = int(df['Units_Ordered'].sum())
    total_pred = int(df['Predicted_Demand'].sum())
    shortages = int((df['Alert_Status'] == 'CRITICAL SHORTAGE').sum())
    
    # 3. HTML TABLE COMPILATION: Dynamically builds the rows
    table_rows = ""
    for idx, row in df.head(15).iterrows():
        badge_cls = "critical" if row['Alert_Status'] == "CRITICAL SHORTAGE" else "normal"
        table_rows += f"""
        <tr>
            <td>{row['Date']}</td>
            <td>{row['Region']}</td>
            <td>{row['Drug_Name']}</td>
            <td>{int(row['Units_Ordered'])} units</td>
            <td>{row['Predicted_Demand']} units</td>
            <td><span class="badge {badge_cls}">{row['Alert_Status']}</span></td>
        </tr>"""
        
    # 4. ALERTS COMPILATION: Generates target side panels
    shortage_cards = ""
    shortage_df = df[df['Alert_Status'] == 'CRITICAL SHORTAGE'].head(6)
    for idx, row in shortage_df.iterrows():
        shortage_cards += f"""
        <div class="alert-box">
            <div>
                <div class="alert-title">{row['Hospital_Name']}</div>
                <div class="alert-desc">{row['Drug_Name']}</div>
            </div>
            <div class="alert-title" style="font-size: 12pt;">{row['Predicted_Demand']}</div>
        </div>"""

    # 5. ENTERPRISE CSS LAYOUT DESIGN
    html_layout = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pharma Demand Analytics Portal</title>
    <style>
        * {{ box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        body {{ background-color: #f4f6f9; margin: 0; padding: 20px; color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        .header h1 {{ margin: 0; font-size: 20pt; font-weight: 600; }}
        .header p {{ margin: 5px 0 0 0; opacity: 0.9; font-size: 10pt; }}
        .metrics-grid {{ display: flex; gap: 20px; margin-bottom: 25px; }}
        .metric-card {{ flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border-left: 5px solid #2a5298; }}
        .metric-card.alert {{ border-left-color: #d9534f; }}
        .metric-label {{ font-size: 9pt; text-transform: uppercase; color: #777; font-weight: bold; }}
        .metric-value {{ font-size: 22pt; font-weight: bold; margin-top: 5px; color: #1e3c72; }}
        .metric-value.alert-text {{ color: #d9534f; }}
        .content-layout {{ display: flex; gap: 20px; }}
        .panel-left {{ flex: 2; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        .panel-right {{ flex: 1; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        h2 {{ margin-top: 0; font-size: 13pt; color: #1e3c72; border-bottom: 2px solid #f4f6f9; padding-bottom: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 9.5pt; }}
        th {{ background-color: #f4f6f9; text-align: left; padding: 12px; color: #555; font-weight: 600; border-bottom: 2px solid #ddd; }}
        td {{ padding: 12px; border-bottom: 1px solid #eee; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 7.5pt; font-weight: bold; }}
        .badge.critical {{ background-color: #fddede; color: #d9534f; }}
        .badge.normal {{ background-color: #e2f0d9; color: #385723; }}
        .alert-box {{ background-color: #fdf2f2; border: 1px solid #fde2e2; padding: 12px; border-radius: 6px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between; }}
        .alert-title {{ font-weight: bold; color: #b91c1c; font-size: 9.5pt; }}
        .alert-desc {{ color: #7f1d1d; font-size: 9pt; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📦 Pharmaceutical Commercial Analytics & Predictive Demand Engine</h1>
            <p>Enterprise Deployment Interface Layer • Connected to Local SQLite Warehouse</p>
        </div>
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Historical Volume Demanded</div>
                <div class="metric-value">{total_actual:,} <span style="font-size: 10pt; font-weight: normal; color: #555;">units</span></div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Pipeline Forecast Volume</div>
                <div class="metric-value">{total_pred:,} <span style="font-size: 10pt; font-weight: normal; color: #555;">units</span></div>
            </div>
            <div class="metric-card alert">
                <div class="metric-label">Active Supply Chain Disruptions</div>
                <div class="metric-value alert-text">{shortages:,} <span style="font-size: 10pt; font-weight: normal; color: #d9534f;">alerts</span></div>
            </div>
        </div>
        <div class="content-layout">
            <div class="panel-left">
                <h2>📊 Live Prediction Model Logs (Sample Matrix)</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Region</th>
                            <th>Drug Product</th>
                            <th>Actual Orders</th>
                            <th>Predicted Demand</th>
                            <th>Logistics Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows}
                    </tbody>
                </table>
            </div>
            <div class="panel-right">
                <h2>🚨 Critical Shortage Allocation Exceptions</h2>
                {shortage_cards}
            </div>
        </div>
    </div>
</body>
</html>"""
    
    with open("visual_dashboard.html", "w", encoding="utf-8") as out:
        out.write(html_layout)
    print("\nDashboard compiled successfully into 'visual_dashboard.html'!")

if __name__ == '__main__':
    build_static_dashboard()