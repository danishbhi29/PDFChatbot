# PDF Chatbot

A full-stack RAG-based PDF chatbot that lets users upload a PDF and ask questions about its content. The backend processes the uploaded PDF, splits it into chunks, and uses Google Gemini through LangChain to generate answers from the document context. The frontend provides a simple React interface for uploading files and chatting with the document.

## Features

- Upload and process PDF files
- Ask questions based on the uploaded PDF content
- FastAPI backend with LangChain document processing
- Google Gemini LLM integration
- React + Vite frontend
- Axios-based API communication
- Local runtime storage for uploaded PDFs

## Tech Stack

**Frontend**

- React
- Vite
- Axios
- CSS

**Backend**

- Python
- FastAPI
- LangChain
- Google Gemini
- PyPDF
- Uvicorn

## Project Structure

```text
RAG PDF Chatbot/
├── Backend/
│   ├── app/
│   │   ├── main.py
│   │   └── uploads/
│   ├── requirements.txt
│   └── .env
├── Frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10+
- Node.js 18+
- npm
- Google Gemini API key

## Backend Setup

Go to the backend folder:

```bash
cd Backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `Backend` folder:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

## Frontend Setup

Open a new terminal and go to the frontend folder:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

Start the frontend development server:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

## How To Use

1. Start the backend server.
2. Start the frontend server.
3. Open the frontend in your browser.
4. Upload a PDF file.
5. Ask questions related to the uploaded PDF.

## API Endpoints

### Upload PDF

```http
POST /upload
```

Uploads and processes a PDF file.

### Chat

```http
POST /chat
```

Sends a question and returns an answer based on the uploaded PDF content.

## Environment Variables

| Variable | Description |
| --- | --- |
| `GOOGLE_API_KEY` | Google Gemini API key used by LangChain |

## Git Ignore Notes

This project ignores local dependencies, environment variables, uploaded files, generated vector databases, build output, logs, and cache files. These files should not be pushed to GitHub.

## License

This project is for learning and development purposes.
