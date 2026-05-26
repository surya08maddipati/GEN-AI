# AI Resume Screener

An intelligent resume screening application built with Streamlit and Gemini AI that analyzes resumes against job descriptions and stores them in a vector database for intelligent searching.

## Features

- 📄 **Resume Upload**: Support for PDF, DOCX, and TXT formats
- 🤖 **AI Analysis**: Powered by Google Gemini AI for intelligent resume analysis
- 🔍 **Smart Search**: Self-query retriever with semantic understanding
- 💾 **Vector Storage**: ChromaDB for efficient resume embedding and retrieval
- 🎯 **Job Matching**: Match resumes against job descriptions

## Prerequisites

- Python 3.11 or higher
- Google Gemini API Key

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/surya08maddipati/GEN-AI.git
cd GEN-AI
```

### 2. Create a virtual environment (Optional but recommended)
```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On macOS/Linux
```

### 3. Install dependencies
```bash
py -3.11 -m pip install -r requirements.txt
```

Or install individually:
```bash
py -3.11 -m pip install langchain
py -3.11 -m pip install chromadb
py -3.11 -m pip install streamlit
py -3.11 -m pip install google-generativeai
py -3.11 -m pip install sentence-transformers
```

## Configuration

### Set up your environment variables

Create a `.env` file in the project root and add your Google Gemini API key:

```
GOOGLE_API_KEY=your_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Steps to use:
1. **Paste Job Description** - Enter the job requirements in the text area
2. **Upload Resume** - Upload a resume file (PDF, DOCX, or TXT)
3. **Analyze & Store** - Click the button to analyze and store the resume
4. **Search** - Use the search functionality to find relevant resumes

## Project Structure

```
.
├── app.py                  # Main Streamlit application
├── resume_processor.py     # Resume processing logic
├── requirements.txt        # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Dependencies

- **langchain** - LLM framework and document processing
- **chromadb** - Vector database for embeddings
- **streamlit** - Web UI framework
- **google-generativeai** - Google Gemini API
- **sentence-transformers** - Embedding models
- **python-dotenv** - Environment variable management
- **PyPDF2** - PDF processing
- **python-docx** - DOCX file processing

## Technologies Used

- **LLM**: Google Gemini AI
- **Vector Store**: ChromaDB
- **Embeddings**: Hugging Face Sentence Transformers
- **Framework**: Streamlit
- **Language**: Python 3.11

## License

This project is open source and available under the MIT License.

## Author

Surya (surya08maddipati)

## Support

For issues or questions, please open an issue on GitHub.
