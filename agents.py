## --------------------------- 
## agents.py (Fixed for CrewAI + Groq LLM) 
## ---------------------------

import os
from dotenv import load_dotenv
from crewai import LLM, Agent
from tools import read_pdf_tool, investment_tool, risk_tool

# Load environment variables
load_dotenv()

# -------------------------
# Initialize LLM with Groq API key (FIXED)
# -------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "your api key"

# FIX: Use the correct Groq model format
llm = LLM(
    model="groq/llama-3.1-8b-instant",  # <- Correct Groq model format
    temperature=0.1,
    max_tokens=1000,
    api_key=GROQ_API_KEY
)

# Alternative models
# llm = LLM(model="groq/mixtral-8x7b-32768", api_key=GROQ_API_KEY)
# llm = LLM(model="groq/llama-3.1-70b-versatile", api_key=GROQ_API_KEY)

# -------------------------
# Financial Analyst Agent
# -------------------------
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Accurately analyze financial documents and provide actionable investment insights.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an experienced financial analyst with deep knowledge of markets, "
        "financial ratios, and corporate filings. You provide clear, practical insights."
    ),
    tools=[read_pdf_tool, investment_tool, risk_tool],
    llm=llm,
    max_iter=1,
    max_rpm=3,
    allow_delegation=True
)

# -------------------------
# Document Verifier Agent
# -------------------------
verifier = Agent(
    role="Financial Document Verifier",
    goal="Check whether the uploaded document is a valid financial report and summarize key sections.",
    verbose=True,
    memory=False,
    backstory=(
        "You have expertise in financial compliance. You carefully check documents "
        "to confirm they are genuine financial reports."
    ),
    tools=[read_pdf_tool],
    llm=llm,
    max_iter=1,
    max_rpm=3,
    allow_delegation=False
)

# -------------------------
# Investment Advisor Agent
# -------------------------
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide tailored investment recommendations based on the financial analysis.",
    verbose=True,
    memory=False,
    backstory=(
        "You are a trusted investment advisor who balances risks and opportunities, "
        "helping clients make well-informed decisions."
    ),
    tools=[investment_tool],
    llm=llm,
    max_iter=1,
    max_rpm=3,
    allow_delegation=False
)

# -------------------------
# Risk Assessment Agent
# -------------------------
risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Evaluate risks in financial documents and suggest clear mitigation strategies.",
    verbose=True,
    memory=False,
    backstory=(
        "You specialize in financial risk management and regulatory compliance. "
        "You identify potential threats and advise on mitigations."
    ),
    tools=[risk_tool],
    llm=llm,
    max_iter=1,
    max_rpm=3,
    allow_delegation=False
)