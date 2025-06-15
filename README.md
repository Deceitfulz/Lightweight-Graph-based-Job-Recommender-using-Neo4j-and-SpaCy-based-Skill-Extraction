# Lightweight Graph-based Job Recommender using Neo4j and SpaCy-based Skill Extraction

This project is a lightweight, open-source job recommendation system that leverages graph-based modeling in Neo4j and natural language processing using spaCy to extract skills from user profiles and job postings. It aims to deliver efficient job recommendations by modeling relationships between people, skills, and jobs as a graph.

---

## 📌 Features

- Skill extraction from LinkedIn profiles and job descriptions using spaCy
- Graph construction in Neo4j: `Person`, `Job`, and `Skill` nodes with relationships like `HAS_SKILL`, `REQUIRES_SKILL`, and `RECOMMENDED_FOR`
- Querying job recommendations through Neo4j Cypher
- Lightweight, local-first, and LLM-free
- Open-source and reproducible using CSV data

---

## 🛠️ Tech Stack

| Component     | Tool                        |
|---------------|-----------------------------|
| Programming   | Python 3.10+                |
| NLP           | spaCy                       |
| Graph DB      | Neo4j (Bolt connection)     |
| Data Handling | pandas, csv                 |
| Visualization | Mermaid (Architecture Diagrams) |
| Versioning    | Git                         |

---

## 🗂️ Project Structure

├── extract_profile_skills.py # Extracts skills from LinkedIn profile data
├── extract_skills.py # NLP logic using spaCy
├── generate_job_skill_edges.py # Creates job-skill edges
├── generate_person_and_edges.py # Creates person nodes and their skill links
├── get_recommendation.py # Neo4j Cypher query to recommend jobs
├── get_recommendation_to_csv.py # Writes recommendation result to CSV
├── import_to_neo4j.py # Pushes nodes and edges to Neo4j
├── jobs.csv # Cleaned job postings
├── people.csv # Cleaned profile data
├── skills.csv # Unique extracted skills
├── person_has_skill.csv # Edges: Person -> Skill
├── job_requires_skill.csv # Edges: Job -> Skill
├── job_recommendations.csv # Output recommendation result
├── postings_with_skills.csv # Job postings with extracted skills
├── profiles_with_skills.csv # Profiles with extracted skills
├── skills_list.txt # Skill keyword reference
├── README.md # Project documentation


---

# 🚀 How to Run

1. Clone this repository

```
git clone https://github.com/Deceitfulz/graph-job-recommender.git
cd graph-job-recommender
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Prepare Neo4j database

- Run Neo4j locally and ensure Bolt connection is enabled

- Default credentials used in this project:

```
URL: bolt://localhost:7687
Username: nodes2025
Password: ihsanifan
```

4. Run the scripts
Make sure your working directory contains `postings.csv` and `LinkedIn people profiles datasets.csv`

```
python extract_profile_skills.py
python generate_person_and_edges.py
python extract_skills.py
python generate_job_skill_edges.py
python import_to_neo4j.py
python get_recommendation.py
```

# 📈 Example Output
Sample format from `job_recommendations.csv`:

| Person Name | Recommended Job Title | Score |
|---------------|-----------------------------| - |
| John Doe   | Data Engineer at ABC Tech                | 0.85 |
| Jane Smith           | Python Developer at XYZ                       | 0.78 |



# 📄 Dataset Source
- LinkedIn Job Posting Dataset (Kaggle)
https://www.kaggle.com/datasets/arshkon/linkedin-job-postings?select=postings.csv

- LinkedIn People Profiles Dataset (Kaggle)
https://www.kaggle.com/datasets/manishkumar7432698/linkedinuserprofiles?select=LinkedIn+people+profiles+datasets.csv

# 🤝 Acknowledgements
- spaCy
- Neo4j

Inspired by lightweight AI engineering and graph-based solutions for talent matching.

