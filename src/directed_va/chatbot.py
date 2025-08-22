from components import *

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
    
    


    
