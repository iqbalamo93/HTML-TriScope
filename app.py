import os
import shutil
import streamlit as st
import pickle

import langchain
from langchain import OpenAI

from typing import List

# import langchain_openai.OpenAIEmbeddings

from langchain.chains import RetrievalQAWithSourcesChain

from langchain.text_splitter import RecursiveCharacterTextSplitter

from  langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma, Pinecone, FAISS


from langchain_community.document_loaders import AsyncHtmlLoader





if 'vectordb_exists' not in st.session_state:
    st.session_state['vectordb_exists'] = False

splitter = RecursiveCharacterTextSplitter(
    separators=['\n\n', '\n', '.', ',',' '],
    chunk_size=1000,
    chunk_overlap=250
)


def doc_processor(url: List):
    loader = AsyncHtmlLoader(url)
    data = loader.load()
    docs = splitter.split_documents(data)
    return docs

example_url = "https://www.nasa.gov/image-article/galaxy-next-door/"
example_2 = 'https://www.nasa.gov/image-article/25-years-ago-the-first-pieces-of-the-international-space-station/'
example_3 = 'https://www.nasa.gov/image-article/pioneer-10-crosses-the-asteroid-belt/'
# Folder name
vector_index_path = 'vector_index'


st.header('HTML TriScope: Rapid Answers from Triple Web Sources')
main_placeholder = st.empty()
# Input for OpenAI key
openai_key = st.text_input("Enter your OpenAI API Key and then goto sidebar", type="password")


if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key   
    llm = OpenAI(temperature=0.9, max_tokens=500)
    embeddings = OpenAIEmbeddings()


urls = []
with st.sidebar:
    st.title("Enter links Below ")

    url_key = 'input_url_1'
    question_key = 'input_question'
    
    input_1 = st.text_input(label='Link 1',value=example_url)
    urls.append(input_1)

    input_2 = st.text_input(label='Link 2',value=example_2)
    urls.append(input_2)

    input_3 = st.text_input(label='Link 3',value=example_3)
    urls.append(input_3)

    process_url_clicked = st.button('Process...')


    if process_url_clicked:
        main_placeholder.text("Data Loading...Started...✅✅✅")
        urls = [item for item in urls if item.strip()]
        docs = doc_processor(urls)

        main_placeholder.text("Embedding Vector Started Building...✅✅✅")
        if os.path.exists(vector_index_path):
            shutil.rmtree(vector_index_path)
            main_placeholder.text("Old data cleaned...✅✅✅")
        
        vector_index = FAISS.from_documents(docs, embeddings)
        vector_index.save_local('vector_index')

        st.session_state['vectordb_exists'] = True
        main_placeholder.text("Embedding Vector done Ask your question now...🔮🔮🔮")



state = st.session_state['vectordb_exists']
default_question = 'How far is Andromeda galaxy? '
query = st.text_input("Question: ",disabled=not state,value=default_question)

Get_Answer = st.button('Answer Me...',disabled=not state)

if Get_Answer and state:
    if query:

        vector_index = FAISS.load_local("vector_index",embeddings)

        chain = RetrievalQAWithSourcesChain.from_llm(llm=llm,retriever=vector_index.as_retriever())

        result = chain({"question": query}, return_only_outputs=True)
        st.header("Answer")
        st.write(result["answer"])
        
        sources = result.get("sources", "")

        if sources:
            st.subheader("Sources:")
            sources_list = sources.split("\n")  # Split the sources by newline
            for source in sources_list:
                st.write(source)

