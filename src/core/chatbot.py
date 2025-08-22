from .components import *
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from .data_handlers import retriever
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    reasoning_effort="medium"
)

educational_retriver = EducationalRetriever(retriever)
content_generator = ContentGenerator(llm, educational_retriver)
analyzer = LearningAnalyzer()

@traceable(run_type="chain")
def run_educational_assistant(request: str, user_id:str,analyzer: LearningAnalyzer, is_instructor: bool = False) -> Dict[str, Any]:

    router = PromptTemplate.from_template(
        "Analyze the request: '{request}'. Is it asking for a quiz, or a general explanation (tutoring)? Respond with 'QUIZ' or 'TUTORING'."
    ) | llm | StrOutputParser()

    try:
        user_intent = router.invoke({"request": request}).strip().upper()
        
        output_content = ""
        content_type = ""

        if "QUIZ" in user_intent:
            output_content = content_generator.generate_quiz(request)
            content_type = "QUIZ"
        else:
            output_content = content_generator.answer_generator(request)
            content_type = "TUTORING"

        performance = "correct" if "quiz" in request.lower() else "incorrect"
        analyzer.log_performance(user_id, request, performance)
        response = {
            "user_type": "Instructor" if is_instructor else "Student",
            "content_type": content_type,
            "output": output_content,
            "updated_profile": analyzer.get_profile(user_id)
        }
        return response
    except Exception as e:
        return {"Error!": "An error occurred during execution.", "details": str(e)}
    
    
if __name__ == "__main__":
    import json
    analyzer = LearningAnalyzer()
    
    # Test Case 1: Student requesting tutoring
    print("Running Test Case 1: Student asks for an explanation.")
    response1 = run_educational_assistant(
        "Explain the langchain's use using flashcards", 
        "student_123", 
        analyzer
    )
    print("\n--- Final Response 1 ---")
    print(json.dumps(response1, indent=2))
    
    print("\n" + "="*50 + "\n")
    
    # Test Case 2: Student requesting a quiz
    print("Running Test Case 2: Student asks for a quiz.")
    response2 = run_educational_assistant(
        "Give me a quiz about design.", 
        "student_123", 
        analyzer
    )
    print("\n--- Final Response 2 ---")
    print(json.dumps(response2, indent=2))