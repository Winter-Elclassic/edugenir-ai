SYSTEM_PROMPT = """
You are EduGenie, a helpful AI-powered learning assistant.

Your goal is to help students understand concepts clearly.
Use simple language, logical explanations, examples, and structured answers.

Do not unnecessarily make answers complicated.
"""


QA_PROMPT = """
Answer the student's question clearly and accurately.

Question:
{question}

Give a helpful educational answer with:
1. Direct answer
2. Short explanation
3. Example when useful
"""


EXPLAIN_PROMPT = """
Explain the following topic to a student.

Topic:
{topic}

Student level:
{level}

Explain using:
1. Simple definition
2. Step-by-step explanation
3. Real-world analogy or example
4. Important points
5. Short summary
"""


SUMMARY_PROMPT = """
Summarize the following text for a student.

Text:
{text}

Create a clear summary containing:
- Main ideas
- Important points
- Key terms
- A short final takeaway
"""


QUIZ_PROMPT = """
Create a multiple-choice educational quiz from the following text.

Text:
{text}

Number of questions:
{num_questions}

Each question must contain:
- question
- exactly 4 options
- correct answer
- short explanation

Return only valid JSON matching the requested schema.
"""


LEARNING_PATH_PROMPT = """
Create a personalized learning path for a student.

Topic:
{topic}

Current level:
{level}

Available duration:
{duration}

Provide:
1. Learning objectives
2. Ordered topics to study
3. Practice activities
4. Suggested project or practical activity
5. Weekly progression
6. Final revision plan

Keep the plan realistic and beginner-friendly when appropriate.
"""