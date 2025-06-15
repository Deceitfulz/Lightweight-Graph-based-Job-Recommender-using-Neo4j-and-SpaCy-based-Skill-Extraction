import pandas as pd
import spacy
from tqdm import tqdm

# Load model spaCy
nlp = spacy.load("en_core_web_sm")

# Load daftar skill
with open("skills_list.txt", "r", encoding="utf-8") as f:
    skills = set([line.strip().lower() for line in f if line.strip() and not line.startswith("#")])

# Load dataset profil
df = pd.read_csv("D:/Kuliah/Sem8/Graph/NODES 2025/data/LinkedIn people profiles datasets.csv")

# Kolom yang akan diekstrak skill-nya
columns_to_check = ["position", "about", "experience", "education", "certifications", "languages"]

# Gabungkan semua kolom teks ke satu kolom
df["combined_text"] = df[columns_to_check].fillna("").agg(" ".join, axis=1).str.lower()

# Ekstraksi skill
extracted_skills = []

print("🔍 Mulai ekstraksi skill dari profil...")

for i, text in enumerate(tqdm(df["combined_text"], total=len(df))):
    doc = nlp(text)
    found = set()
    for token in doc:
        if token.text in skills:
            found.add(token.text)
    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()
        if phrase in skills:
            found.add(phrase)
    extracted_skills.append(list(found))

    if i % 100 == 0:
        print(f"✓ {i}: {df.loc[i, 'name']} → {list(found)}")

# Simpan hasil ke DataFrame
df["extracted_skills"] = extracted_skills

# Simpan ke file
df.to_csv("profiles_with_skills.csv", index=False)
print("✅ Selesai! Hasil disimpan ke profiles_with_skills.csv")