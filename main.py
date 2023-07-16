import os
import sys
import json
import openai

openai.api_key = 'key'

response = openai.Completion.create(
  engine="text-davinci-003",
  prompt="Create a course outline for a beginner's course in Python programming.",
  max_tokens=60
)

# importing required modules
from PyPDF2 import PdfReader

# creating a pdf reader object
reader = PdfReader('/Users/suqiyang/Downloads/chapter-1-the-science-of-life.pdf')

# printing number of pages in pdf file
print(len(reader.pages))
for i in range(len(reader.pages)):
    page = reader.pages[i]
    text = page.extract_text()
    print(text)


class CourseGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.engine = "text-davinci-003"

    def create_course_from_text(self, input_text, max_tokens=200):
        prompt = f"Summarize the following text and create a course outline with 5 lessons: '{input_text}'"

        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=max_tokens
        )

        return response.choices[0].text.strip()

    def create_course_from_grade_subject(self, grade, subject, max_tokens=200):
        prompt = f"Create a course outline for a {grade} {subject} course."

        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=max_tokens
        )

        return response.choices[0].text.strip()

    def generate_quiz(self, text, num_questions=5, max_tokens=200):
        prompt = f"Generate {num_questions} quiz questions based on the following text: '{text}'"

        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt,
            max_tokens=max_tokens
        )

        return response.choices[0].text.strip()


# test
course_generator = CourseGenerator('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')

# Generating quiz from a text
quiz_questions = course_generator.generate_quiz('Can you create a quiz for students')
print(quiz_questions)


from src.chunker import Chunker
from src.open_ai_wrapper import OpenAIWrapper

books = [f'biology{i + 3}.pdf' for i in range(13)]
chapters = []
# Iterate over all books
for book in books:
    reader = PdfReader(book)
    chapter = ""
    # Iterate over all pages of the book
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text = page.extract_text()
        chapter += text
    chapters.append(chapter)

    # Break each book into a piece that fits within GPT prompt length
    c = Chunker()
    texts = c.chunk_text(chapter, chunk_size=6000, chunk_overlap=200)
    i = 0
    # Generate questions from each (change type of the question to get different kinds)
    for text in texts:
        i += 1
        if i >= 3:
            break
        prompt = "The following is an excerpt from a biology book for 10th graders: " + text
        prompt += "\n\nYou are a teacher trying to prepare material for students to study.\n"
        prompt += "Write 10 'explain' questions of increasing difficulty. Start with an easy question and gradually make it more difficult. Write the answer to the questions afterwards"
        answer = OpenAIWrapper.generate_text(prompt, model="gpt-4")
        # Print the questions generated
        print(answer)

# we break down the book, use openai wrapper, prompt with the right questions, and let users configure. 
