# modules/ai_handler.py
from langchain_ollama import OllamaLLM


class AIHandler:
    def __init__(self, config):
        """Initialize AI handler"""
        self.config = config
        self.llm = OllamaLLM(
            model=config["ai"]["model"],
            base_url=config["ai"]["host"],
            temperature=config["ai"]["temperature"],
            timeout=config["ai"]["timeout"],
            num_ctx=config["ai"]["num_ctx"],
        )

    def get_command(self, prompt):
        """Get command suggestion from AI"""
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            raise Exception(f"Error getting AI command: {str(e)}")

    def analyze_output(self, prompt):
        """Analyze output using AI"""
        try:
            response = self.llm.invoke(prompt)
            return response.strip()
        except Exception as e:
            raise Exception(f"Error analyzing output: {str(e)}")
