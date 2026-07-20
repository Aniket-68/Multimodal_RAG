# Multimodal RAG Explorer

A state-of-the-art Multimodal Retrieval-Augmented Generation (RAG) system with a high-performance Python FastAPI backend and a responsive, glassmorphism-themed React & Vite frontend.

## Backend Architecture & Packages (Phase 1)

Below is the structured list of packages used in the backend for processing, OCR, layout extraction, web serving, and testing:

| Package | Purpose | Phase |
| :--- | :--- | :--- |
| **FastAPI** | REST API framework for high performance web endpoints | 1 |
| **Uvicorn** | ASGI web server execution for hosting the FastAPI app | 1 |
| **python-multipart** | Streaming support for multipart/form-data PDF file uploads | 1 |
| **PyMuPDF** | Rapid PDF parsing, page rendering, and embedded image extraction | 1 |
| **Docling** | Document layout analysis, structural zoning, and schema-based document conversion | 1 |
| **pymupdf4llm** | Specialized text extraction targeting LLM-friendly Markdown format | 1 |
| **PaddleOCR** | Optical Character Recognition for scanned images and non-selectable text PDFs | 1 |
| **Pillow** | Image processing library for reading, saving, and editing page assets | 1 |
| **OpenCV** | Computer vision preprocessing (denoising, binarization, rotation correction) | 1 |
| **NumPy** | High-performance array structures for pixel data and coordinate math | 1 |
| **Pandas** | Tabular data extraction, dataframes, and structured table manipulation | 1 |
| **Loguru** | Structured, clean logging with customizable formats and automatic rotation | 1 |
| **orjson** | Fast, binary-driven JSON serialization and deserialization | 1 |
| **httpx** | Async HTTP client for external service integration and API calls | 1 |
| **pytest** | Unit testing, test harness execution, and automation checks | 1 |

---

## Getting Started

### Backend
1. Initialize python environment (e.g. `venv` or `conda`).
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

### Frontend
1. Install node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Run Vite local dev server:
   ```bash
   npm run dev
   ```
