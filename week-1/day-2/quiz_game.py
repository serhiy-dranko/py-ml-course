questions = [
    {"question": "What is 2 + 2?", "answer": "4"},
    {"question": "Capital of Germany?", "answer": "Berlin"},
    {"question": "What color is the sky?", "answer": "blue"},
    {"question": "How many days in a week?", "answer": "7"},
    {"question": "What is famos greeting from Die Hard?", "answer": "Yippee-ki-yay"},
]


def run_quiz(questions):
    score = 0

    for q in questions:
        try:
            user_answer = input(q["question"] + " ")
            if user_answer.strip().lower() == q["answer"].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Wrong. The correct answer was: {q['answer']}")
        except Exception:
            
            print("Something went wrong with that question, skipping.")

    return score


total_questions = len(questions)
final_score = run_quiz(questions)

print(f"\nYour final score: {final_score}/{total_questions}")

percentage = (final_score / total_questions) * 100

if percentage >= 80:
    print("Great job!")
elif percentage >= 50:
    print("Not bad, keep practicing!")
else:
    print("Keep practicing!")