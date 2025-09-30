from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model='gpt-4', temperature=0.2, max_completion_tokens=20)

result = model.invoke("who is PM of india in 2016?")

print(result.content)