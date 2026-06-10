import pandas as pd
from sqlalchemy import create_engine

class MatchingEngine:
    def __init__(self, db_url):
        # 1. Load the database into a Pandas DataFrame when the engine starts

        self.db_engine = create_engine(db_url)
        self.db = pd.read_sql("SELECT * FROM donors_table", self.db_engine)

        self.compatibility_rules = {
            "B+": ["B+", "B-", "O+", "O-"],
            "A+": ["A+", "A-", "O+", "O-"],
            "O+": ["O+", "O-"],
            "O-": ["O-"],
            "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        }

    def find_optimal_donors(self, requested_blood_group, max_distance=50):
        
        # Get the safe blood types for the recipient
        safe_types = self.compatibility_rules.get(requested_blood_group, [])
        
        # Step 1: Filter by Blood Type
        eligible = self.db[self.db['blood_group'].isin(safe_types)]
        
        # Step 2: Apply the Medical Cooldown Filter
        eligible = eligible[eligible['days_since_donation'] >= 56]
        
        eligible = eligible.sort_values(by="days_since_donation", ascending=False)
        
        # Convert the resulting DataFrame back into a standard list of dictionaries 
        return eligible.to_dict(orient='records')

if __name__ == "__main__":
    # 1. Put your Render PostgreSQL URL here
    DB_URL = "postgresql://triage_db_i5sf_user:Um5MLaKyiwkE6Vd4wNWFQOTv1t6nOUhV@dpg-d8kpgjegvqtc73fm34b0-a.oregon-postgres.render.com/triage_db_i5sf"
    
    # 2. Initialize the engine with the database
    engine = MatchingEngine(DB_URL)
    
    print("Searching for B+ Donors...")
    # 3. Run the search
    results = engine.find_optimal_donors("B+")
    
    # 4. Display results
    for rank, donor in enumerate(results, start=1):
        # Note: Make sure the dictionary keys match your database column names exactly!
        print(f"Match {rank}: {donor['name']} ({donor['blood_group']}) - Last donated {donor['days_since_donation']} days ago.")