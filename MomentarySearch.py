import os
import sys
from typing import List, Dict
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from serpapi import GoogleSearch
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
MAX_GENERATION_TOKENS = 200
NUM_SEARCH_RESULTS = 3

print("[INIT] Loading model. This may take a moment...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def generate_text(prompt: str, max_new_tokens: int = MAX_GENERATION_TOKENS) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_beams=3,
            do_sample=False
        )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def perform_web_search(query: str, num_results: int = NUM_SEARCH_RESULTS) -> List[Dict]:
    """
    Returns a list of {url, snippet} dictionaries.
    """
    if not SERPAPI_KEY or SERPAPI_KEY == "YOUR_SERPAPI_KEY_HERE":
        print("[WARNING] No valid SERPAPI_KEY. Returning fake/empty results.")
        return []

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num_results,
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    organic = results.get("organic_results", [])
    snippets = []
    for item in organic[:num_results]:
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        if link or snippet:
            snippets.append({"url": link, "snippet": snippet})
    return snippets

def ephemeral_knowledge_constructor(raw_snippets: List[Dict]) -> List[Dict]:
    knowledge_doc = []
    for s in raw_snippets:
        knowledge_doc.append({
            "source_url": s["url"],
            "text": s["snippet"]
        })
    return knowledge_doc

def compose_answer(user_query: str, knowledge_doc: List[Dict]) -> str:
    # Build context from ephemeral knowledge
    context_lines = []
    for i, item in enumerate(knowledge_doc, start=1):
        context_lines.append(f"Snippet {i}: {item['text']} (URL: {item['source_url']})")
    context_text = "\n".join(context_lines)

    # Provide a clear few-shot example
    example = """
Example:
Context:
Snippet 1: "Press Windows + I to open Settings."
Snippet 2: "Then go to Accounts > Sign-in Options and select Password."
Question: "How do I reset my Windows password?"
Answer: "Here are the steps: Press Windows + I to open Settings, go to Accounts > Sign-in Options, select Password, and follow the on-screen instructions to reset your password."

Now, using the context provided below, answer the question.
""".strip()

    # Construct the final prompt with the example
    prompt = f"""
{example}

Context:
{context_text}

Question: "{user_query}"
Answer:
""".strip()

    print("[DEBUG] Final Prompt to T5:\n", prompt)
    raw_output = generate_text(prompt)
    print("[DEBUG] Model raw output:\n", raw_output)
    # Optionally, remove any echoed example text
    lines = raw_output.split("\n")
    filtered = [line for line in lines if "Example:" not in line and "Context:" not in line and "Question:" not in line]
    final_answer = "\n".join(filtered).strip()
    return final_answer


# FASTAPI
app = FastAPI(
    title="Ephemeral AI Assistant",
    description="Minimal ephemeral knowledge AI with real-time search. No persistent memory.",
    version="1.0"
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Ephemeral AI Assistant</h1>
    <p>Send queries to <code>/ask?query=YOUR_QUESTION</code></p>
    """

@app.get("/ask")
def ask(query: str):
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Empty query.")
    
    search_results = perform_web_search(query)
    knowledge = ephemeral_knowledge_constructor(search_results)
    answer = compose_answer(query, knowledge)
    return {"question": query, "answer": answer}

def run_cli():
    print("Ephemeral Assistant (CLI Mode)")
    print("Type 'exit' or 'quit' to end.\n")

    while True:
        user_input = input("User > ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        search_results = perform_web_search(user_input)
        knowledge = ephemeral_knowledge_constructor(search_results)
        response = compose_answer(user_input, knowledge)
        print(f"Assistant > {response}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        run_cli()
