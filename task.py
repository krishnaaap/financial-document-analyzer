## Importing libraries and files
from crewai import Task
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import read_pdf_tool, investment_tool, risk_tool

# -----------------------------
# Task: Verification (First Step)
# -----------------------------
verification = Task(
    description=(
        "Verify whether the uploaded file at path '{file_path}' is a valid financial document "
        "(e.g., balance sheet, income statement, annual report, 10-K, earnings report). "
        "Use the read_pdf_tool to examine the document content."
    ),
    expected_output=(
        "Verification result:\n"
        "- Confirm whether the document is a financial report or not\n"
        "- Provide reasoning (e.g., contains financial terms, ratios, tables)\n"
        "- Mention the document type if identifiable\n"
        "- Brief summary of document structure and key sections found"
    ),
    agent=verifier,
    tools=[read_pdf_tool],
    async_execution=False,
)

# -----------------------------
# Task: Analyze Financial Document
# -----------------------------
analyze_financial_document = Task(
    description=(
        "Analyze the financial document at path '{file_path}' and answer the user's query: '{query}'. "
        "Use the read_pdf_tool to extract content. Focus on extracting meaningful insights such as "
        "revenue, expenses, financial ratios, growth trends, and investment opportunities. "
        "Build upon the verification results from the previous task."
    ),
    expected_output=(
        "Comprehensive financial analysis including:\n"
        "- Executive summary of key findings\n"
        "- Financial highlights (revenue, profit, expenses, debt, assets)\n"
        "- Important financial ratios and their interpretation\n"
        "- Growth or decline patterns over time\n"
        "- Key performance indicators\n"
        "- Summary of insights directly relevant to the user's query"
    ),
    agent=financial_analyst,
    tools=[read_pdf_tool, investment_tool, risk_tool],
    async_execution=False,
    context=[verification],  # Uses verification results
)

# -----------------------------
# Task: Investment Analysis
# -----------------------------
investment_analysis = Task(
    description=(
        "Based on the financial analysis results, evaluate investment opportunities and risks. "
        "Use the investment_tool to generate insights. Consider profitability, growth potential, "
        "industry outlook, competitive position, and financial health before making recommendations."
    ),
    expected_output=(
        "Detailed investment recommendations including:\n"
        "- Clear Buy/Hold/Sell recommendation with strong reasoning\n"
        "- 3-5 specific investment opportunities supported by financial data\n"
        "- Valuation insights (P/E ratios, book value, market cap considerations)\n"
        "- Growth prospects and market position analysis\n"
        "- Timeline for potential returns\n"
        "- Key factors that could change the recommendation"
    ),
    agent=investment_advisor,
    tools=[investment_tool],
    async_execution=False,
    context=[analyze_financial_document],  # Uses financial analysis results
)

# -----------------------------
# Task: Risk Assessment
# -----------------------------
risk_assessment = Task(
    description=(
        "Conduct a comprehensive risk evaluation based on the financial analysis. "
        "Use the risk_tool to identify potential threats. Focus on financial, operational, "
        "market, and regulatory risks that could impact investment decisions."
    ),
    expected_output=(
        "Structured risk assessment including:\n"
        "- Financial risks (debt levels, liquidity issues, revenue concentration)\n"
        "- Market risks (competition, economic sensitivity, industry trends)\n"
        "- Operational risks (management quality, supply chain, business model)\n"
        "- Regulatory/compliance risks (legal issues, regulatory changes)\n"
        "- Risk severity ratings (High/Medium/Low) with explanations\n"
        "- Specific risk mitigation strategies\n"
        "- Overall risk profile summary"
    ),
    agent=risk_assessor,
    tools=[risk_tool],
    async_execution=True,
    context=[analyze_financial_document, investment_analysis],  # Uses both previous results
)