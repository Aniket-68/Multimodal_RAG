# Multimodal RAG Explorer

A production-grade **Multimodal Retrieval-Augmented Generation (RAG)** system built from scratch to maintain modularity, extensibility, and clean architectural boundaries.

---

## 🗺️ Project Roadmap

The system is divided into five major phases. Currently, the project is focusing on **Phase 1**.

| Phase | Objective | Deliverable | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | **Document Ingestion & Understanding** | PDF → Structured Document | 🔄 In Progress |
| **Phase 2** | **Knowledge Representation** | Chunks → Embeddings → Vector Database | ⏳ Planned |
| **Phase 3** | **Retrieval Engine** | Semantic Search & Hybrid Retrieval | ⏳ Planned |
| **Phase 4** | **Multimodal Intelligence** | Images, Tables, OCR, Vision Models | ⏳ Planned |
| **Phase 5** | **Production RAG** | APIs, LLM, Chat UI, Deployment, Evaluation | ⏳ Planned |

---

## 🏗️ Phase 1 — Document Ingestion & Understanding

The goal of Phase 1 is to transform an unstructured PDF into a **Structured Document** representation that can later be indexed and retrieved.

### Why is Phase 1 Necessary?
Large Language Models (LLMs) cannot process PDF binaries directly. Before downstream tasks (like chunking and vector storage) can begin, we must extract:
- **Text & Metadata** (structure, coordinates, and tags)
- **Reading Order & Layout** (distinguishing headings, body, headers, footers)
- **Images & Embedded Media**
- **Tables** (capturing structural grid relationships)

```
                     data/raw
                         │
                         ▼
                Document Scanner
                         │
                         ▼
                  Loader Factory
                         │
               ┌─────────┴──────────┐
               ▼                    ▼
          PDF Loader           DOCX Loader
               │
               ▼
          Native Document (fitz.Document)
                │
                ▼
           Parser Factory
                │
                ▼
            PDFParser (Orchestrator)
                │
   ┌────────────┼────────────┬────────────┐
   ▼            ▼            ▼            ▼
Text       Image        Table      Metadata
Extractor  Extractor    Extractor  Extractor
   │            │            │            │
   └────────────┼────────────┴────────────┘
                ▼
         Layout Analyzer
                │
                ▼
        StructuredDocument
```

### Why Introduce the Extractor Layer?

To adhere to the **Single Responsibility Principle (SRP)** and make the codebase modular and testable, we decouple the extraction logic from the parsing orchestrator:

1. **Orchestration vs. Extraction**: The `PDFParser` acts purely as an orchestrator. It manages the document lifecycle (opening the file, iterating over pages) but delegates the actual work of parsing page elements to specialized extractors.
2. **Strict Internal Schemas**: Extractors do not return raw PyMuPDF objects or simple primitive types (like raw strings). They return our own strongly-typed models (e.g., `Block`, `PageMetadata`), ensuring all downstream RAG components are entirely isolated from third-party library internals.
3. **Granular Extractor Definitions**:
   - **`TextExtractor`**: Takes a native page object (`fitz.Page`) and extracts raw text blocks, returning `List[Block]`. It does not perform layout analysis, OCR, or save images.
   - **`MetadataExtractor`**: Extracts Page-level metadata fields into a structured `PageMetadata` model:
     - `page_number`: 1-based index
     - `width` / `height` / `rotation`
     - Boolean flags: `has_text`, `has_images`, `has_links`
   - **`ImageExtractor`**: Focuses on extracting image bytes, saving image assets locally, and compiling coordinate & bounding box metadata. This acts as a foundation for Phase 4 where images are sent to Vision-Language Models (VLMs) for captioning.
   - **`TableExtractor`**: Focuses solely on tabular boundaries and cell structures.
4. **Text-First Dependency**: Text is the critical path for downstream RAG tasks (chunking, embeddings, retrieval). Isolating the `TextExtractor` allows us to implement, test, and run the core pipeline first, incrementally adding images and tables later as additional context.

---

## 🛠️ Project Structure

```text
backend/
├── app/
│   ├── api/             # API Router and Endpoints
│   ├── ingestion/       # Ingestion and preprocessing pipeline
│   │   ├── loaders/     # File loaders returning native doc objects
│   │   ├── parsers/     # Base/orchestrator parsers
│   │   └── extractors/  # Isolated data extractors (Text, Image, Table, Metadata)
│   ├── models/          # Pydantic schemas (document, metadata blocks)
│   └── services/        # Orchestration services
└── frontend/            # React & Vite application with glassmorphism UI
```


---

## 📐 Design Principles

- **Clean Architecture & SOLID Principles**: Each layer has a single, isolated responsibility.
- **Interface-Driven Design**: The loader and parser layers use Abstract Base Classes (`BaseLoader`, `BaseParser`) to allow polymorphic implementations.
- **Factory & Strategy Patterns**: Document loaders are dynamically resolved via a `LoaderFactory` based on extension, enabling easy support for new formats (e.g., `.docx`, `.pptx`) without altering core routing logic.
- **Encapsulated Schema**: External libraries (like PyMuPDF) are never exposed beyond the parsing boundary. Downstream tasks operate strictly on `StructuredDocument` models.

---

## 📦 Backend Stack (Phase 1 Dependencies)

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

## 🚀 Getting Started

### Backend
1. Initialize your Python environment (e.g., using `venv` or `conda`).
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the local development server:
   ```bash
   npm run dev
   ```
