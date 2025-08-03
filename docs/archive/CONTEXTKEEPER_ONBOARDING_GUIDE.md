# Welcome to ContextKeeper: A Developer's Onboarding Guide
This guide provides a comprehensive, step-by-step explanation of the ContextKeeper workflow. By the end of this document, you will understand the complete data lifecycle, from how a project's source code is first added and processed to how your questions are answered with rich, relevant context.
---
### Phase 1: Onboarding a New Project—From Code to Context
Your first step is to introduce your codebase to the system. This initial phase is all about creating a new, isolated space for your project and then feeding its source code into ContextKeeper for the first time.
#### 1. Creating a New Project
Everything starts with telling ContextKeeper about your project. This is handled by a core component called the **`ProjectManager`**, which acts as the librarian for all the different codebases ContextKeeper knows about.
*   **The `create_project` Command**: You'll start by running a command that calls the `create_project` function. You'll provide a name for your project and the file path to its root directory.
*   **A Unique Identity**: The `ProjectManager` then generates a unique identifier for your project (a `project_id`). This ID ensures that your project's knowledge is kept completely separate from others.
*   **Configuration File**: A configuration file (a `.json` file) is created in your home directory (`~/.rag_projects/`). This file acts as the project's birth certificate, storing its name, ID, file path, and current status (which starts as `ACTIVE`).
At this point, your project officially exists in ContextKeeper, but the system doesn't know anything about the code inside it yet.
#### 2. The First Read-Through: Code Ingestion
Next, you'll kick off the **ingestion process**. Think of this as ContextKeeper reading your entire codebase for the first time. This is managed by the central orchestrator of the system, the **`ProjectKnowledgeAgent`**.
*   **Walking the Directory Tree**: The `ingest_directory` function systematically walks through every file and folder within your project's root path.
*   **Intelligent Filtering**: As it encounters each file, it asks a critical question: "Should I read this?" This is where the **`PathFilter`** comes in. It's configured with a set of rules to ignore things that don't contain useful context, such as:
    *   **Dependency Folders**: `node_modules`, `venv`
    *   **Build Output**: `build`, `dist`
    *   **Git History**: `.git`
    *   **Configuration and Lock Files**: `.env`, `package-lock.json`
