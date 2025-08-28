# utils/conversation.py
import json
import os

CANDIDATE_FILE = "candidates.json"

def mask_email(email: str) -> str:
    """Mask email for privacy (keep first char + domain)."""
    if "@" not in email:
        return email
    name, domain = email.split("@", 1)
    if len(name) > 1:
        return name[0] + "***@" + domain
    return "***@" + domain

def mask_phone(phone: str) -> str:
    """Mask phone number (keep last 3 digits)."""
    if len(phone) > 3:
        return "*" * (len(phone) - 3) + phone[-3:]
    return phone

def load_candidates():
    """Load all candidates from file (returns list)."""
    if not os.path.exists(CANDIDATE_FILE):
        return []
    try:
        with open(CANDIDATE_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []

def save_candidate(candidate):
    """Append a new candidate to file with masked email/phone."""
    candidates = load_candidates()

    # 🔒 Mask sensitive info
    candidate["Email Address"] = mask_email(candidate.get("Email Address", ""))
    candidate["Phone Number"] = mask_phone(candidate.get("Phone Number", ""))

    candidates.append(candidate)
    with open(CANDIDATE_FILE, "w") as f:
        json.dump(candidates, f, indent=4)
