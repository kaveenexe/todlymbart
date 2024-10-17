from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the ChatPromptTemplate
template = """You are an expert in child nutrition and development. Please provide a concise, plain-text answer to the following question without any special characters or formatting:

Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

# Set up the OllamaLLM model
ollama_model = OllamaLLM(model="blackalpha/todlymist")
