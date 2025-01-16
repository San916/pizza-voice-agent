from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
import json
from logger_config import logger

# Load company data
def load_data(file_path):
    logger.debug("Loading company data.")
    with open(file_path, 'r') as f:
        return json.load(f)

# Turn company data into a list of documents
def generate_documents(data):
    logger.debug("Generating documents.")
    documents = []

    # Add Location and Contact Info
    location_contact = "Location and Contact Info:\n" \
        f"Location: {data['Location and Contact']['address']}, " \
        f"Phone: {data['Location and Contact']['phone']}, " \
        f"Email: {data['Location and Contact']['email']}, " \
        f"Hours: {data['Location and Contact']['hours']}\n\n"
    documents.append(Document(page_content = location_contact))

    # Add Menu Items
    menu_items = "Menu:\n"
    for pizza in data["Menu"]:
        menu_items += f"Pizza Name: {pizza['name']}, Price: {pizza['price']}, " \
            f"Ingredients: {pizza['ingredients']}, " \
            f"Vegetarian: {'Yes' if pizza['vegetarian'] else 'No'}\n" \
            f"Classic: {'Yes' if pizza['classic_pizza'] else 'No'}\n" \
            f"Signature: {'Yes' if pizza['signature_pizza'] else 'No'}\n"
    documents.append(Document(page_content = menu_items))

    # Add Delivery Information
    delivery_information = "Delivery Information:\n" \
        f"Free delivery within {data['Delivery Information']['free_delivery_radius']}, " \
        f"Delivery charge for {data['Delivery Information']['delivery_charge_radius']}, " \
        f"Minimum order: {data['Delivery Information']['minimum_order']}, " \
        f"Average delivery time: {data['Delivery Information']['delivery_time']}\n"
    documents.append(Document(page_content = delivery_information))
    
    # Add Special Offers
    special_offers = "Special Offers:\n"
    for offer in data["Special Offers"]:
        special_offers += f"Offer: {offer['offer']}, Discount: {offer['discount']}\n"
    documents.append(Document(page_content = special_offers))

    return documents

# Create and store document embeddings
def create_vector_store(documents, persist_directory = "chroma_db"):
    logger.debug("Creating vector store.")
    embeddings = OpenAIEmbeddings()
    vector_store = Chroma.from_documents(documents, embeddings, persist_directory = persist_directory)    
    return vector_store

# Retrieve relevant documents from vector store
def query_vector_store(query, vector_store : Chroma):
    logger.debug("Retrieving vector stores.")
    results = vector_store.similarity_search(query, k = 2)
    return_val = [result.page_content for result in results]
    logger.debug("Retrieved vector stores: " + "\n".join(return_val))
    return return_val