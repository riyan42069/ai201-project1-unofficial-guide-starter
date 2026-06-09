"""Milestone 5 — Gradio interface for The Unofficial Guide.

Run:
  .venv\\Scripts\\python.exe app.py
then open http://localhost:7860
"""
import gradio as gr

from query import ask  # end-to-end grounded generation


def handle_query(question: str):
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"]) or "— (no grounded sources)"
    return result["answer"], sources


with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown(
        "# The Unofficial Guide\n"
        "Ask about UNT CSCE professors and courses. Answers come **only** from "
        "student reviews and official syllabi in the knowledge base."
    )
    inp = gr.Textbox(label="Your question", placeholder="e.g. How lenient is Jonathan Doran as a grader?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
