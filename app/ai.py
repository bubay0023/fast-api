
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import AzureChatOpenAI,AzureOpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
import chromadb
import os

chroma_host = os.getenv("CHROMA_HOST", "localhost")

client = chromadb.HttpClient(host=chroma_host, port=8000)

embeddings = AzureOpenAIEmbeddings(
                model="text-embedding-3-large",         # base model name
                deployment="text-embedding-3-large",   # your Azure deployment name
                api_key="QWmiTX1DHDOFcYD2t091xAnGByAUGeV5gRPTKUKzZ6iSm9dBPrFoJQQJ99BHACYeBjFXJ3w3AAAAACOG03rg",        # Azure OpenAI key
                azure_endpoint="https://fristaifoundry01.cognitiveservices.azure.com/",
                api_version="2024-12-01-preview"                # check your Azure resource version
                )

vectorstore = Chroma(embedding_function=embeddings,collection_name="my_collection_AzureOpenAIEmbeddings",client=client)



prompt_template = """
        You are a helpful AI assistant. Your primary goal is to answer questions
        accurately based *only* on the provided context.

        If the answer cannot be found in the context, explicitly state:
        "I cannot find the answer to that question in the provided documents."
        Do not make up information. Keep answers concise and to the point.

        Context: {context}

        Question: {question}

        Answer:
        """
PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

retriever = vectorstore.as_retriever(search_kwargs={"k": 5}) 

llm = AzureChatOpenAI(
        api_key="AL9rC5qu4a0WamflSAC36c6DShVCyk29IV18V8mJWGPMf9HjhVG0JQQJ99BHACHYHv6XJ3w3AAAAACOG8GNr",     # Azure OpenAI Key
        azure_endpoint="https://bubay-mewfyz7m-eastus2.cognitiveservices.azure.com/",
        api_version="2025-01-01-preview",   
        azure_deployment="gpt-4.1",   
        model="gpt-4.1"               
        )

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT}
)


def apicall(question: str) -> None:
    """
    Asks a question to the chatbot and prints the generated answer.
    """
    try:
        response = qa_chain.invoke({"query": question})
        answer = response.get("result", "No answer generated.")
        return answer
    except Exception as e:
        return f"Error: {e}"
