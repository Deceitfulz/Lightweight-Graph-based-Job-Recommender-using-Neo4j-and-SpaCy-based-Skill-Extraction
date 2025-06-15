import pandas as pd
import ast

# Load file profil yang sudah diekstrak
df = pd.read_csv("data/processed/profiles_with_skills.csv")

# Parse kolom extracted_skills
df["extracted_skills"] = df["extracted_skills"].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else [])

# Tambah person_id otomatis
df["person_id"] = df.index + 1

# Simpan node Person
people_df = df[["person_id", "name"]]
people_df.to_csv("data/processed/people.csv", index=False)
print("✅ people.csv berhasil dibuat.")

# Simpan edge HAS_SKILL
edges = []
for i, skills in enumerate(df["extracted_skills"]):
    pid = df.loc[i, "person_id"]
    for skill in skills:
        edges.append({"person_id": pid, "skill": skill})

edges_df = pd.DataFrame(edges)
edges_df.to_csv("data/processed/person_has_skill.csv", index=False)
print("✅ person_has_skill.csv berhasil dibuat.")