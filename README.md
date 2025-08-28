# TalentScout – AI Hiring Assistant

TalentScout is an intelligent AI-powered hiring assistant that helps recruiters screen candidates by:

- Collecting candidate details  
- Asking technical questions based on their tech stack and experience  
- Evaluating responses  
- Respecting data privacy and allowing candidates to exit gracefully  

This project demonstrates prompt engineering, LLM integration, and interactive candidate interviews using the OpenAI API.

---

## Features

- **Candidate Information Gathering** – Collects name, email, tech stack, and experience.  
- **Dynamic Technical Questions** – Adjusts question difficulty according to experience level.  
- **Context-Aware Evaluation** – Evaluates candidate answers within the declared tech stack.  
- **Conversation Exit** – Candidate can type `exit` anytime to end the interview.  
- **Data Privacy** – Candidate information is anonymized and not stored permanently.  

---

## 🛠Tech Stack

- **Language Model**: OpenAI GPT-4o / GPT-4o-mini  
- **Framework**: Streamlit (Frontend UI)  
- **Backend**: Python  
- **Environment**: dotenv for API key management  

---

## Project Structure

- **.venv/** → Python virtual environment  

- **utils/**
  - `__init__.py` → Package initializer  
  - `conversation.py` → Candidate data save/load helpers  
  - `openai_utils.py` → LLM API call functions  

- `app.py` → Streamlit frontend application  
- `candidates.json` → Temporary storage for candidate details  
- `prompts.py` → System and user prompts  
- `requirements.txt` → Python dependencies  
- `.env` → API key and environment variables  
- `.gitignore` → Git ignore rules  




## Setup & Installation

**1. Clone the repo**

```bash
git clone https://github.com/<your-username>/TalentScout-Hiring-Assistant.git
cd TalentScout-Hiring-Assistant
```

**2. Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```
**4. Add your OpenAI API key to .env**
```bash
OPENAI_API_KEY=your_api_key_here
```
**5. Run the Streamlit app**
```bash
streamlit run app.py
```

## Usage
- Start the app and enter candidate details.  
- The assistant asks role-specific technical questions.  
- Candidate provides answers.  
- Candidate can type exit anytime to leave the interview.  

## Data Privacy & Exit
- Candidate data is stored only in-memory (or temporary JSON if enabled).  
- No personal data is logged permanently.  
- Candidate can type exit to immediately stop the conversation.  

## Example Interaction
- **TalentScout**: Hello! I am TalentScout, your hiring assistant. Can I start by asking your name and tech stack?  
- **Candidate**: I am Rahul, Python & SQL developer with 3 years of experience.  
- **TalentScout**: Great, Rahul! Since you have 3 years of experience, I'll ask intermediate-level Python questions.  
- **Question**: What is the difference between a list and a tuple in Python?  
- **Candidate**: A list is mutable, a tuple is immutable.  
- **TalentScout**: Correct!  

## Assignment Alignment
- Prompt Engineering → Tech questions aligned with stack & experience.  
- Dynamic Questioning → Difficulty increases with experience.  
- Privacy & Exit → Candidate can exit anytime; data not stored permanently.  

## Future Enhancements
- Recruiter Dashboard → Centralized view of candidate performance & analytics.  
- Adaptive Scoring → AI-based evaluation and scoring of candidate responses.  
- Question Bank Expansion → Support for more domains (AI, DevOps, Cloud, etc.).  
- Interview History → Securely store past interviews for recruiters (with opt-in consent).  
- Multilingual Support → Allow interviews in Hindi, Spanish, etc.  
