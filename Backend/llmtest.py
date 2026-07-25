from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize the Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Invoke the model
response = llm.invoke("Who is Quaid-e-Azam?")

# Print only the text response
print(response.content)