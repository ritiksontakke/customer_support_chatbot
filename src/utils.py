from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langfuse import Langfuse


load_dotenv()
langfuse = Langfuse()

def get_openai_model():
    return ChatOpenAI(
        model="gpt-5.4-nano",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

def get_model():
    return get_openai_model()

def get_system_prompt(prompt_name: str = "cutomer_chatbot"):
    try:
        prompt = langfuse.get_prompt(
            prompt_name,
            label="production"  # or "latest"
        )

        # Depending on Langfuse version
        return prompt.prompt

    except Exception as e:
        print(f"Failed to load prompt: {e}")

        return """
        You are an Orchestrator Agent.
        Route tasks to the correct sub-agent.
        Never hallucinate.
        """