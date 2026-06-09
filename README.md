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

### Sample Chunks


**Chunk 1 (`chunk-0114`)** · source: `jonathon_doran_rmp.txt` · Jonathan Doran · CSCE 4600 · type: review

> Course: CSCE 4600 Date: Jun 7th, 2026 Rating: 3 Difficulty: 4 Would Take Again: Yes Grade: A+ Review: Personality is his biggest flaw — he can come off as rude and condescending. Holds students to a high standard that he himself often fails to maintain with frequent mistakes on his part. That aside lectures are good and workload is reasonable. Email response time is great. If you can stand a difficult personality he is manageable at least for CSCE 4600.

**Chunk 2 (`chunk-0028`)** · source: `bahareh_dorri_rmp.txt` · Bahareh Dorri · CSCE 4110 · type: review

> Course: CSCE 4110 Date: May 2nd, 2026 Rating: 5 Difficulty: 3 Would Take Again: Yes Grade: B Review: Professor Dorri is a great lecturer with clear examples, but be prepared for unannounced quizzes that heavily impact your grade. Study guides are too vague to help with exams. Also, poor handling of cheating led to assigned seating and harder tests for everyone. TAs are hit-or-miss and can be rude or have an ego. Overall good class but minor issues.

**Chunk 3 (`chunk-0101`)** · source: `hadiseh_gooran_rmp.txt` · Hadiseh Gooran · CSCE 3444 · type: review

> Course: CSCE 3444 Date: Jan 24th, 2025 Rating: 5 Difficulty: 3 Would Take Again: Yes Grade: A Review: Honestly one of the best professors I've had at UNT. She is super nice and really knows her stuff. She explains everything clearly and her lectures are interactive which is rare. Group projects are a big part but she makes them fun and keeps everything organized. Practical assignments teach real-world skills. Highly recommend.

**Chunk 4 (`chunk-0240`)** · source: `fundamentals_database_managemnet_systems.pdf` · Ryan Garlick · CSCE 4350 · type: syllabus · section: "Communication Expectations"

> Communication Expectations
> Please send all communication as email via your official student UNT email (my.unt.edu), and if applicable, CC the TA for the class. I see emails before I see Canvas notifications. [...] I have a 48 hour reply policy on all emails, excepting weekends and holidays. [...]
> In your emails please include:
> • Subject line: the course (e.g. CSCE 4350) that you are emailing about and a few words (aka, the Subject)
> • Body: a signature with your email with your name and UNT ID number.

**Chunk 5 (`chunk-0227`)** · source: `foundations_of_cybersecurity.pdf` · Dr. Jacob Hochstetler · CSCE 3550 · type: syllabus · section: "Canvas File Upload Policy"

> Canvas File Upload Policy
> Assignments may require multiple file uploads. Do not archive/compress/zip these into one file: Attach them individually. The only acceptable file type for upload is what can be previewed automatically by DocViewer in Canvas. Please ensure you have actually submitted your files to Canvas; it is your responsibility to verify that the file has been uploaded and accepted.

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

## Retrieval Test Examples


### Example 1: "How lenient is Jonathan Doran as a grader?"

| Rank | Source | Course | distance | rerank | Chunk |
|------|--------|--------|----------|--------|------------------|
| 1 | `jonathon_doran_rmp.txt` | CSCE 3444 | 0.290 | 4.40 | "...He is a harsh grader and very condescending. Sometimes picks students one by one... Lectures don't make any sense..." |
| 2 | `jonathon_doran_rmp.txt` | CSCE 4010 | 0.333 | 3.42 | "...Doran has a very short temper... His lectures have little correlation to quizzes and papers he assigns..." |
| 3 | `jonathon_doran_rmp.txt` | CSCE 4600 | 0.413 | 3.05 | "...he can come off as rude and condescending. Holds students to a high standard... lectures are good and workload is reasonable..." |

