from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TriageEngine:
    def __init__(self):
        # Our pre-defined training data: Diseases and their associated text descriptions
        self.diseases = [
            "Common Cold", 
            "Influenza (Flu)", 
            "Food Poisoning"
        ]
        
        self.descriptions = [
            "mild running nose cough sore throat low fever sneeze",
            "high sudden fever chills severe body ache dry cough exhaustion",
            "stomach ache nausea vomiting diarrhea cramps dehydration"
        ]
        
        # Initialize the Vectorizer. This converts raw text into numbers based on word importance.
        self.vectorizer = TfidfVectorizer()
        
        # Turn our known descriptions into geometric vectors
        self.disease_vectors = self.vectorizer.fit_transform(self.descriptions)

    def diagnose(self, user_input):
        """Calculates the geometric distance between user input and known diseases."""
        
        # 1. Transform the user's input text into the exact same vector space
        user_vector = self.vectorizer.transform([user_input])
        
        # 2. Calculate the 'Cosine Similarity' (the angle between vectors)
        # This compares the user vector against all disease vectors simultaneously
        similarity_scores = cosine_similarity(user_vector, self.disease_vectors)[0]
        
        # 3. Find the index of the highest score
        best_match_idx = similarity_scores.argmax()
        highest_score = similarity_scores[best_match_idx]
        
        # If the text doesn't match anything well, return a safe fallback
        if highest_score < 0.1:
            return "Unknown Condition", "Symptoms too vague. Please consult a professional."
            
        predicted_disease = self.diseases[best_match_idx]
        
        # Triage recommendations dictionary
        triage_advice = {
            "Common Cold": "Likely a common cold. Rest, stay hydrated, and take over-the-counter decongestants if needed.",
            "Influenza (Flu)": "High probability of Flu. Limit contact with others, rest, and monitor your temperature. Seek clinic care if fever stays dangerously high.",
            "Food Poisoning": "Signs of foodborne illness. Focus on electrolyte replacement fluids. Avoid solid foods for a few hours. See a doctor if vomiting persists past 24 hours."
        }
        
        return predicted_disease, triage_advice.get(predicted_disease)

# --- Test the Triage Logic ---
if __name__ == "__main__":
    engine = TriageEngine()

    
    # Simulating a user typing natural symptoms
    sample_input = "I woke up with a massive sudden fever and my whole body aches terribly"
    
    disease, advice = engine.diagnose(sample_input)
    
    print(f"User Input: '{sample_input}'")
    print(f"\nPredicted Condition: {disease}")
    print(f"Triage Advice: {advice}")


