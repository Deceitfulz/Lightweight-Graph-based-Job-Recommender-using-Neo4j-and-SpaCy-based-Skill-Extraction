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

def recommend_and_print():
    # Ambil hanya 10 orang pertama
    people_df = pd.read_csv("data/processed/profiles_with_skills.csv").head(10)

    with driver.session() as session:
        for i, row in people_df.iterrows():
            person_id = str(row["id"])
            name = row["name"]
            recommendations = session.execute_read(get_recommendations, person_id)

            if recommendations:
                print(f"\n👤 {name} (ID: {person_id})")
                for rec in recommendations:
                    print(f"   → {rec['job_title']} (matched skills: {rec['matched_skills']})")
            else:
                print(f"\n👤 {name} (ID: {person_id}) — ❌ Tidak ada rekomendasi yang cocok.")

if __name__ == "__main__":
    recommend_and_print()