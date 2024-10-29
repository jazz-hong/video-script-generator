import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langfuse import Langfuse

load_dotenv()

# Initialize Langfuse client (prompt management)
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST_URL"),
)

def generate_script(subject, video_length, creativity, api_key):

    model = ChatGroq(api_key=api_key, temperature=creativity)
    
    title_checker_prompt = langfuse.get_prompt("title-chat", label="latest", type="chat")
    title_checker_prompt_langchain = ChatPromptTemplate.from_messages(title_checker_prompt.get_langchain_prompt())
    # LCEL chain (Same as how you created using chain as usual)
    title_chain = title_checker_prompt_langchain | model
    
    script_generator_prompt = langfuse.get_prompt("video-script-chat", label="latest", type="chat")
    script_generator_prompt_langchain = ChatPromptTemplate.from_messages(script_generator_prompt.get_langchain_prompt())
    # LCEL chain (Same as how you created using chain as usual)
    script_chain = script_generator_prompt_langchain | model

    # We use .content, so we get only the content, and no other useless sentence
    title = title_chain.invoke({"subject": subject}).content

    # We take in WikipediaAPI (search engine)
    search = WikipediaAPIWrapper(lang="en") 
    search_result = search.run(subject)

    video_script = script_chain.invoke({"title": title, "duration": video_length,
                                  "wikipedia_search": search_result}).content

    # Once every information fulfilled, video generator outputs only these 3
    return search_result, title, video_script

# ---------- TESTING ----------
print(generate_script("llama模型", 1, 0.7, os.getenv("GROQ_API_KEY")))
# ---------- TESTING ----------