**Why these are relevant:** All three results are actually Doran reviews, not some other professor, and the top one literally calls him a "harsh grader" which is exactly what I asked about. I think this works because I prepend the professor name to each chunk before embedding, so a query with his name stays on his reviews instead of grabbing any review that happens to mention harsh grading.

### Example 2: "What is Bahareh Dorri's teaching style like?"

| Rank | Source | Course | distance | rerank | Chunk (abridged) |
|------|--------|--------|----------|--------|------------------|
| 1 | `bahareh_dorri_rmp.txt` | CSCE 4110 | 0.416 | 5.51 | "...Has a great lecture and teaching style. The subject material is tough, but she teaches it effectively..." |
| 2 | `bahareh_dorri_rmp.txt` | CSCE 2110 | 0.372 | 3.09 | "...Many lectures felt rushed or confusing, and I relied heavily on YouTube and notes from other sources..." |
| 3 | `bahareh_dorri_rmp.txt` | CSCE 4110 | 0.445 | 2.51 | "...Teaches and shows everything you need. Makes learning algorithms interesting..." |

**Why these are relevant:** Every result is a Dorri review and all of them talk about her teaching: how she lectures, whether things are clear, how she presents the material. The interesting part is chunk #1 had a worse bi-encoder distance (0.416) than chunk #2 (0.372) but the reranker still moved it to the top. That makes sense to me: the cross-encoder looks at the question and the chunk together, so it picks up that "great lecture and teaching style" answers a *style* question better than a complaint about pacing. This is also why I could keep k small instead of pulling a ton of chunks.

### Example 3: "How are grades divided in Fundamentals of Database Systems?"

| Rank | Source | Course | distance | rerank | Chunk (abridged) |
|------|--------|--------|----------|--------|------------------|
| 1 | `foundations_of_cybersecurity.pdf` | CSCE 3550 | 0.565 | -8.68 | "Grade: 80-89 B, 70-79 C... no curving of grades, nor extra credit." |
| 2 | `fundamentals_database_managemnet_systems.pdf` | CSCE 4350 | 0.584 | -9.33 | "Course Description: logical and physical database system organization..." |
| 3 | `fundamentals_database_managemnet_systems.pdf` | CSCE 4350 | 0.410 | -10.13 | "Final Grade Letter: 90.0-100 A, 80.0-89.9 B... There is no curving of grades." |

**Why this one is weaker (honest note):** I was asking how grades are *divided*, meaning the percentage split (Homework 35%, Quizzes 35%, Midterm 15%, Final 15%), but instead it gave me the grade *letter scales*, and it even pulled a cybersecurity chunk at #1 which isn't even the right course. My guess is the embedder just latched onto the word "grade" and missed that I meant the weightings, so the actual percentage chunk never made the top 3. The rerank scores here are all very negative, which at least tells me none of these really answer the question. This is the retrieval problem behind one of my evaluation results and I dig into it more in the Failure Case Analysis.

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

### Example Responses (with source attribution)

**Q: "How lenient is Jonathan Doran as a grader?"**

> **Answer:** According to the reviews, Jonathan Doran is not lenient as a grader. He is described as a "harsh grader" in one review, and despite his difficult teaching style and personality, students have still managed to earn high grades such as A and A-. This suggests that while he may be demanding, it is possible to achieve a good grade in his class. However, his grading is generally perceived as strict.
>
> **Sources:**
> - `jonathon_doran_rmp.txt` (Jonathan Doran)

**Q: "What are the file upload rules for assignments?"**

> **Answer:** For assignments, files should be uploaded individually and not archived/compressed/zipped into one file. Only file types that can be previewed automatically by DocViewer in Canvas are acceptable. It is the student's responsibility to verify that the file has been uploaded and accepted by Canvas.
>
> **Sources:**
> - `foundations_of_cybersecurity.pdf` (CSCE 3550)
> - `fundamentals_database_managemnet_systems.pdf` (CSCE 4350)

### Out-of-Scope Query (refusal)

**Q: "What is the best dorm to live in at UNT?"**

