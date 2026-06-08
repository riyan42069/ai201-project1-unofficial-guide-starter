# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Domain: Student reviews and experiential knowledge about Computer Science & Engineering (CSCE) professors and courses at the University of North Texas (Denton, TX)

Why this knowledge valuavble and hard to find through official channels: Th UNT official channels only tells us about the course catalog, department website and registration system. It also mentions the course availability and the instructor assigned to the class. These information doesn't help the student understand the abilities of an instructor. It tells nothing about whether the professor explains things clearly, exam's leniency, and more importantly the student reviews. All these information can be found in Rate My Professor, r/UNT reddit threads. All these information can be hard to find and analyze to choose the right class.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate My Professor - Jonathon Doran | 83 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/1579301 |
| 2 |Rate My Professor - Curtis Chambers |42 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/2174155 |
| 3 |Rate My Professor - John Curtis |29 ratings UNT Kinesiology professor |https://www.ratemyprofessors.com/professor/1707713 |
| 4 |Rate My Professor - Pradhumna Shrestha |44 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/2174392 |
| 5 |Rate My Professor - Bahareh Dorri |22 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2936044 |
| 6 |Rate My Professor - David Keathly |74 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/702560 |
| 7 |UNT course info - Foundations of Cybersecurity|Official course description, prerequisites, policies, grading structure, and credit hours|https://s3.amazonaws.com/mirror.facultyinfo.unt.edu/jdh0355%2Fschteach%2F3550-1.pdf |
| 8 |Rate My Professor - Zeenat Tariq |143 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2722479 |
| 9 |UNT course info - Fundamentals of Database systems |Official course description, prerequisites, policies, grading structure, and credit hours |https://s3.amazonaws.com/mirror.facultyinfo.unt.edu/rmg0045%2Fschteach%2F4350%20-%20Syllabus%20-%20Spring%202026-1.pdf|
| 10 |Rate My Professor - Hadiseh Gooran |32 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2940069 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->
**RMP Reviews - Document Chunking"**
**Chunk size:50-250**
**Overlap:0**
**Reasoning: Each reviews is treated as one chunk and no overlap is needed because of that.**

**Syllabus - Section-level chunking**
**Chunk: 100-400**
**Overlap: 0**
**Reasoning: Each section of the syllabus talks about one topic which should be lost because of chunking and no overlap needed as there is no cross relation among the topics**
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model: all-MiniLM-L6-v2 via sentence-transformers (local, no API key)**

**Top-k:Start at 5**

**Production tradeoff reflection: OpenAI text-embedding-3-large for better accuracy, multilingual-e5 if non-English reviews appear, cost vs. latency tradeoff of API vs. local**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |How are the group projects in CSCE 3444 instructed by Hadiseh Gooran? |Group projects are a major component, 
described as fun and well-organized by the professor. |
| 2 |What are the file upload rules for assignments? |Files must be uploaded individually. do not zip or compress them Only file types previewable by Canvas DocViewer are accepted. Students are responsible for verifying their submission was uploaded and accepted. |
| 3 |How lenient is Jonathan Doran as a grader |Doran is described as a tough, strict grader — students warn to expect very low scores. He grades in an all-or-nothing style with no partial credit. No textbook or structured materials are provided; exams are based solely on his lectures. |
| 4 | What is Bahareh Dorri's teaching style like? |Classes are interactive with many example problems. Students can earn bonus points by solving problems on the board. She and her TAs respond promptly to emails and she is consistently 
accessible for help. |
| 5 |How are grades divided among categories in Fundamentals of Database Systems? |Homework 35%, Quizzes 35%, 
Midterm 15%, Final Exam 15%. Note that percentages are approximate and subject to change. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. The syllabus may contain paragraph breaks within the same topic, causing related information to land in separate chunks. For example, the grading policy description and the actual percentage breakdown may be separated by a paragraph break — split into two chunks, neither of which fully answers "how is this course graded?" on its own. Fix: chunk on section headers rather than paragraph breaks, and manually inspect chunks before embedding.

2.Not all reviews mention the same aspects of a professor. One student may write only about exam difficulty, another 
only about teaching clarity, another only about grading fairness. A query like "what is Doran's attendance policy?" may return zero relevant chunks if no student ever mentioned attendance in their review, even if Doran has 8 reviews in the corpus. The system would either return loosely related chunks or generate a hallucinated answer from general knowledge. Fix: include the course syllabus for that professor where possible, since it explicitly covers attributes reviews may never mention.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
Raw docs(.txt reviews, .pdf syllabus) -> Ingestion (pdfplumber, plain text loading) -> Chunking (Record-level-RMP, Section-level-Syllabus) -> Embedding + Vector Store(all-MiniLM-L6-v2,sentence-transformers,ChromaDB (local)) -> Retrieval(Semantic Search, top k = 5, ChromaDB .query()) -> Generation (Groq llama-3.3-70b)
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Objective: Ingestion
Tool: Claude
Input: Documents section (source list with file types), Chunking Strategy section, pipeline diagram
Ask for: A script that loads .txt files from data/raw/ using plain text reading and .pdf files using pdfplumber, cleans repeated headers, page numbers, and whitespace artifacts, and outputs clean text per document
Verify: Print one cleaned RMP file and one cleaned syllabus section and confirm no HTML artifacts, repeated headers, or empty strings remain

Objective: Chunking
Tool: Claude
Input: Chunking Strategy section (record-level for reviews, section-level for syllabi, 500 token ceiling), cleaned document output from ingestion step
Ask for: A chunk_documents() function that splits RMP .txt files on double newlines (one review per chunk) and splits syllabus text on section headers, attaches metadata fields (professor, course_code, source, type, section) to every chunk
Verify: Print 5 random chunks and confirm each is readable, self-contained, under 500 tokens, and has correct metadata attached

**Milestone 4 — Embedding and retrieval:**
Objective: Embedding
Tool: Claude
Input: Retrieval Approach section, pipeline diagram, chunk output format from Milestone 3
Ask for: An embed_and_store() function that loads chunks, embeds them using all-MiniLM-L6-v2 via sentence-transformers, and stores them in ChromaDB with all metadata fields preserved
Verify: Query ChromaDB directly with a known professor name and confirm correct chunks are returned with source metadata intact

Objective: Retrieval
Input: Retrieval Approach section (top-k=5, ChromaDB), embed_and_store() output
Ask for: A retrieve(query, k=5) function that accepts a query string and returns the top 5 chunks with their text, source, professor, and course_code metadata
Verify: Run 3 evaluation plan queries and print returned chunks — confirm they are relevant and distance scores are below 0.5

**Milestone 5 — Generation and interface:**
Objective: Generation
Tool: Groq
Input: Grounding requirement (answer from retrieved context only), evaluation plan questions, retrieve() output format
Ask for: A prompt template and Groq API call that passes retrieved chunks as context and explicitly instructs the model to answer only from that context, with source filenames appended to every response
Verify: Ask one in-scope question and confirm answer cites a source. Ask one out-of-scope question and confirm system declines rather than hallucinating

Objective: Interface
Tool: Claude
Input: Generation output format (answer + sources), Gradio skeleton from project spec
Ask for: A Gradio app.py with a text input, Ask button, answer output box, and sources output box wired to the end-to-end ask() function
Verify: Run python app.py, open localhost:7860, submit one evaluation plan question and confirm answer and sources both display correctly
