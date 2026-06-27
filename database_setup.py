# 1)importing requirements
import pandas as pd
import sqlite3

# 2)loading csv file-pharma_raw_data.csv
csv_file='pharma_raw_data.csv'

# try ... except FileNotFoundError: This is a safety mechanism called Exception Handling.
# The script tries to execute the code inside the try block.If the CSV file is missing, 
# instead of crashing with a massive ugly error screen,it catches the specific FileNotFoundError,
# prints a helpful reminder message, and exits gracefully using exit().
try:                        
    df=pd.read_csv(csv_file)
    print("1. CSV file loaded successfully.")
except FileNotFoundError:
    print(f"Error:{csv_file} not found!")
    exit()

# 3) Establishing the database connection (sqlite3)-
conn = sqlite3.connect('pharma_warehouse.db')  #opens (or creates) a database named pharma_warehouse.db
cursor = conn.cursor()  #cursor = conn.cursor(): A database cursor is an active control object.
                        #Think of it like a blinking typing cursor or an invisible hand inside the database.
                        #Cursor as a pointer or messenger that carries SQL statements to the database.
                        #Whenever you want to type or run a SQL command, you tell the cursor to do it.

# 4) Migrating Data from python to SQL-
df.to_sql('sales_records',conn, if_exists='replace', index=False) # Save DataFrame to SQL table (replace old table if it exists)
                                                                  #index=False → This prevents Pandas from adding an unnecessary extra column tracking of row numbers.
print("2. All 10,000 records safely migrated to SQL table:- 'sales_records'.")

# 5) performing Advanced Window Functions in SQLite--
    # A: Calculating Regional Running Totals--
running_total_query = """
SELECT 
    Transaction_ID, 
    Date, 
    Region, 
    Drug_Name, 
    Units_Ordered,
    SUM(Units_Ordered) OVER (PARTITION BY Region ORDER BY Date) as Cumulative_Units_Region
FROM sales_records
LIMIT 5;
"""    ##--> Multi-line string in python(useful for writing SQL queries neatly)

    # B: Ranking Top Hospitals--
rank_query = """
SELECT 
    Hospital_Name,
    Region,
    SUM(Units_Ordered) as Total_Units,
    DENSE_RANK() OVER (PARTITION BY Region ORDER BY SUM(Units_Ordered) DESC) as Hospital_Rank
FROM sales_records
GROUP BY Hospital_Name, Region
LIMIT 5;
"""

    # C: Fetching the previous transaction's volume(Using LAG function) --
lag_query = """
SELECT 
    Transaction_ID, 
    Region, 
    Drug_Name, 
    Date, 
    Units_Ordered,
    LAG(Units_Ordered, 1, 0) OVER (PARTITION BY Region, Drug_Name ORDER BY Date) as Previous_Orders
FROM sales_records
LIMIT 5;
"""
         # WINDOW QUERY: Calculates metrics across rows while keeping individual transaction rows intact (no collapsing data).
         # DELTA DETECTION (LAG): Compares current row values with previous rows to calculate shifts/trends over time without complex table joins.
         # Delta(variance) = Current Units Ordered - Previous Units Ordered.

# 6) Running above Queries and Printing Results--

print("\n[COMPUTING REGIONAL CUMULATIVE VOLUME--]")
cursor.execute(running_total_query)
for row in cursor.fetchall(): 
    print(row)  

print("\n[REGIONAL PROCUREMENT DENSITY RANKINGS--]")
cursor.execute(rank_query)
for row in cursor.fetchall(): 
    print(row)  

print("\n[DELTA DETECTION (Variance) USING LAG()--]")
cursor.execute(lag_query)
for row in cursor.fetchall(): 
    print(row)  

# 7) Keeping and Clean Up-
conn.close()        ## CLEANUP (conn.close): Safely saves all data changes and unlocks the database file so other applications (like Streamlit/Power BI) can access it.
print("\nLocal 'pharma_warehouse.db' is created and fully queryable.")