import spacy
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import csv

# Load spaCy NER model
nlp = spacy.load("en_core_web_sm")

# List of resume PDF file paths
resume_paths = ["resume1.pdf", "resume2.pdf", "resume3.pdf", "Priya_Resume.pdf"]  # Add more file paths here

# Extract text from PDFs
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

# Extract emails using regex (names can be extracted similarly, but not implemented here)
def extract_entities(text):
    # Extract emails using regular expression
    emails = re.findall(r'\S+@\S+', text)
    return emails

# Extract job description features using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
job_desc_vector = tfidf_vectorizer.fit_transform([job_description])

# Rank resumes based on similarity
ranked_resumes = []
for resume_path in resume_paths:
    resume_text = extract_text_from_pdf(resume_path)
    emails = extract_entities(resume_text)  # Only getting emails
    resume_vector = tfidf_vectorizer.transform([resume_text])
    similarity = cosine_similarity(job_desc_vector, resume_vector)[0][0]
    ranked_resumes.append((emails, similarity))

# Sort resumes by similarity score
ranked_resumes.sort(key=lambda x: x[1], reverse=True)

# Display ranked resumes with emails
for rank, (emails, similarity) in enumerate(ranked_resumes, start=1):
    print(f"Rank {rank}: Emails: {emails}, Similarity: {similarity:.2f}")

# Writing to CSV (no name column)
with open(csv_filename, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Rank", "Email", "Similarity"])

    for rank, (emails, similarity) in enumerate(ranked_resumes, start=1):
        email = emails[0] if emails else "N/A"
        csv_writer.writerow([rank, email, similarity])

