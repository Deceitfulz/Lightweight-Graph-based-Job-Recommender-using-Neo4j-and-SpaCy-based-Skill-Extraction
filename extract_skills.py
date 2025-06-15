import pandas as pd
import spacy
from tqdm import tqdm

# Load model spaCy kecil (cepat dan ringan)
nlp = spacy.load("en_core_web_sm")

# Load daftar skill dari file
with open("skills_list.txt", "r", encoding="utf-8") as f:
    skills = set([line.strip().lower() for line in f if line.strip() and not line.startswith("#")])

# Load dataset
df = pd.read_csv("D:/Kuliah/Sem8/Graph/NODES 2025/data/postings.csv")

# Ambil kolom description saja
job_descriptions = df["description"].fillna("").astype(str)

# Simpan hasil ekstraksi
extracted_skills = []

print("🔍 Mulai ekstraksi skill...")

for i, desc in enumerate(tqdm(job_descriptions, total=len(job_descriptions))):
    doc = nlp(desc.lower())
    found = set()
    for token in doc:
        if token.text in skills:
            found.add(token.text)
    # Cek phrase (biar "machine learning" bisa kena)
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if phrase in skills:
            found.add(phrase)
    extracted_skills.append(list(found))

    if i % 100 == 0:
        print(f"✓ {i}: {df.loc[i, 'title']} → {list(found)}")

# Tambahkan kolom baru ke DataFrame
df["extracted_skills"] = extracted_skills

# Simpan hasil
df.to_csv("postings_with_skills.csv", index=False)
print("✅ Selesai! Hasil disimpan ke postings_with_skills.csv")