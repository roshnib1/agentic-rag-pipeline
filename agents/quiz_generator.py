from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from core.config import GROQ_API_KEY, LLM_MODEL
import json
import re

def generate_quiz(context: list, difficulty: str, num_questions: int, quiz_type: str) -> list:
    context_str = "\n".join(context[:8])  # Use top 8 chunks

    prompt = PromptTemplate.from_template("""
You are a quiz generator. Generate {num_questions} quiz questions based on the context below.

Difficulty: {difficulty}
Type: {quiz_type}

Rules:
- For MCQ: provide 4 options (A, B, C, D) and indicate the correct answer
- For True/False: provide a statement and indicate if it is True or False
- Mix both types if quiz_type is "mixed"
- Easy: basic recall questions
- Medium: understanding and application questions  
- Hard: analysis and inference questions
- Return ONLY a valid JSON array, no explanation, no markdown

Format:
[
  {{
    "type": "mcq",
    "question": "question text",
    "options": {{"A": "option1", "B": "option2", "C": "option3", "D": "option4"}},
    "answer": "A",
    "explanation": "brief explanation"
  }},
  {{
    "type": "truefalse",
    "question": "statement text",
    "answer": "True",
    "explanation": "brief explanation"
  }}
]

Context:
{context}

Generate exactly {num_questions} questions now:
""")

    llm = ChatGroq(
        model=LLM_MODEL,
        groq_api_key=GROQ_API_KEY,
        temperature=0.4
    )

    chain = prompt | llm
    response = chain.invoke({
        "num_questions": num_questions,
        "difficulty": difficulty,
        "quiz_type": quiz_type,
        "context": context_str
    })

    # Parse JSON from response
    try:
        text = response.content.strip()
        # Remove markdown code blocks if present
        text = re.sub(r"```json|```", "", text).strip()
        questions = json.loads(text)
        return questions
    except Exception as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response: {response.content}")
        return []