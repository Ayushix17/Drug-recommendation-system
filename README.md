💊 AI-Powered Personalized Drug Recommendation Engine
<p align="center"> <img src="assets/demo.gif" alt="Demo" width="700"/> </p> <p align="center"> <b>An explainable, risk-aware clinical AI system for safe medication recommendations</b> </p>
<p align="center"> <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python"/> <img src="https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi"/> <img src="https://img.shields.io/badge/Streamlit-Frontend-red?logo=streamlit"/> <img src="https://img.shields.io/badge/LLM-AI-purple"/> <img src="https://img.shields.io/badge/Graph-Knowledge--Graph-orange"/> <img src="https://img.shields.io/badge/Status-Active-success"/> <img src="https://img.shields.io/badge/License-MIT-yellow"/> </p>
🧠 Overview

This project simulates a real-world clinical decision support system that goes beyond basic ML predictions.

It intelligently analyzes:

👤 Patient profile (age, allergies, history)
🦠 Disease conditions
💊 Drug interactions

…and generates:

✨ Safe, explainable, and personalized drug recommendations

🚀 Features
✨ Personalized Recommendations

Tailored to individual patient profiles

⚠️ Drug Interaction Detection

Prevents unsafe medication combinations

📊 Risk Scoring System

Classifies recommendations into Low / Medium / High

🔁 Alternative Drug Suggestions

Suggests safer substitutes automatically

🧠 Explainable AI (LLM-powered)

Generates human-readable reasoning

🕸️ Knowledge Graph Integration

Models real drug–disease relationships

🏗️ System Architecture
<p align="center"> <img src="assets/architecture.png" width="700"/> </p>
User → Frontend → FastAPI → (LLM + Graph + Risk Engine + Drug DB) → Output
🖥️ Demo
<p align="center"> <img src="assets/ui_input.png" width="400"/> <img src="assets/ui_output.png" width="400"/> </p>
🔹 Sample Output
Recommended Drug: Amlodipine
Risk Level: Medium
Alternatives: Losartan
Explanation: Generated via LLM
🕸️ Knowledge Graph
<p align="center"> <img src="assets/graph.png" width="500"/> </p>

Relationships Modeled:

Drug → Treats → Disease
Drug → Interacts With → Drug
Drug → Causes → Side Effect

⚙️ Tech Stack
| Layer       | Technology              |
| ----------- | ----------------------- |
| 🧩 Backend  | FastAPI                 |
| 🎨 Frontend | Streamlit               |
| 🧠 AI Layer | LLM (GPT / Open-source) |
| 🕸️ Graph   | NetworkX / Neo4j        |
| 📊 Data     | OpenFDA / DrugBank      |
| 🐍 Language | Python                  |

📁 Project Structure
drug-recommendation-engine/
│
├── backend/        # API & logic
├── frontend/       # Streamlit UI
├── ai/             # LLM + prompts
├── graph/          # Knowledge graph
├── data/           # datasets
├── assets/         # images & GIFs
├── notebooks/      # experiments
│
├── README.md
├── requirements.txt
└── .env.example

🔧 Installation

# Clone repository
git clone https://github.com/your-username/drug-recommendation-engine.git

cd drug-recommendation-engine

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn backend.main:app --reload

# Run frontend
streamlit run frontend/app.py

🔐 Environment Variables
OPENAI_API_KEY=your_api_key_here

📈 Future Improvements

🚀 Real-time EHR integration
🧠 RL-based doctor feedback loop
🌐 SaaS deployment for clinics
📊 Better clinical validation

🧠 Key Learnings
AI systems > standalone ML models
Knowledge graphs improve reasoning
Explainability is critical in healthcare
🤝 Contributing

Pull requests are welcome!

📜 License

MIT License

🌟 Support

If you like this project, ⭐ the repo and share it!

💼 Resume Highlight

Built an AI-powered personalized drug recommendation system using FastAPI, knowledge graphs, and LLMs, enabling safe, explainable, and patient-specific treatment recommendations.

