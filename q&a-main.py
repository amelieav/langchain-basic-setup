from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from docx import Document
import pandas as pd
import io
import sys

# Ensure proper encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


"""helper functions"""

class DocumentPage:
    def __init__(self, content, metadata=None):
        self.page_content = content
        self.metadata = metadata if metadata is not None else {}

def read_docx(file_path):
    doc = Document(file_path)
    return [DocumentPage(para.text, {"paragraph": i}) for i, para in enumerate(doc.paragraphs) if para.text.strip() != '']

"""Load environment variables"""
load_dotenv()
api_key = os.getenv('API_KEY')

"""Initialize the ChatOpenAI model"""
llm = ChatOpenAI(openai_api_key=api_key)

"""Load the Excel file"""
excel_path = 'q&a spreadsheet.xlsx'  # Replace with your file path
df = pd.read_excel(excel_path)

# Prepare the embeddings and text splitter
embeddings = OpenAIEmbeddings(openai_api_key=api_key)
text_splitter = RecursiveCharacterTextSplitter()

# Prepare the prompt template
prompt_template = ChatPromptTemplate.from_template("""Answer the following question concisely based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

for index, row in df.iterrows():
    # Read the source document
    source_doc_path = f'resources/{row["Source"]}.docx'
    doc_pages = read_docx(source_doc_path)

    # Process the document
    documents = text_splitter.split_documents(doc_pages)
    vector = DocArrayInMemorySearch.from_documents(documents, embeddings)

    # Set up the document chain and retriever
    document_chain = create_stuff_documents_chain(llm, prompt_template)
    retriever = vector.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    # Generate the response
    input_query = {"input": row["Questions"]}
    response = retrieval_chain.invoke(input_query)

    # Store the answer in the DataFrame
    df.at[index, 'Answer'] = response["answer"]

# Save the updated DataFrame back to the Excel file
df.to_excel(excel_path, index=False)
