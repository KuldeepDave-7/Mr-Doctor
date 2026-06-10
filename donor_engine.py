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


# --- Testing the Engine ---
if __name__ == "__main__":
    # Initialize the engine (Loads the CSV)
    engine = MatchingEngine("data.csv")
    
    print("Searching for B+ Donors...")
    # Run the search
    results = engine.find_optimal_donors("B+")
    print(results)
    # Display results
    for rank, donor in enumerate(results, start=1):
        print(f"Match {rank}: {donor['name']} ({donor['blood_group']}) - Last donated {donor['days_since_donation']} days ago.")     