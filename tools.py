import os
from dotenv import load_dotenv
from crewai.tools import BaseTool
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

# -------------------------
# PDF Reading Tool
# -------------------------
class ReadPDFTool(BaseTool):
    name: str = "Read PDF"
    description: str = "Reads a PDF file from a given path and returns its full text content."
    
    def _run(self, path: str = "data/sample.pdf") -> str:  # ✅ sync now
        """Synchronous PDF reading tool"""
        try:
            if not os.path.exists(path):
                return f"❌ File not found: {path}"
            
            loader = PyPDFLoader(path)
            docs = loader.load()
            text_content = ""
            
            for doc in docs:
                content = doc.page_content.strip()
                # Clean up excessive newlines
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                text_content += content + "\n"
            
            return text_content if text_content else "⚠️ No content extracted from PDF."
        
        except Exception as e:
            return f"❌ Error reading PDF: {str(e)}"

# -------------------------
# Investment Analysis Tool
# -------------------------
class InvestmentTool(BaseTool):
    name: str = "Investment Analysis"
    description: str = "Analyzes financial document text and provides investment insights."
    
    def _run(self, financial_document_data: str) -> str:  # ✅ sync
        try:
            processed_data = financial_document_data.replace("  ", " ").strip()
            
            key_terms = ["revenue", "profit", "loss", "debt", "assets", "equity", "cash flow"]
            found_terms = [term for term in key_terms if term.lower() in processed_data.lower()]
            
            analysis = f"📊 Investment Analysis:\n"
            analysis += f"✅ Financial terms found: {', '.join(found_terms)}\n"
            analysis += f"📄 Document preview: {processed_data[:500]}...\n"
            analysis += f"💡 This appears to be a valid financial document for analysis."
            
            return analysis
            
        except Exception as e:
            return f"❌ Error in investment analysis: {str(e)}"

# -------------------------
# Risk Assessment Tool
# -------------------------
class RiskTool(BaseTool):
    name: str = "Risk Assessment"
    description: str = "Evaluates risks in the given financial document."
    
    def _run(self, financial_document_data: str) -> str:  # ✅ sync
        try:
            risk_keywords = ["debt", "loss", "decline", "risk", "liability", "uncertainty"]
            found_risks = [keyword for keyword in risk_keywords if keyword.lower() in financial_document_data.lower()]
            
            risk_assessment = f"⚠️ Risk Assessment:\n"
            if found_risks:
                risk_assessment += f"🔴 Risk indicators found: {', '.join(found_risks)}\n"
                risk_assessment += f"📋 Recommendation: Detailed due diligence required\n"
            else:
                risk_assessment += f"🟢 No major risk indicators detected in initial scan\n"
            
            risk_assessment += f"💼 General advice: Always diversify your investment portfolio\n"
            risk_assessment += f"📊 Consider market volatility and economic conditions"
            
            return risk_assessment
            
        except Exception as e:
            return f"❌ Error in risk assessment: {str(e)}"

# Tool instances
# -------------------------
read_pdf_tool = ReadPDFTool()
investment_tool = InvestmentTool()
risk_tool = RiskTool()
