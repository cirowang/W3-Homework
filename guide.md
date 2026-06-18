After-school homework

link:https://beebeeai.feishu.cn/docx/K1ZAdnPFdoYXARxHsdVcL35tnIV

Job Type: Performance Job Course: W301a RAG Core Principles + VRAG Advanced Architecture Job 

Description: The goal of this assignment is to help students translate the core principles of RAG in the W301a course into practical results that can be run, demonstrated, and explained. Participants need to understand the complete process of the RAG system from document loading, segmentation, vectorization, indexing, retrieval, rearrangement to answer generation, and further master how VRAG / multimodal RAG is applied in complex knowledge scenarios such as pictures, tables, PDF page screenshots, etc. 

Core tasks: 
    - Build a basic RAG MVP: support uploading or reading documents, splitting text into chunks, generating embeddings, and storing them in a vector database or local retrieval structure. 
    - Implement a complete question-answering process at once: after the user enters a question, the system is able to retrieve relevant content and generate answers based on the retrieval results. - Add at least one enhancement to the base RAG: such as Hybrid Search, Rerank, RAG Fusion, Query Decomposition, Metadata Filtering, Web Search as RAG, Image / Table Retrieval, etc. 
    - Record a Demo or provide screenshots showing the complete process from data import to the final Q&A. 
    
References: - W301a Course Materials: RAG Core Principles, Elasticsearch Vector Retrieval, PDF Processing, Hybrid Search, Rerank, RAG Fusion, Coreference Resolution, Query Decomposition, Metadata Filtering, Web Search as RAG, Image & Table Retrieval. 

Optional Direction / Choose One of Two: 

1. Direction A: Basic RAG system implementation 
    - Complete a minimal available text RAG system for students who want to lay a solid foundation in the RAG process. 
    - Supports reading at least 1 PDF, Markdown, TXT or web page text. 
    - Use text segmentation to split the document into chunks. 
    - Convert chunks to vectors using embedding model. 
    - Complete retrieval using Elasticsearch, Chroma, FAISS, Supabase Vector, Pinecone, or other vector storage schemes. 
    - After the user asks a question, the system is able to return the relevant snippet and generate an answer based on the snippet. 
    - The answer should try to reflect the source basis, such as file name, page number, chunk content or citation fragment. 
    - Suggest adding Hybrid Search, Rerank, Metadata Filtering or a simple review (3–5 questions). 

2. Direction B: VRAG / Advanced RAG Architecture Design and Demo 
    - Choose a real-world scenario, such as a corporate knowledge base, course Q&A, contract review, financial report analysis, product manual Q&A, medical / legal / educational material search, etc. 
    - Design a RAG architecture that supports complex materials and can contain text, images, tables, PDF page screenshots or web content. 
    - Demonstrate how the system handles at least one complex input, such as a PDF table, image text or illustration, a multi-file knowledge base, multiple rounds of follow-up questions, question disassembly, online search for supplementary information, etc. 
    - Implement or clearly design at least one advanced capability: RAG Fusion, Query Decomposition, Coreference Resolution, Hybrid Search + Rerank, Metadata Filtering, Image / Table Retrieval, Web Search as RAG, Multimodal Retrieval and Answering. 
    - Output an architectural documentation explaining data flow, module responsibilities, retrieval strategy, generation strategy, and evaluation methods. 
    - Suggested inclusion of system architecture diagrams, retrieval flowcharts, demo Q&A samples, success/failure case analysis, and discussion of accuracy, traceability, and hallucination risks. 

Completion criteria: 
    - Minimum completion requirement: Complete a runnable or clearly demonstrable RAG / VRAG job. The complete process of data entry, text or multimodal content processing, retrieval, and response generation must be demonstrated. Submit at least 1 Demo Q&A sample and indicate which RAG components the system uses. 
    - Recommended completion effect: The system does not just “answer”, but explains “why it answers this way”. It is recommended to present the retrieval results, chunk content, source information, rerank or fusion process, and do a simple result analysis of 3–5 test questions. Excellent assignments should reflect an understanding of the choices of RAG architecture, such as chunk size, overlay, embedding model, vector store, reranker, metadata, etc. 
    - Non-acceptance: Only screenshots are submitted but no explanation is given; only ChatGPT answers directly without any retrieval process; code or links are inaccessible; Demo cannot prove the use of RAG; only the final answer is shown but the data source is not shown; the system architecture is not explained; the job content is not related to the W301a topic. 
    
Estimated time: 3–6 hours 
    - Basic RAG MVP: approximately 3–4 hours 
    - VRAG / Advanced RAG Architecture Design and Demo: 

approximately 4–6 hours Submission: 
    - 1–3 minute screen recording Demo showing the complete process from data import and retrieval to generating answers. 
    - Link to the project code repository, or an accessible online Demo link. 
    - A short explanatory document that suggests the following: project objectives, data sources used, system architecture, RAG/VRAG process, models/vector libraries/key tools used, results of at least 3 test questions and answers, shortcomings of the current system, and optimizable directions. 
    - If you are unable to submit code, you must submit a complete screenshot, including data processing, retrieval results, final answers, and key configuration. 
    - Submit to the Feishu mission comment area; if submitting for a group, please state the group name and members. 

Submission deadline: June 20, 2026, 9:25 AM Beijing time / June 19, 2026, 9:25 PM Eastern time Reminder setting: 2 days before the deadline Review Schedule: Pacer reviews assignments within 24 hours of the deadline.

