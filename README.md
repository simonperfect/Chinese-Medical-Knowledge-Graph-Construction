# Chinese-Medical-Knowledge-Graph-Construction

A scalable, end-to-end Medical Knowledge Graph built with Python and Neo4j, storing structured relationships between Diseases, Symptoms, Drugs, Foods, and Medical Departments.

---

## 🌟 Key Highlights & Engineering Impact
- **Data Scale**: Successfully processed and ingested thousands of complex medical entities and relationships.
- **Performance Optimization**: 
  - Reduced graph ingestion time by **over 10x** by implementing **`UNWIND` parameterised batch operations** to mitigate network I/O overhead.
  - Implemented **schema indexing on entity names (`CREATE INDEX`)**, eliminating full table scans during relation matching ($O(1)$ lookup performance).
- **Architecture**: Containerised Neo4j setup with Docker, using Python `neo4j-driver` for automated batch ETL pipelines.

---

## Graph Visualization & Results

### 1. Medical Knowledge Graph Schema
<img width="1204" height="914" alt="image" src="https://github.com/user-attachments/assets/17b707c4-8e22-429b-b39e-1b63aa36a649" />

> *Example: Relationship network for Disease, showing Symptoms (`has_symptom`), Recommended Drugs (`recommand_drug`), and Food Constraints (`no_eat`).*

### 2. Knowledge Graph Statistics
- **Total Nodes**: ~XX,XXX+
- **Total Relationships**: ~XX,XXX+
- **Node Labels**: Disease, Drug, Food, Symptom, Check, Department, Producer.

---

## 🏗️ Knowledge Graph Ontology (Schema Design)

| Node Label | Description | Example Relationships |
| :--- | :--- | :--- |
| **Disease** | Central entity | `(Disease)-[:has_symptom]->(Symptom)` |
| **Drug** | Common or recommended medication | `(Disease)-[:recommand_drug]->(Drug)` |
| **Food** | Dietary recommendations/restrictions | `(Disease)-[:no_eat]->(Food)` |
| **Department** | Hospital medical department | `(Disease)-[:belongs_to]->(Department)` |

---

## 🛠️ Project Structure & Setup

```bash
.
├── main.py              # Main ETL pipeline with UNWIND batch ingestion & indexing logic
├── config.example.py    # Database connection configuration template
└── README.md            # Project documentation and visual showcase
temp.json is first 1000 examples of medical_json 
