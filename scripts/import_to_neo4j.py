from neo4j import GraphDatabase
import pandas as pd
from tqdm import tqdm

# Kredensial Neo4j
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "nodes2025"
NEO4J_PASSWORD = "ihsanifan"

# Koneksi
driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def create_job_nodes(tx, jobs_df):
    for _, row in jobs_df.iterrows():
        tx.run("""
            MERGE (j:Job {job_id: $job_id})
            SET j.title = $title
        """, {
            "job_id": str(row["job_id"]),
            "title": row["title"]
        })

def create_skill_nodes(tx, skill_list):
    for skill in skill_list:
        tx.run("""
            MERGE (s:Skill {name: $name})
        """, {"name": skill})

def create_person_nodes(tx, people_df):
    for _, row in people_df.iterrows():
        tx.run("""
            MERGE (p:Person {person_id: $person_id})
            SET p.name = $name
        """, {
            "person_id": str(row["id"]),
            "name": row["name"]
        })

def create_job_skill_edges(tx, job_skill_df):
    for _, row in job_skill_df.iterrows():
        tx.run("""
            MATCH (j:Job {job_id: $job_id})
            MATCH (s:Skill {name: $skill})
            MERGE (j)-[:REQUIRES]->(s)
        """, {
            "job_id": str(row["job_id"]),
            "skill": row["skill"]
        })

def create_person_skill_edges(tx, people_df):
    for _, row in people_df.iterrows():
        skills = eval(row["extracted_skills"]) if pd.notna(row["extracted_skills"]) else []
        for skill in skills:
            tx.run("""
                MATCH (p:Person {person_id: $person_id})
                MATCH (s:Skill {name: $skill})
                MERGE (p)-[:HAS_SKILL]->(s)
            """, {
                "person_id": str(row["id"]),
                "skill": skill
            })

def main():
    print("📦 Membaca data CSV...")
    jobs_df = pd.read_csv("data/processed/postings_with_skills.csv")
    people_df = pd.read_csv("data/processed/profiles_with_skills.csv")
    job_skill_df = pd.read_csv("data/processed/job_requires_skill.csv")

    # Ambil daftar skill unik dari job dan people
    skill_from_jobs = set(job_skill_df["skill"].dropna().unique())
    skill_from_people = set()
    for s in people_df["extracted_skills"].dropna():
        skill_from_people.update(eval(s))
    all_skills = skill_from_jobs.union(skill_from_people)

    with driver.session() as session:
        print("🧠 Membuat node Skill...")
        session.execute_write(create_skill_nodes, all_skills)

        print("🧠 Membuat node Job...")
        session.execute_write(create_job_nodes, jobs_df)

        print("🧠 Membuat node Person...")
        session.execute_write(create_person_nodes, people_df)

        print("🔗 Membuat relasi Job-REQUIRES->Skill...")
        session.execute_write(create_job_skill_edges, job_skill_df)

        print("🔗 Membuat relasi Person-HAS_SKILL->Skill...")
        session.execute_write(create_person_skill_edges, people_df)

    print("✅ Semua data berhasil diimport ke Neo4j!")

if __name__ == "__main__":
    main()