This step is vital for keeping the knowledge base clean and focused only on your source code.
#### 3. Detecting Changes and Ensuring Security
For every file that passes the filter, two more checks happen:
*   **Change Detection**: Has this file been seen before, and has it changed? The `ingest_file` function calculates a unique signature (an MD5 hash) of the file's content. It compares this signature to a stored record. If they match, the file is skipped, making future updates much faster.
*   **Security Screening**: If the file is new or has been modified, its contents are read and passed to the **`SecurityFilter`**. This component acts as a security guard, using regular expressions to find and automatically redact sensitive information like API keys, passwords, or secret tokens. Any secrets found are replaced with `[REDACTED]`.
After this phase, ContextKeeper has a clean, secure, and relevant set of source code files ready for the next step: breaking them down into meaningful pieces to be indexed.
---
### Phase 2: The Indexing Pipeline—Turning Code into Searchable Knowledge
With the source code read and cleaned, the next step is to transform it into a format that enables intelligent, semantic search. This is the core of the Retrieval-Augmented Generation (RAG) system. It involves breaking the code into smaller pieces, converting those pieces into a numerical format, and storing them in a specialized database.
#### 1. Intelligent Code Chunking
A single source file can be thousands of lines long—too large to be useful as a single piece of context. The code must be broken down into smaller, meaningful segments. This is the job of the **`TextChunker`**.
*   **Semantic Boundaries**: Instead of just splitting files every `N` lines, the chunker uses a more intelligent approach. The `_chunk_by_structure` method looks for logical boundaries in the code, such as the start of a function (`def`, `function`), a class, or a major component (`export const`). This ensures that the resulting chunks are self-contained and semantically coherent.
*   **Size and Overlap**: Each chunk is still constrained by a maximum size (e.g., 1000 tokens). To avoid losing context at the edges of a chunk, a small amount of overlap is included. The last few lines of one chunk become the first few lines of the next.
*   **Metadata is Key**: For every chunk created, crucial metadata is attached, including the original `file_path`, the `start_line` and `end_line` numbers, and the `type` of content (e.g., `code`).
#### 2. Generating Vector Embeddings
This is where the magic happens. Each chunk of text is converted into a **vector embedding**—a long list of numbers that represents the semantic meaning of the text.
*   **The Embedding Model**: ContextKeeper uses Google's `text-embedding-004` model to convert a text chunk into its corresponding vector embedding.
*   **A Numerical Representation of Meaning**: Think of this vector as a coordinate in a high-dimensional "meaning space." Code that implements user authentication will be located in one neighborhood of this space, while code related to database connections will be in another.
#### 3. Storing in the Vector Database
Once the chunks are converted into vectors, they are stored in **ChromaDB**, a specialized vector database.
*   **Project-Specific Collections**: A dedicated "collection" is created for each project (e.g., `project_<project_id>`). This guarantees **project isolation**—a query for one project will *never* see results from another.
*   **Storing Vectors and Metadata**: For each chunk, the system stores its unique `id`, the vector embedding, and the rich metadata from the chunking phase.
At the end of this pipeline, the project's knowledge base is fully indexed and ready to be queried.
---
### Phase 3: The Query and Retrieval Process—Finding the Right Context
This phase is about taking a user's question in plain English, understanding its intent, and finding the most relevant pieces of code or documentation from the knowledge base.
#### 1. The User's Question
A user asks a question, such as "How do we handle user authentication?", and provides the `project_id` to ensure the query is run in the correct context.
#### 2. Converting the Question into a Vector
The system uses the same Google GenAI embedding model to convert the text of the question into a query vector. This vector represents the semantic meaning of the user's question in the same "meaning space" where the code chunks live.
#### 3. The Similarity Search
*   **Targeting the Right Collection**: The query is executed *only* against the ChromaDB collection that matches the `project_id`.
*   **Nearest Neighbor Search**: ChromaDB performs a **similarity search**, calculating the distance between the query vector and all the chunk vectors in the collection.
*   **Top-K Results**: The search returns the "top-K" most similar results (e.g., the top 10 closest chunks).
The output is a ranked list of the most relevant code chunks, each with its content, metadata, and a distance score.
---
### Phase 4: Answer Synthesis and Generation—Creating a Coherent Response
The final step is to synthesize the retrieved context into a single, easy-to-understand answer.
#### 1. Preparing the Context for the Language Model
The `query_with_llm` function takes the top results from the search and prepares them for the Large Language Model (LLM).
*   **Consolidating the Context**: The `content` from each of the retrieved chunks is joined together into a single block of text.
*   **Compiling the Sources**: The `metadata` is used to create a list of the source files, which will be presented alongside the final answer for transparency.
#### 2. Prompt Engineering: Instructing the LLM
The system constructs a carefully crafted **prompt** to guide the model's behavior. This prompt instructs the LLM to answer the user's question based **solely on the provided context**. This technique, known as **grounding**, significantly reduces the risk of the model making up incorrect information.
#### 3. Generating the Final Answer
The complete prompt is sent to the Google Gemini model. The LLM reads the instructions, the question, and the code snippets, and then synthesizes all of this information to generate a final, natural-language answer. The final output is a complete package containing the answer and the list of sources.
---
### Phase 5: The Sacred Layer—Enforcing Architectural Integrity
The **Sacred Layer** allows a team to establish "sacred plans"—immutable documents that define the core architectural principles for a project.
#### 1. Creating and Approving a Sacred Plan
*   **Drafting**: An architectural document is created and introduced to the system as a `DRAFT` plan.
*   **Two-Layer Approval**: To become `APPROVED`, the plan must pass a strict verification process involving a unique verification code and a secret approval key.
*   **Immutable Storage**: Once approved, the plan is indexed and stored in a **separate, isolated ChromaDB collection** (e.g., `sacred_<project_id>`). It can no longer be changed.
#### 2. Querying and Drift Detection
*   **Authoritative Answers**: The Sacred Layer can be queried to get authoritative answers about the project's architecture.
*   **Drift Detection**: The **`SacredDriftDetector`** compares recent code changes (tracked via the **`GitActivityTracker`**) against the approved sacred plans. If the new code is semantically "drifting" away from the established architecture, the system can flag it, allowing teams to catch architectural deviations early.
This transforms ContextKeeper from a passive knowledge base into an active guardian of architectural integrity.