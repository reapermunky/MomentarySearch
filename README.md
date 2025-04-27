# MomentarySearch

MomentarySearch is an ephemeral AI assistant that provides instant, context-aware answers by retrieving and processing real-time web information. It leverages live search results to deliver up-to-the-minute accuracy, without storing user data or retaining long-term memory.

## Note:
MomentarySearch is not just a lightweight search assistant. It represents an alternate model for AI itself - ephemeral, stateless, and privacy-native by architecture. In a world increasingly driven by centralized, memory-hoarding models, MomentarySearch demonstrates that real-time intelligence can be achieved without surveillance, without bloat, and without permanent data retention. This is a small project — but it points toward a different future for AI.


## Features

* **Ephemeral Knowledge:** Answers are generated based on real-time web searches and are not stored.
* **Context-Aware Responses:** Utilizes language models to provide relevant answers based on search snippets.
* **Real-Time Information:** Retrieves information directly from the web for the most current data.
* **CLI and API:** Accessible via a command-line interface or a simple API.

## Getting Started

### Prerequisites

* Python 3.6+
* pip
* A SerpAPI key (You can get one from [SerpAPI](https://serpapi.com/))

### Installation

1.  Clone the repository:

    ```bash
    git clone [your_repository_url]
    cd MomentaryAI
    ```

2.  Install the required Python packages:

    ```bash
    pip install fastapi uvicorn requests transformers torch serpapi
    ```

3.  Set your SerpAPI key as an environment variable:

    * **Windows:**
        ```bash
        setx SERPAPI_KEY "YOUR_ACTUAL_KEY"
        ```
    * **macOS/Linux:**
        ```bash
        export SERPAPI_KEY="YOUR_ACTUAL_KEY"
        ```

### Usage

#### CLI

1.  Run the Python script:

    ```bash
    python ephemeral_ai.py
    ```

2.  Enter your queries in the terminal.

3.  To exit, type `exit` or `quit`.

#### API

1.  Run the API server:

    ```bash
    python ephemeral_ai.py server
    ```

2.  Send GET requests to `/ask?query=YOUR_QUESTION`:

    ```bash
    curl "[http://0.0.0.0:8000/ask?query=What%20is%20the%20weather%20today](http://0.0.0.0:8000/ask?query=What%20is%20the%20weather%20today)?"
    ```

## Example

**CLI:**

User > What are the latest advancements in renewable energy?
Assistant > ... (assistant's response)


**API Response:**

```json
{
  "question": "What is the capital of France?",
  "answer": "Paris."
}