> **Answer:** I don't have enough information on that.
>
> **Sources:** *(none)*

This is correct behavior: the corpus only covers CSCE professors and course syllabi, so there is nothing about dorms to ground an answer on, and the system refuses instead of guessing.

---

## Query Interface

**Input fields**
- **Your question** (textbox): a free-text question about a UNT CSCE professor or course. Submit with the **Ask** button or by pressing Enter.

**Output fields**
- **Answer** (textbox): the grounded answer generated from the retrieved chunks, or the refusal string if nothing relevant was found.
- **Retrieved from** (textbox): the deduplicated list of source documents the answer was grounded in, one per line. Shows "— (no grounded sources)" on a refusal.

**Sample interaction transcript**

```
Your question:  What are the group projects like in CSCE 3444 with Hadiseh Gooran?

Answer:
  In CSCE 3444 with the professor, group projects are a significant part of the
  course. One student mentioned that the professor makes them fun and keeps
  everything organized. However, another student had a negative experience with a
  group project due to an unresponsive teammate, which made things harder for the
  rest of the group. The projects are described as teaching real-world skills and
  being practical. In some semesters, there was only one project for the entire
  semester, such as building an app.

Retrieved from:
  • hadiseh_gooran_rmp.txt (Hadiseh Gooran)
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |Group projects in CSCE 3444 with Hadiseh Gooran |Group projects are a major component, described as fun and well-organized. |"Significant part of the course; prof makes them fun and organized, teaches real-world skills; one student had an unresponsive teammate." |Relevant |Accurate |
| 2 |File upload rules for assignments |Upload files individually (do not zip); only Canvas DocViewer-previewable types; student is responsible for verifying the upload was accepted. |"Upload individually, no archiving/zipping, only DocViewer-previewable types, and verify the file was uploaded and accepted." |Relevant |Accurate |
| 3 |How lenient is Jonathan Doran as a grader |Tough, strict, all-or-nothing grader with no partial credit; no textbook, exams based on lectures. |"Not lenient; described as a harsh grader, though some students still earned A / A-." |Relevant |Accurate |
| 4 |Bahareh Dorri's teaching style |Interactive with many example problems, board bonus points, prompt email replies, consistently accessible. |"Great and effective; clear examples, good pace, makes algorithms interesting; one course felt rushed and study guides were vague." |Relevant |Accurate |
| 5 |How are grades divided in Fundamentals of Database Systems |Homework 35%, Quizzes 35%, Midterm 15%, Final 15% (approximate). |"Returned the letter-grade *scale* (90-100 A, 80-89.9 B, ...) and 'no curving', NOT the category weightings asked for." |Partially relevant |Partially accurate  |

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

**Question that failed: How are grades divided in Fundamentals of Database Systems?**

**What the system returned:** Instead of the category weightings (Homework 35%, Quizzes 35%, Midterm 15%, Final 15%), it gave back the letter-grade scale (90-100 A, 80-89.9 B, and so on) and the "no curving of grades" note. So the answer is about grades but it's the wrong kind of grading info.

**Root cause (tied to a specific pipeline stage):** The chunk that actually has the answer (chunk-0256) does exist in the corpus, but my section-level chunking put the weighting table under the header "Category Final Grade", which doesn't contain any of the words in my question like "divided" or even "grade". When I retrieve, the chunks that say "Grade" and "Final Grade Letter" look closer to the query, so the bi-encoder and the reranker both rank them higher. I checked and the correct chunk lands at rank #7, which is past my k=5 cutoff, so the model never even sees it and answers from the letter-scale chunks instead.

**What you would change to fix it:** Either chunk the grading section so the weighting table keeps the surrounding words (like "final grade is divided into these categories") instead of just the bare header, or add a small query rewrite step so a question about how grades are "divided" also searches for "category percentage weighting". Bumping k would technically pull chunk #7 in, but that's the lazy fix and it just adds noise, so I'd rather fix the chunk or the query.

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