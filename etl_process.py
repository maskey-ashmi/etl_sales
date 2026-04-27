import pandas as pd
import sqlite3
import datetime
import logging

# 1. Setup Logging (The "Black Box" recorder)
logging.basicConfig(filename='pipeline.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

def run_pipeline():
    try:
        # --- EXTRACT ---
        df = pd.read_csv('sales_raw.csv')
        raw_count = len(df)
        logging.info(f"Extract: Read {raw_count} rows from CSV.")

        # --- TRANSFORM ---
        # Select only the columns we need from your Kaggle list
        cols_to_keep = {'Order ID': 'order_id', 'Region': 'region', 'Sales': 'amount', 'Order Date': 'date'}
        df = df[list(cols_to_keep.keys())].rename(columns=cols_to_keep)
        
        # Data Cleaning
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        df = df.dropna(subset=['amount', 'order_id'])
        df['load_timestamp'] = datetime.datetime.now()
        
        # Logic Check: Remove negative sales
        df = df[df['amount'] >= 0]
        
        # --- LOAD ---
        conn = sqlite3.connect('sales.db')
        df.to_sql('sales_data', conn, if_exists='replace', index=False)
        
        # --- VALIDATE (The Reconciliation Check) ---
        final_count = pd.read_sql("SELECT COUNT(*) FROM sales_data", conn).iloc[0,0]
        logging.info(f"Load: {final_count} rows successfully written to SQLite.")
        
        # --- REPORT ---
        report = pd.read_sql("""
            SELECT region, SUM(amount) as total_revenue, COUNT(order_id) as total_orders
            FROM sales_data 
            GROUP BY region
        """, conn)
        report.to_csv('summary_report.csv', index=False)
        
        conn.close()
        print("Pipeline finished successfully! Check pipeline.log and summary_report.csv")

    except Exception as e:
        logging.error(f"Pipeline crashed: {str(e)}")

if __name__ == "__main__":
    run_pipeline()