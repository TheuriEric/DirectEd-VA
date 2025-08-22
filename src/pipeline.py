import torch
import gc
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load model with memory management
MODEL_NAME = "sidiushindi/DirectEd-Curriculum-Bot"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
# Clear memory first
if torch.cuda.is_available():
    torch.cuda.empty_cache()
gc.collect()

# Load with minimal memory usage
try:
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
        device_map=None  
    )
    
    # Move to GPU if available, otherwise stay on CPU
    if torch.cuda.is_available():
        print("Moving model to GPU...")
        model = model.to("cuda")
    else:
        print("Using CPU...")
        
except Exception as e:
    print(f"Error loading model: {e}")
    print("Trying CPU-only fallback...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, 
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    )

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Create pipeline
print("Creating text generation pipeline...")
hf_pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, 
                   max_new_tokens=512, temperature=0.2, return_full_text=False)
llm = HuggingFacePipeline(pipeline=hf_pipe)

# Define prompts using new syntax
content_retrieval_prompt = PromptTemplate.from_template(
    "### Instruction:\nExtract relevant info for: {user_question}\n\nDocuments: {retrieved_documents}\n\n### Response:\n"
)

conversation_prompt = PromptTemplate.from_template(
    "### Instruction:\nYou are a {topic} tutor. Answer: {user_question}\n\nContent: {retrieved_content}\n\n### Response:\n"
)

# Create chains using new LCEL syntax
content_chain = content_retrieval_prompt | llm | StrOutputParser()
conversation_chain = conversation_prompt | llm | StrOutputParser()

def run_pipeline(user_question, topic, retrieved_documents):
    """Run the education pipeline using new LangChain syntax"""
    print("Step 1: Extracting relevant content...")
    retrieved_content = content_chain.invoke({
        "user_question": user_question,
        "retrieved_documents": retrieved_documents
    })
    
    print("Step 2: Generating response...")
    response = conversation_chain.invoke({
        "user_question": user_question,
        "topic": topic,
        "retrieved_content": retrieved_content
    })
    
    return {"retrieved_content": retrieved_content, "response": response}

# Example usage
if __name__ == "__main__":
    result = run_pipeline(
        user_question="What are UI accessibility best practices?",
        topic="UI/UX Design",
        retrieved_documents="WCAG guidelines: Perceivable, Operable, Understandable, Robust. Use alt text, color contrast, keyboard navigation."
    )
    
    print("\n" + "="*50)
    print("RESULTS:")
    print("="*50)
    print("Response:", result["response"])