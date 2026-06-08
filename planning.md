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
| 7 |Rate My Professor - Jacod Hochsteller |14 ratings UNT CSCE Professor|https://www.ratemyprofessors.com/professor/2228800 |
| 8 |Rate My Professor - Zeenat Tariq |143 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2722479 |
| 9 |Rate My Professor - Ryan M. Garlick |58 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/272533 |
| 10 |Rate My Professor - Hadiseh Gooran |32 ratings UNT CSCE Professor |https://www.ratemyprofessors.com/professor/2940069 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

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

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
