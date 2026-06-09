# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
Domain: Student reviews and experiential knowledge about Computer Science & Engineering (CSCE) professors and courses at the University of North Texas (Denton, TX)

Why this knowledge valuavble and hard to find through official channels: Th UNT official channels only tells us about the course catalog, department website and registration system. It also mentions the course availability and the instructor assigned to the class. These information doesn't help the student understand the abilities of an instructor. It tells nothing about whether the professor explains things clearly, exam's leniency, and more importantly the student reviews. All these information can be found in Rate My Professor, r/UNT reddit threads. All these information can be hard to find and analyze to choose the right class.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Rate My Professor - Jonathon Doran | 83 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/1579301 |
| 2 |Rate My Professor - Curtis Chambers |42 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/2174155 |
| 3 |Rate My Professor - Amar Maharjan |25 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/2649807 |
| 4 |Rate My Professor - Pradhumna Shrestha |44 ratings UNT CSCE professor |https://www.ratemyprofessors.com/professor/2174392 |
| 5 |Rate My Professor - Bahareh Dorri |22 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2936044 |
| 6 |Rate My Professor - David Keathly |74 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/702560 |
| 7 |UNT course info - Foundations of Cybersecurity|Official course description, prerequisites, policies, grading structure, and credit hours|https://s3.amazonaws.com/mirror.facultyinfo.unt.edu/jdh0355%2Fschteach%2F3550-1.pdf |
| 8 |Rate My Professor - Zeenat Tariq |143 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2722479 |
| 9 |UNT course info - Fundamentals of Database systems |Official course description, prerequisites, policies, grading structure, and credit hours |https://s3.amazonaws.com/mirror.facultyinfo.unt.edu/rmg0045%2Fschteach%2F4350%20-%20Syllabus%20-%20Spring%202026-1.pdf|
| 10 |Rate My Professor - Hadiseh Gooran |32 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2940069 |


---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:50-250(reviews) and 100-400(syllabus), cap to 500 max**

**Overlap:0**

**Why these choices fit your documents:reviews and sections are already discrete units**

**Final chunk count:279 (189 review + 90 syllabus)**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:all-MiniLM-L6-v2**

**Production tradeoff reflection:needs bigger embedder for better accuracy. If the data is non-English maybe a multilingual-e5, Local for cost contraints and API reducing complexity and quality embeddings.**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction: ONlY answer from the context provided. Refuse to answer anything if there is no context to refer to. IT should not add extra information and also shouldnot cite itself.**

**How source attribution is surfaced in the response:After the LLM generates the answer, the system builds a source list in Python from the retrieved chunks' source metadata. The LLM is explicitly instructed not to cite sources itself, so attribution is programmatically guaranteed rather than model-generated. On a refusal, the source list is empty.**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Gooran CSCE 3444 group projects | |"well-organized, made fun; one unresponsive teammate" |Relevant |Accurate |
| 2 |File upload rules | |"individually, no zip, DocViewer-only, verify accepted" |Relevant |Accurate |
| 3 |Doran grader leniency | |"harsh, not lenient; failed despite performing well" |Relevant |Accurate|
| 4 |Dorri teaching style | |"clear examples, interactive, well-paced; one course felt rushed" |Relevant |Accurate |
| 5 |DB grade split | |"Homework 35%, Quizzes 35%, Midterm 15%, Final 15%" |Relevant |Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed: How is Dorri's teaching style?**

**What the system returned:I dont have enough information on that**

**Root cause (tied to a specific pipeline stage):The bi-encoder the right review in #14 which is bad as k = 5 it ignored the correct one**

**What you would change to fix it:I used cross-encoder reranker and it moved the review from #14 to #2**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:The spec acted itself as a prompt for the Ai as it had all the information about the model, sources, pipeline architecture.i had to put minimal prompt as claude was advanced enought to read the documents and produce a running prototype.**

**One way your implementation diverged from the spec, and why:raised ceiling 400→500 (keep chunks whole) and added a reranker not in the original plan. As Question number 4 provided a refusal, I had to introduce a cross-encoder reranker to produce a correct embedding distance. This made the model accept the answer and use the correct embedding for generation**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI: planning.md was provide to AI which included the pipeline diagram, model selection, chunking strategy.*
- *What it produced: an embed_and_store() that loads the chunks, embeds them with all-MiniLM-L6-v2, and stores them in a persistent ChromaDB collection with all metadata preserved, plus a retrieve(query, k=5) function returning the top chunks with their source metadata and distance scores.*
- *What I changed or overrode:Nothing*

**Instance 2**

- *What I gave the AI:Open questions while buildinge for e.g. "what is source attribution?", "would needing k = 5 instead of k = 15 mean a better retrieval model?", and asking it to explain ChromaDB API calls I didn't recognize.*
- *What it produced: Explanations tying each concept to my own pipeline (e.g. that small-k-that-works signals better ranking, and that a stronger embedder or a reranker is the real fix), rather than generic textbook answers.*
- *What I changed or overrode:I used these to make my own design decisions, understood the limitations of a bi-encoder*

**Instance 3**

- *What I gave the AI:"What is Bahareh Dorri's teaching style like?" was returning "I don't have enough information on that." I gave it the retrieved chunks and asked why, and whether reducing k while still getting the answer was possible.*
- *What it produced: A diagnosis (the bi-encoder ranked the one substantive review #14, so top-k = 5 only saw thin generic praise and the model refused) and an implementation: a cross-encoder reranker*
- *What I changed or overrode: I rejected the quick fix of simply raising k in favor of the reranker, which let me keep k = 5.*