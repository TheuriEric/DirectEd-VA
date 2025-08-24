## 🎓 DirectEd: An Adaptive AI Educational Assistant
DirectEd is a smart, adaptive educational assistant designed to provide personalized learning experiences. Built with FastAPI and LangChain, it uses a sophisticated multi-step pipeline to answer user questions, generate custom learning content, and provide actionable feedback. The assistant is powered by a large language model fine-tuned with LoRA, enabling it to maintain a specific instructional tone and format.

## ✨ Features
Adaptive Tutoring: Guides students using a Socratic method, providing hints and encouraging critical thinking rather than just giving answers.

Intelligent Content Generation: Creates tailored educational content, including summaries, quizzes, and examples, based on the student's needs and difficulty level.

Learning Analysis: Provides a detailed breakdown of a student's strengths and weaknesses and suggests personalized next steps.

Fine-Tuned Persona: Uses a fine-tuned LoRA adapter to ensure a consistent, supportive, and knowledgeable persona across all interactions.

## Project Structure
.
├── finetuning/
│   ├── finetuned_model/
│   │   ├── README.md
│   │   └── finetuning_and_inference.ipynb
│   ├── generate_dataset.py
│   ├── prepare_data.py
│   └── run_finetuning.py
├── knowledge/
├── data/
├── db/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── pipeline.py
│   ├── templates.py
│   └── core/
│       ├── __init__.py
│       ├── app.py
│       ├── chatbot.py
│       ├── components.py
│       ├── data_handlers.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── endpoints.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── chat_models.py
│       └── services/
│           ├── __init__.py
│           └── educational_assistant.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── trials.ipynb

## Core Technologies
Python: The primary programming language.

FastAPI: A modern, high-performance web framework.

LangChain: The framework for building the LLM application pipeline.

Hugging Face: Used for loading models, tokenizers, and running fine-tuning.

PEFT (LoRA): Parameter-Efficient Fine-Tuning for adapting the model with minimal cost.

TRL (Transformer Reinforcement Learning): Provides the SFTTrainer for fine-tuning.

ChromaDB: The vector store for Retrieval-Augmented Generation (RAG).

Docker: For containerization and deployment.

## 🚀 Setup and Installation
Clone the repository:
```Bash

git clone https://github.com/TheuriEric/DirectEd-VA.git
cd DirectEd-VA
```
Create a virtual environment:

```Bash

python -m venv venv
source venv/bin/activate
Install dependencies:
```

```Bash

pip install -r requirements.txt
#Set up API Keys:
#Create a .env file in the root directory and add your API keys.


OPENAI_API_KEY="your-openai-key"
GROQ_API_KEY="your-groq-key"
```
## Fine-Tuning Workflow
The fine-tuning process is separate but essential for improving the model's performance.

Generate a Dataset: Run finetuning/generate_dataset.py.

Prepare the Data: Run finetuning/prepare_data.py.

Run Fine-Tuning: Use the finetuning/run_finetuning.py to execute the fine-tuning process and save the finetuned_adapters to the finetuned_adapters directory.


## Running with Docker
This project is fully containerized for easy deployment.

Build the Docker image:

```Bash

docker build -t direct-ed-app .
```
Run the application using Docker Compose:

```Bash

docker-compose up -d
```
This command will build and start your application and any other services defined in the docker-compose.yaml file (e.g., a database).

## Usage
Once the application is running, the API will be available at http://127.0.0.1:8000. You can test the endpoints using a tool like Postman or by navigating to http://127.0.0.1:8000/docs to use the interactive Swagger UI.

