import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split  #It splits data into an 80% Training set (to teach the model) and a 20% Testing set (to grade the model).
from sklearn.preprocessing import LabelEncoder    # Translates textual categories into numerical integers for the model.(e.g., North ➔ 0, South ➔ 1)
from sklearn.ensemble import RandomForestRegressor  #(ML Brain) It combines the outputs of dozens of independent trees (an ensemble) to predict highly stable, accurate numeric values for drug order volumes.Ensemble Method (a group working together).
                                                    # An ensemble algorithm that builds multiple independent decision trees on random subsets of data, then averages their numeric outputs to create a highly stable, accurate prediction.
from sklearn.metrics import mean_squared_error,r2_score  # RMSE (how close your predictions are to the real answers) and R^2 (how well your model understands data trends).Grading scores (RMSE and R2) evaluate forecast accuracy.

def run_forecast_pipeline(db_path="pharma_warehouse.db"):   #clean, reusable function
    conn=sqlite3.connect(db_path)      #Opens a connection channel directly to your structural data warehouse file.

    raw_query = "SELECT Date, Region, Drug_Name, Hospital_Name, Units_Ordered FROM sales_records"
    df = pd.read_sql_query(raw_query, conn)   # SQL EXTRACTION: Runs a targeted SELECT query to pull clean historical transaction columns into memory.

   # FEATURE ENGINEERING: Extracts numerical temporal components from datetime string
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month
    df['DayOfWeek'] = df['Date'].dt.dayofweek

    # LABEL ENCODING: Converts distinct text categories into sequential integers for scikit-learn
    encoders = {}
    categorical_cols = ['Region', 'Drug_Name', 'Hospital_Name']
    for col in categorical_cols:
        le = LabelEncoder()
        df[f'{col}_Encoded'] = le.fit_transform(df[col])
        encoders[col] = le

    # MATRICES: Separating independent feature inputs (X) from target dependent variable (y)
    feature_cols = ['Month', 'DayOfWeek', 'Region_Encoded', 'Drug_Name_Encoded', 'Hospital_Name_Encoded']
    X = df[feature_cols]
    y = df['Units_Ordered']

    # CROSS-VALIDATION: Split data into training matrix (80%) and test matrix (20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # MODEL ARCHITECTURE: Initializing and fitting ensemble Random Forest Regressor
      #Fits a 50-tree Random Forest Regressor using parallel processor cores (n_jobs=-1).
    regressor = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1)
    regressor.fit(X_train, y_train)

    # METRICS EVALUATION: Extracts RMSE and R2 coefficients from validation split
    predictions = regressor.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"\n--- Pipeline Performance Evaluator ---")
    print(f"Validation Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Validation R-squared (R2) Coefficient: {r2:.4f}")

    # INFERENCE: Generates total forecasted demand values for warehouse comparison
    df['Predicted_Demand'] = np.round(regressor.predict(X))
    
    # BUSINESS LOGIC ALERT: Flags shortage if predicted velocity passes warehouse limit bounds
    df['Alert_Status'] = np.where(df['Predicted_Demand'] > 110, 'CRITICAL SHORTAGE', 'NORMAL')

    # MIGRATION: Streams processed forecasting vectors into target relational database table
    export_cols = ['Date', 'Region', 'Drug_Name', 'Hospital_Name', 'Units_Ordered', 'Predicted_Demand', 'Alert_Status']
    output_df = df[export_cols]
    output_df.to_sql('demand_predictions', conn, if_exists='replace', index=False)

    # CLEANUP: Unlocks database files and flushes background runtime memory
    conn.close()
    print("\nInference layer successfully updated in structural target table: 'demand_predictions'.")

if __name__ == "__main__":
    run_forecast_pipeline()
