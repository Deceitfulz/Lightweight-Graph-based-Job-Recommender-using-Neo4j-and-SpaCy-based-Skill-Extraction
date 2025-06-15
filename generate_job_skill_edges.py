import pandas as pd
import ast

# Load data hasil ekstraksi
df = pd.read_csv("postings_with_skills.csv")

# Pastikan kolom 'extracted_skills' diparsing sebagai list
df["extracted_skills"] = df["extracted_skills"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

# Simpan pasangan (job_id, skill) sebagai edge
edges = []

for _, row in df.iterrows():
    job_id = row["job_id"]
    for skill in row["extracted_skills"]:
        edges.append((job_id, skill))

# Buat DataFrame edge
edges_df = pd.DataFrame(edges, columns=["job_id", "skill"])

# Simpan ke CSV
edges_df.to_csv("job_requires_skill.csv", index=False)
print("✅ File job_requires_skill.csv berhasil dibuat.")