import os
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser    
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

def get_llm(model: str = "liquid/lfm-2.5-2.6b:free", temperature: float = 0):
    api_key = os.getenv("OPENROUTER_API_KEY")
    return ChatOpenRouter(
        model=model,
        temperature=temperature,
        api_key=api_key
    )

def build_search_agent(llm=None):
    model = llm or get_llm()
    return create_agent(
        model=model,
        tools=[web_search],
    )

def build_scrape_agent(llm=None):
    model = llm or get_llm()
    return create_agent(
        model=model,
        tools=[scrape_url],
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that writes content based on the provided information."),
    ("human", """Write a detailed article based on the following information.
Topic: {topic}

Research Gathered: {research}

Structure the report as follows:
1. Introduction 
2.main body
3. Conclusion 

Be detailed and provide examples where applicable. Ensure the content is well-organized and easy to read. Avoid plagiarism and ensure the content is original."""),
])

def get_writer_chain(llm=None):
    model = llm or get_llm()
    return writer_prompt | model | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that critiques and improves content based on the provided information."),
    ("human", """Critique and improve the following article based on the provided information.
Report: {report}

Respond with a detailed critique, highlighting areas for improvement, and provide suggestions for enhancing the content. Ensure the critique is constructive and specific, focusing on clarity, coherence, and overall quality of the article."""),
])

def get_critic_chain(llm=None):
    model = llm or get_llm()
    return critic_prompt | model | StrOutputParser()

# Dynamic chain wrappers for seamless backward compatibility
class _DynamicChain:
    def __init__(self, chain_factory):
        self._factory = chain_factory

    def invoke(self, *args, **kwargs):
        return self._factory().invoke(*args, **kwargs)

writer_chain = _DynamicChain(get_writer_chain)
critic_chain = _DynamicChain(get_critic_chain)
