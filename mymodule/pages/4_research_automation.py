import streamlit as st
from dotenv import load_dotenv
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chat_models.openai import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers.web_research import WebResearchRetriever
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.vectorstores import Chroma
from streamlit_chat import message

__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

load_dotenv()


@st.cache_resource
def load_chain():
    # Vectorstore
    vectorstore = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory="./chroma_db_oai")

    # LLM
    llm_for_search = ChatOpenAI(model="gpt-3.5-turbo-16k")
    llm = ChatOpenAI()

    # Search
    search = GoogleSearchAPIWrapper()
    web_research_retriever: WebResearchRetriever = WebResearchRetriever.from_llm(vectorstore=vectorstore, llm=llm_for_search, search=search)

    qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=web_research_retriever)
    return qa_chain


# streamlit part
st.header("Research Automation Chat")

# show explain this is simple chat using LLMChain
st.write("this is the qa chat using google search api")

chain = load_chain()

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


with st.form(key="form", clear_on_submit=True):
    user_input: str = st.text_area("You: ", "", key="input_text", placeholder="please type here")
    submit: bool = st.form_submit_button("Submit")


if submit:
    output: str = chain({"question": user_input})

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i])
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
