import streamlit as st
from pyvis.network import Network
import tempfile
from neo4j import GraphDatabase
import pandas as pd
from ast import literal_eval

# 🚀 HARUS PALING ATAS
st.set_page_config(page_title="Graph Job Recommender", layout="centered")

# Konfigurasi koneksi Neo4j
NEO4J_URL = "bolt://localhost:7687"
NEO4J_USERNAME = "nodes2025"
NEO4J_PASSWORD = "ihsanifan"

driver = GraphDatabase.driver(NEO4J_URL, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

def get_recommendations_for_person(tx, name):
    query = """
    MATCH (p:Person {name: $name})-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(j:Job)
    WITH j, collect(s.name) AS matchedSkills, count(s) AS score
    ORDER BY score DESC
    RETURN j.title AS job_title, matchedSkills
    LIMIT 5
    """
    result = tx.run(query, name=name)
    return result.data()

def get_person_skills(tx, name):
    query = """
    MATCH (p:Person {name: $name})-[:HAS_SKILL]->(s:Skill)
    RETURN collect(s.name) AS skills
    """
    result = tx.run(query, name=name)
    record = result.single()
    return record["skills"] if record else []

def visualize_graph(person_name, job_recs, skills):
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="black")

    # Tambahkan node Person
    net.add_node(person_name, label=person_name, shape="ellipse", color="lightblue")

    # Tambahkan node Skill dan edge dari Person
    for skill in skills:
        if skill:
            net.add_node(skill, label=skill, shape="box", color="lightgreen")
            net.add_edge(person_name, skill)

    existing_nodes = set(net.get_nodes())

    for job_title, matched_skills in job_recs:
        if not job_title:
            continue
        net.add_node(job_title, label=job_title, shape="ellipse", color="orange")

        # Pastikan matched_skills berupa list
        if isinstance(matched_skills, str):
            try:
                matched_skills = literal_eval(matched_skills)
            except:
                matched_skills = []

        for skill in matched_skills:
            if skill in existing_nodes:
                net.add_edge(skill, job_title)

    net.toggle_physics(True)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    html_content = net.generate_html()
    with open(tmp_file.name, "w", encoding="utf-8") as f:
        f.write(html_content)

    return tmp_file.name

# ================== UI Streamlit ==================

st.title("💼 Graph-based Job Recommender")
person_name = st.text_input("Enter person name:", value="Christian Zerial")

if st.button("Recommend Jobs"):
    with driver.session() as session:
        job_recs = session.read_transaction(get_recommendations_for_person, person_name)
        skills = session.read_transaction(get_person_skills, person_name)

    # Tampilkan tabel rekomendasi
    if job_recs:
        for i in range(len(job_recs)):
            # Ubah ke list Python jika masih string
            if isinstance(job_recs[i]["matchedSkills"], str):
                try:
                    job_recs[i]["matchedSkills"] = literal_eval(job_recs[i]["matchedSkills"])
                except:
                    job_recs[i]["matchedSkills"] = []

        df = pd.DataFrame(job_recs)
        df["matched_skills"] = df["matchedSkills"].apply(lambda x: ", ".join(x))
        df = df[["job_title", "matched_skills"]]
        st.subheader(f"Top job recommendations for {person_name}:")
        st.dataframe(df)

        # Visualisasi graf
        st.subheader("🕸️ Relationship Graph")
        html_path = visualize_graph(person_name, [(rec["job_title"], rec["matchedSkills"]) for rec in job_recs], skills)
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        st.components.v1.html(html_content, height=500)

    else:
        st.warning("No recommendations found.")
        
# Tambahkan footer di bagian paling akhir
st.markdown(
    "<hr style='margin-top: 3rem; margin-bottom: 0.5rem;'>"
    "<div style='text-align: center; color: grey;'>"
    "Powered by <b>Neo4j</b> + <b>Streamlit</b>"
    "</div>",
    unsafe_allow_html=True
)