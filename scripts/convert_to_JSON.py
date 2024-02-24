from langchain.document_loaders import Docx2txtLoader
import json


document_path = "/home/elias/Documents/10 Academy/WEEK 11/LegalAI-RAG-Contract-Advisor/data/Evaluation Sets/Robinson Q&A.docx"
loader = Docx2txtLoader(document_path)
documents = loader.load()


question_answer_pairs = []
for document in documents:
    text = document.content
    current_question = None
    for line in text.splitlines():
        if line.startswith("Q:"):
            current_question = line[2:].strip()
        elif line.startswith("A:"):
            answer = line[2:].strip()
            if current_question:
                question_answer_pairs.append({"question": current_question, "answer": answer})
                current_question = None
json_data = json.dumps(question_answer_pairs, indent=4)
print(json_data)


