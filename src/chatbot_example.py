from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("⚠️ No API key found. Please set GROQ_API_KEY in your .env file.")

# Use a current Groq model
llm = ChatOpenAI(
    model="llama-3.1-8b-instant",    # ✅ supported Groq model
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Create prompt
prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Q: {question}")

# New style: prompt | llm (instead of LLMChain)
chain = prompt | llm

# Test run
response = chain.invoke({"question": "Hello! Can you give me 3 study tips for programmers?"})
print(response.content)




