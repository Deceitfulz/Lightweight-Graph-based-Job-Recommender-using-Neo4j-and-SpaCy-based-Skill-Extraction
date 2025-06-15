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

## 🧠 System Architecture

![System Architecture](assets/Architecture.svg)

---

## 🗂️ Project Structure

├── scripts/
│   ├── extract_profile_skills.py
│   ├── extract_skills.py
│   ├── generate_job_skill_edges.py
│   ├── generate_person_and_edges.py
│   ├── import_to_neo4j.py
│   ├── get_recommendation.py
│   └── get_recommendation_to_csv.py
├── data/
│   ├── raw/
│   │   ├── LinkedIn people profiles datasets.csv
│   │   └── postings.csv
│   └── processed/
│       ├── profiles_with_skills.csv
│       ├── postings_with_skills.csv
│       ├── people.csv
│       ├── jobs.csv
│       ├── skills.csv
│       ├── person_has_skill.csv
│       └── job_requires_skill.csv
├── graph/
│   └── skills_list.txt
├── output/
│   └── job_recommendations.csv
├── assets/
│   └── Architecture.svg
└── README.md


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

