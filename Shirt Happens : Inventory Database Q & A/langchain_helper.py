from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate

from few_shots import few_shots

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env (especially OpenAI API key)


# Custom Embedding Function to align with Chroma's new API signature
class CustomEmbeddingFunction:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def embed_documents(self, input):
        # Ensure the embedding follows the expected input-output structure
        return self.embeddings.embed_documents(input)

    def embed_query(self, input):
        # Use the same embedding function for queries
        return self.embeddings.embed_query(input)


# Define the MySQL prompt manually
_mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, 
then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results 
using the LIMIT clause as per MySQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. 
Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that 
do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves 'today'."""

# Combine the MySQL prompt with the prompt suffix from Langchain
full_prompt = _mysql_prompt + PROMPT_SUFFIX


def get_few_shot_db_chain():
    db_user = "root"
    db_password = "Rohit%40123"
    db_host = "localhost"
    db_name = "shirthappens"

    # Connect to the SQL database
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)

    # Set up the LLM (OpenAI in this case)
    llm = OpenAI(openai_api_key=os.environ["api_key"], temperature=0.1)

    # Initialize HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    # Create a vectorized representation of the few-shot examples
    to_vectorize = [" ".join(str(value) if value is not None else "" for value in example.values()) for example in
                    few_shots]
    cleaned_few_shots = [{k: str(v) if v is not None else '' for k, v in example.items()} for example in few_shots]

    # Use the custom embedding function to ensure compatibility with Chroma
    custom_embeddings = CustomEmbeddingFunction(embeddings)

    # Create a Chroma vector store
    vectorstore = Chroma.from_texts(to_vectorize, custom_embeddings, metadatas=cleaned_few_shots)

    # Create an example selector using semantic similarity
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,  # Number of examples to retrieve based on similarity
    )

    # Define the example prompt template
    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    # Set up the few-shot prompt template using the example selector and prompt
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"]
    )

    # Create the SQLDatabaseChain using the LLM, database, and few-shot prompt
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    return chain


if __name__ == "__main__":
    chain = get_few_shot_db_chain()
    print(chain.invoke("How many black Marimekko t-shirts do we have?"))