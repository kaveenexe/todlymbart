from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the ChatPromptTemplate
template = """You are an expert in child nutrition and development. Please provide a concise, plain-text answer to the following question without any special characters or formatting:

Question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

# Set up the OllamaLLM model
# REMOVE ENDPOINT IF RUN ON LOCAL MACHINE , base_url="http://34.56.218.131:11434/"
ollama_model = OllamaLLM(model="blackalpha/todlymist", base_url="http://34.56.218.131:11434/")
