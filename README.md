# drug-recommendation-engine

Personalized Drug Recommendation Engine that suggests medications based on:
- patient profile (`age`, `allergies`, `history`, `current medications`)
- disease
- drug-drug interactions

It includes:
- knowledge graph (`drugs + diseases + relations`)
- risk scoring
- alternative medicines for conflict cases

## Repo Structure
```text
drug-recommendation-engine/
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   ├── drugs.csv
│   ├── diseases.csv
│   ├── interactions.csv
├── backend/
│   ├── main.py
│   ├── routes/recommend.py
│   ├── services/recommender.py
│   ├── services/risk_scoring.py
│   ├── services/alternatives.py
│   ├── graph/knowledge_graph.py
│   └── models/schemas.py
├── ai/
│   ├── llm_engine.py
│   └── prompts.py
├── frontend/
│   └── app.py
└── notebooks/
    └── data_exploration.ipynb
```

## Setup
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Backend (FastAPI)
```bash
uvicorn backend.main:app --reload
```

Open:
- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Run Frontend (Streamlit)
```bash
streamlit run frontend/app.py
```

## Deploy UI Separately
- Backend: deploy the FastAPI backend using Vercel with `vercel.json` and `api/index.py`.
- UI: deploy the frontend dashboard separately on Streamlit Cloud using `frontend/app.py`.
- On Streamlit Cloud, configure a secret named `api_base_url` with your backend URL, e.g. `https://your-api-url.vercel.app`.

## Notes
- This project is decision-support oriented and should be reviewed by clinicians before real-world use.
- AI module in `ai/` is scaffolding for future LLM-based explanation workflows.
