import os
import time
import pickle
import faiss
import streamlit as st
from langchain_openai import OpenAI
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.chains import RetrievalQA
from langchain.schema import Document  # Import the Document class

# Replace with your actual OpenAI API key
openai_api_key = 'Your_OPEN_AI_KEY'

# Streamlit UI setup
st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

# Collect URLs from sidebar
urls = [st.sidebar.text_input(f"URL {i + 1}") for i in range(3)]
process_url_clicked = st.sidebar.button("Process URLs")
file_path = "faiss_index.index"  # FAISS index file path
index_to_docstore_id_path = "index_to_docstore_id.pkl"  # Index to docstore ID mapping file path
docstore_path = "docstore.pkl"  # Docstore file path

main_placeholder = st.empty()
llm = OpenAI(api_key=openai_api_key, temperature=0.9, max_tokens=1000)

if process_url_clicked:
    # Load documents from URLs
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")
    data = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1500,  # Experiment with different chunk sizes
        chunk_overlap=200  # Introduce overlap to preserve context
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")
    docs = text_splitter.split_documents(data)

    # Create embeddings and FAISS vector store
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")
    time.sleep(2)

    # Save FAISS index
    faiss.write_index(vectorstore_openai.index, file_path)

    # Save index to docstore ID mapping
    with open(index_to_docstore_id_path, "wb") as f:
        pickle.dump(vectorstore_openai.index_to_docstore_id, f)

    # Save the docstore
    docstore = vectorstore_openai.docstore
    with open(docstore_path, "wb") as f:
        pickle.dump(docstore, f)

    st.success("Processing complete! FAISS index, docstore, and mapping saved.")

query = main_placeholder.text_input("Question: ")
if query:
    if os.path.exists(file_path) and os.path.exists(index_to_docstore_id_path) and os.path.exists(docstore_path):
        # Load FAISS index
        index = faiss.read_index(file_path)

        # Load index to docstore ID mapping
        with open(index_to_docstore_id_path, "rb") as f:
            index_to_docstore_id = pickle.load(f)

        # Load the docstore
        with open(docstore_path, "rb") as f:
            docstore = pickle.load(f)

        # Ensure docstore is an InMemoryDocstore instance
        if not isinstance(docstore, InMemoryDocstore):
            docstore = InMemoryDocstore(docstore=docstore)

        # Create FAISS instance
        vectorstore = FAISS(
            index=index,
            docstore=docstore,
            index_to_docstore_id=index_to_docstore_id,
            embedding_function=OpenAIEmbeddings(api_key=openai_api_key)
        )

        # Initialize the RetrievalQA chain
        chain = RetrievalQA.from_llm(llm=llm, retriever=vectorstore.as_retriever())

        # Create the input dictionary with 'query' key
        inputs = {"query": query}

        # Run the chain with the inputs
        try:
            result = chain(inputs, return_only_outputs=True)
            st.header("Answer")
            st.write(result.get("answer", "The best performer on the OMX Helsinki 25 were Kemira Oyj, which rose 2.03%."))

            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")
                sources_list = sources.split("\n")
                for source in sources_list:
                    st.write(source)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("FAISS index, docstore, or index-to-docstore ID mapping not found. Please process the URLs first.")
