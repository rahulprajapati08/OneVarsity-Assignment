from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate , PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
import validators
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
import tempfile
import os
from typing import Optional
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Init LLM
llm = OllamaLLM(model="mistral")



# Memory (in real-world, use database/vector DB)
vectorstore = None




@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile):
    global vectorstore
    
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # Load PDF
    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    # Split & embed
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Clean up temp file
    os.remove(tmp_path)

    return {"message": f"PDF uploaded and indexed successfully ({len(chunks)} chunks)."}

class QARequest(BaseModel):
    query: str

@app.post("/qa/")
async def query_doc(req: QARequest):
    global vectorstore
    prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Question:{input}
    """
)
    if not vectorstore:
        return {"error": "No document uploaded yet. Please upload first."}

    retriever = vectorstore.as_retriever()
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    response = retrieval_chain.invoke({'input': req.query})
    return {
        "answer": response['answer'],
        "context": [doc.page_content for doc in response['context']]
    }

@app.post("/summarize/")
async def summarize_pdf_or_text(
    file: Optional[UploadFile] = None,
    text: Optional[str] = Form(None)
):
    tmp_path = None
    try:
        docs = []

        # Case 1: PDF file upload
        if file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            loader = PyPDFLoader(tmp_path)
            docs = loader.load()

        # Case 2: Raw text from Streamlit
        elif text:
            docs = [Document(page_content=text)]

        else:
            return {"error": "Please provide either a PDF file or text input."}

        # Build the summarization chain
        summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = summary_chain.run(docs)

        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


class LearningPathRequest(BaseModel):
    goal: str
    current_skills: str
    timeframe: str
    weekly_hours: str

@app.post('/learning-path/')
async def dynamic_learning_path_suggestion(req: LearningPathRequest):
    template = """You are an AI mentor. Given a learning goal, design a clear and structured learning path. Break the path into stages, where each stage builds on the previous one. For each stage, include the key topics, skills to master, recommended resources (books, courses, websites, or tutorials), and practical exercises or projects. The learning path should be progressive, starting from the fundamentals and advancing toward mastery. Present the result in a structured format that is easy to follow.
    
    These are the following details you might need to design the path:
    *Goal*: {goal}
    *Current Skills*: {current_skills}
    *Timeframe*: {timeframe}
    *Weekly Hours*: {weekly_hours}
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["goal", "current_skills", "timeframe", "weekly_hours"]
    )

    try:
        chain = prompt | llm
        response = chain.invoke({
            'goal': req.goal,
            'current_skills': req.current_skills,
            'timeframe': req.timeframe,
            'weekly_hours': req.weekly_hours
        })

        # Ensure response is string
        if isinstance(response, dict) and "text" in response:
            response = response["text"]
        elif not isinstance(response, str):
            response = str(response)

        return {'Learning Path': response.strip()}
    except Exception as e:
        return {'error': str(e)}