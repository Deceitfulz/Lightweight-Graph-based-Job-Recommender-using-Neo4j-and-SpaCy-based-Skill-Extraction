from neo4j import GraphDatabase
import pandas as pd

# Kredensial Neo4j
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "nodes2025"
NEO4J_PASSWORD = "ihsanifan"

# Koneksi
driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def get_recommendations(tx, person_id):
    query = """
    MATCH (p:Person {person_id: $person_id})-[:HAS_SKILL]->(s:Skill)
    MATCH (j:Job)-[:REQUIRES]->(s)
    WITH j, COUNT(s) AS matched_skill_count, COLLECT(s.name) AS matched_skills
    RETURN j.title AS job_title, matched_skill_count, matched_skills
    ORDER BY matched_skill_count DESC
    LIMIT 5
    """
    result = tx.run(query, person_id=person_id)
    return [record.data() for record in result]

def recommend_and_save():
    # Ambil hanya 10 orang pertama
    people_df = pd.read_csv("data/processed/profiles_with_skills.csv")
    results = []

    with driver.session() as session:
        for i, row in people_df.iterrows():
            person_id = str(row["id"])
            name = row["name"]
            recommendations = session.execute_read(get_recommendations, person_id)

            if recommendations:
                for rec in recommendations:
                    results.append({
                        "person_id": person_id,
                        "name": name,
                        "recommended_job": rec["job_title"],
                        "matched_skills": ", ".join(rec["matched_skills"])
                    })
            else:
                results.append({
                    "person_id": person_id,
                    "name": name,
                    "recommended_job": "No Match",
                    "matched_skills": ""
                })

    # Simpan ke CSV
    output_df = pd.DataFrame(results)
    output_df.to_csv("output/job_recommendations.csv", index=False)
    print("✅ Rekomendasi disimpan ke job_recommendations.csv")

if __name__ == "__main__":
    recommend_and_save()