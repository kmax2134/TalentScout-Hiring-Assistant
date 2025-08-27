import json
import os

def load_candidates():
    if not os.path.exists("candidates.json"):
        return []  t
    
    with open("candidates.json", "r") as f:
        try:
            content = f.read().strip()
            if not content: 
                return []
            return json.loads(content)
        except json.JSONDecodeError:
            return [] 
        

def save_candidate(candidate):
    candidates = load_candidates()
    candidates.append(candidate)
    with open("candidates.json", "w") as f:
        json.dump(candidates, f, indent=4)
