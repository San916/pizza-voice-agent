from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from logger_config import logger

load_dotenv()
llm = OpenAI()

classification_prompt_template = """
Classify the following user's query into one of the following categories:

- Location and Contact
- Menu
- Delivery Information
- Special Offers
- Intent to Leave
- General Query

User's query: "{query}"
"""

classification_prompt = PromptTemplate(input_variables = ["query"], template = classification_prompt_template)
classification_chain = LLMChain(prompt = classification_prompt, llm = llm)

# Given a query, classify it based on the 6 above categories
def classify_intent(query):
    logger.debug("Classifying user query.")
    result = classification_chain.predict(query = query).strip()
    logger.debug("Classification result: " + result)
    return result