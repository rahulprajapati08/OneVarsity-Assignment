# AI Microservices Assignment - OneVarsity

This project implements modular **AI microservices** using **FastAPI**, **LangChain**.  
It provides three core functionalities:  

1. **Document Summarization** (from text or PDF)  
2. **Question Answering (QA) over documents**  
3. **Dynamic Learning Path Suggestion**  

A simple **Streamlit frontend** is also developed to interact with these APIs.

---

## 🚀 Features

- **Summarization API** → Summarizes PDFs or raw text.  
- **Q&A API** → Ask questions about uploaded documents.  
- **Learning Path API** → Suggests a learning path based on user’s input (domain, skill level, and goals).  
- **Frontend** → Built with **Streamlit** to provide a clean user interface.  

---

## 🛠️ Tech Stack

- **Backend** → FastAPI, LangChain  
- **Embeddings** → HuggingFace (`all-MiniLM-L6-v2`) + FAISS for vector storage  
- **LLM** → Local LLM (default). You can also integrate with external LLM APIs (like OpenAI or HuggingFace Hub).  
- **Frontend** → Streamlit  

---



## ⚙️ Setup Instructions

1. **Clone this repo:**
   ```bash
    git clone https://github.com/rahulprajapati08/OneVarsity-Assignment.git
    cd OneVarsity-Assignment

2. Create a virtual environment & install dependencies
   ```bash
    python -m venv venv
    source venv/bin/activate   # (Linux/Mac)
    venv\Scripts\activate      # (Windows)
        
    pip install -r requirements.txt

3. Run FastAPI backend
   ```bash
   cd backend
   uvicorn main:app --reload
4. Run Streamlit frontend
   ```bash
   cd frontend
   streamlit run app.py

---

## 📸 Screenshots
- Q&A over documents
  <img width="1920" height="1020" alt="Screenshot 2025-08-28 201109" src="https://github.com/user-attachments/assets/b2409122-00e4-4c1c-aeb3-f2a6de175b69" />
  <img width="1920" height="1020" alt="Screenshot 2025-08-28 201208" src="https://github.com/user-attachments/assets/c596cb11-3659-4400-98b0-4b66aa2aee8d" />
- Text summarization
  <img width="1920" height="1020" alt="Screenshot 2025-08-28 201243" src="https://github.com/user-attachments/assets/7e444a71-159e-4c21-9819-14b200e91f1e" />
  <img width="1920" height="1020" alt="Screenshot 2025-08-28 201536" src="https://github.com/user-attachments/assets/5b6a5496-fe6a-4e44-afe5-96cf4818b9b2" />

- Dynamic learning path suggestion
  <img width="1920" height="1020" alt="Screenshot 2025-08-28 175926" src="https://github.com/user-attachments/assets/3e8a383d-b64f-4d12-ba0e-dc1d4709fccf" />
  <img width="1920" height="1020" alt="Screenshot 2025-08-28 175908" src="https://github.com/user-attachments/assets/c4da2718-20fb-440a-87ca-7b83046ca70e" />

---

## 🔄 Using Local LLM vs External API
Currently, this project uses a local LLM for processing.
If you want to switch to OpenAI API or HuggingFace Hub, update the LLM initialization in main.py:
1. Example: Using OpenAI GPT
   ```bash
   from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY")
    )
2. Example: Using HuggingFace Hub
   ```bash
    from langchain_huggingface import HuggingFaceEndpoint
    
    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-base",
        huggingfacehub_api_token=os.getenv("HF_TOKEN")
    )

---
## 🧪 Testing with Postman

A Postman collection is included in this repository for easy testing of all the API endpoints.

- File: `OneVarsity.postman_collection.json`
- Location: [Postman Collection on GitHub](./OneVarsity.postman_collection.json)

### How to Use:
1. Download the `.postman_collection.json` file.
2. Open Postman → Import → Choose the file.
3. Test endpoints:
   - `/upload_pdf/` → Upload a PDF file.
   - `/qa/` → Send a JSON body with `{ "query": "your question" }`.
   - `/summarize/` → Upload a PDF or raw text for summarization.
   - `/learning_path/` → Send skills,goals,timeframe and weekly hours in the request body.

---
## 👨‍💻 Author

Rahul Prajapati



 
