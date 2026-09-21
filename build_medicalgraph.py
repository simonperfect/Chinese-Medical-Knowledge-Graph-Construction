import json
import os
from config import NEO4J_CONFIG
from neo4j import GraphDatabase

driver = GraphDatabase.driver(**NEO4J_CONFIG)


# Main Knowledge Graph Class
class MedicalGraph:

    def __init__(self):
        cur_dir = "/".join(os.path.abspath(__file__).split("/")[:-1])
        self.data_path = os.path.join(cur_dir, "data/medical.json")

    # Read data from JSON file
    def read_nodes(self):
        # Entity categories
        drugs = []  # Drugs
        foods = []  # Foods
        diseases = []  # Diseases
        symptoms = []  # Symptoms
        checks = []  # Diagnostic checks
        departments = []  # Hospital departments
        producers = []  # Drug manufacturers/producers
        disease_infos = []  # Detailed disease metadata

        # Relationship arrays
        rels_recommandeat = []
        rels_recommanddrug = []
        rels_symptom = []
        rels_department = []
        rels_noteat = []
        rels_doeat = []
        rels_commanddrug = []
        rels_check = []
        rels_drug_producer = []
        rels_acompany = []
        rels_category = []

        count = 0
        for data in open(self.data_path):
            disease_dict = {}
            count += 1
            if count % 500 == 0:
                print("count = ", count)

            # Parse JSON record
            data_json = json.loads(data)
            disease = data_json["name"]
            diseases.append(disease)

            disease_dict["name"] = disease
            disease_dict["desc"] = ""
            disease_dict["prevent"] = ""
            disease_dict["cause"] = ""
            disease_dict["easy_get"] = ""
            disease_dict["cure_department"] = ""
            disease_dict["cure_way"] = ""
            disease_dict["cure_lasttime"] = ""
            disease_dict["symptom"] = ""
            disease_dict["cured_prob"] = ""

            if "symptom" in data_json:
                symptoms += data_json["symptom"]
                for symptom in data_json["symptom"]:
                    rels_symptom.append([disease, symptom])

            if "acompany" in data_json:
                for acompany in data_json["acompany"]:
                    rels_acompany.append([disease, acompany])

            if "desc" in data_json:
                disease_dict["desc"] = data_json["desc"]

            if "prevent" in data_json:
                disease_dict["prevent"] = data_json["prevent"]

            if "cause" in data_json:
                disease_dict["cause"] = data_json["cause"]

            if "get_prob" in data_json:
                disease_dict["get_prob"] = data_json["get_prob"]

            if "easy_get" in data_json:
                disease_dict["easy_get"] = data_json["easy_get"]

            if "cure_department" in data_json:
                cure_department = data_json["cure_department"]
                if len(cure_department) == 1:
                    rels_category.append([disease, cure_department[0]])
                if len(cure_department) == 2:
                    big = cure_department[0]
                    small = cure_department[1]
                    rels_department.append([small, big])
                    rels_category.append([disease, small])
                disease_dict["cure_department"] = cure_department
                departments += cure_department

            if "cure_way" in data_json:
                disease_dict["cure_way"] = data_json["cure_way"]

            if "cure_lasttime" in data_json:
                disease_dict["cure_lasttime"] = data_json["cure_lasttime"]

            if "cured_prob" in data_json:
                disease_dict["cured_prob"] = data_json["cured_prob"]

            if "common_drug" in data_json:
                common_drug = data_json["common_drug"]
                for drug in common_drug:
                    rels_commanddrug.append([disease, drug])
                drugs += common_drug

            if "recommand_drug" in data_json:
                recommand_drug = data_json["recommand_drug"]
                drugs += recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease, drug])

            if "not_eat" in data_json:
                not_eat = data_json["not_eat"]
                for _not in not_eat:
                    rels_noteat.append([disease, _not])
                foods += not_eat

                do_eat = data_json["do_eat"]
                for _do in do_eat:
                    rels_doeat.append([disease, _do])
                foods += do_eat

                recommand_eat = data_json["recommand_eat"]
                for _recommand in recommand_eat:
                    rels_recommandeat.append([disease, _recommand])
                foods += recommand_eat

            if "check" in data_json:
                check = data_json["check"]
                for _check in check:
                    rels_check.append([disease, _check])
                checks += check

            if "drug_detail" in data_json:
                drug_detail = data_json["drug_detail"]
                producer = [i.split("(")[0] for i in drug_detail]
                rels_drug_producer += [
                    [i.split("(")[0], i.split("(")[-1].replace(")", "")]
                    for i in drug_detail
                ]
                producers += producer

            disease_infos.append(disease_dict)

        return (
            set(drugs),
            set(foods),
            set(checks),
            set(departments),
            set(producers),
            set(symptoms),
            set(diseases),
            disease_infos,
            rels_check,
            rels_recommandeat,
            rels_noteat,
            rels_doeat,
            rels_department,
            rels_commanddrug,
            rels_drug_producer,
            rels_recommanddrug,
            rels_symptom,
            rels_acompany,
            rels_category,
        )

    # Create graph nodes and relationships in Neo4j
    def create_graphnodes_and_graphrels(self):
        (
            Drugs,
            Foods,
            Checks,
            Departments,
            Producers,
            Symptoms,
            Diseases,
            disease_infos,
            rels_check,
            rels_recommandeat,
            rels_noteat,
            rels_doeat,
            rels_department,
            rels_commanddrug,
            rels_drug_producer,
            rels_recommanddrug,
            rels_symptom,
            rels_acompany,
            rels_category,
        ) = self.read_nodes()

        # Print data statistics
        print("Drugs: ", len(Drugs))
        print("Foods: ", len(Foods))
        print("Checks: ", len(Checks))
        print("Departments: ", len(Departments))
        print("Producers: ", len(Producers))
        print("Symptoms: ", len(Symptoms))
        print("Diseases: ", len(Diseases))

        print("-------------------------------------------------------------")
        print("rels_check: ", len(rels_check))
        print("rels_recommandeat: ", len(rels_recommandeat))
        print("rels_noteat: ", len(rels_noteat))
        print("rels_doeat: ", len(rels_doeat))
        print("rels_department: ", len(rels_department))
        print("rels_commanddrug: ", len(rels_commanddrug))
        print("rels_drug_producer: ", len(rels_drug_producer))
        print("rels_recommanddrug: ", len(rels_recommanddrug))
        print("rels_symptom: ", len(rels_symptom))
        print("rels_acompany: ", len(rels_acompany))
        print("rels_category: ", len(rels_category))

        # Instantiate Neo4j driver
        driver = GraphDatabase.driver(**NEO4J_CONFIG)
        with driver.session() as session:
            # Create central Disease nodes
            print("Creating Disease nodes...")
            n = 0
            m = 0
            for d in disease_infos:
                cypher = (
                    "MERGE (a:Disease{name:%r, desc:%r, prevent:%r, cause:%r, "
                    "easy_get:%r, cure_lasttime:%r, cure_department:%r, cure_way:%r, cure_prob:%r})"
                    % (
                        d["name"],
                        d["desc"],
                        d["prevent"],
                        d["cause"],
                        d["easy_get"],
                        d["cure_lasttime"],
                        d["cure_department"],
                        d["cure_way"],
                        d["cured_prob"],
                    )
                )

                try:
                    session.run(cypher)
                except:
                    m += 1
                    pass

                n += 1
            print(
                "Disease nodes created in Neo4j: total {}, ERROR {}.".format(
                    n, m
                )
            )
            print("---------------$$$$$$$$$$$$--------------------")

            # Create Drug, Food, Symptom, Check, Department, and Producer nodes
            print("Creating Drug nodes...")
            count, err = 0, 0
            for n in Drugs:
                cypher = "MERGE (a:Drug{name:%r}) RETURN a" % n
                count += 1
                try:
                    session.run(cypher)
                except:
                    err += 1
                    pass
            print("Drug nodes, count={}, error={}".format(count, err))
            print("-----------------------------------------------")

            count, err = 0, 0
            print("Creating Food nodes...")
            for n in Foods:
                cypher = "MERGE (a:Food{name:%r}) RETURN a" % n
                count += 1
                try:
                    session.run(cypher)
                except:
                    err += 1
                    pass
            print("Food nodes, count={}, error={}".format(count, err))
            print("-----------------------------------------------")

            count, err = 0, 0
            print("Creating Symptom nodes...")
            for n in Symptoms:
                cypher = "MERGE (a:Symptom{name:%r}) RETURN a" % n
                count += 1
                try:
                    session.run(cypher)
                except:
                    err += 1
                    pass
            print("Symptom nodes, count={}, error={}".format(count, err))
            print("-----------------------------------------------")

            count, err = 0, 0
            print("Creating Check nodes...")
            for n in Checks:
                cypher = "MERGE (a:Check{name:%r}) RETURN a" % n
                count += 1
                try:
                    session.run(cypher)
                except:
                    err += 1
                    pass
            print("Check nodes, count={}, error={}".format(count, err))
            print("-----------------------------------------------")

            count, err = 0, 0
            print("Creating Department nodes...")
            for n in Departments:
                cypher = "MERGE (a:Department{name:%r}) RETURN a" % n
                count += 1
                try:
                    session.run(cypher)
                except:
                    err += 1
                    pass
            print("Department nodes, count={}, error={}".format(count, err))
            print("-----------------------------------------------")

            count, err = 0, 0
            print("Creating Producer nodes...")
            for n in Producers:
                cypher = "MERGE (a:Producer{name:%r}) RETURN a" % n
                count += 1
                try:
                    session.run(cypher)
                except:
                    err += 1
                    pass
            print("Producer nodes, count={}, error={}".format(count, err))
            print("-----------------------------------------------")

        # Create relationship edges
        self.create_relationship(
            "Disease",
            "Food",
            rels_recommandeat,
            "recommand_eat",
            "Recommended Recipe",
        )
        self.create_relationship(
            "Disease",
            "Drug",
            rels_recommanddrug,
            "recommand_drug",
            "Recommended Drug",
        )
        self.create_relationship(
            "Disease", "Symptom", rels_symptom, "has_symptom", "Symptom"
        )
        self.create_relationship(
            "Disease", "Food", rels_noteat, "no_eat", "Food Constraint"
        )
        self.create_relationship(
            "Disease", "Food", rels_doeat, "do_eat", "Food Preference"
        )
        self.create_relationship(
            "Disease",
            "Drug",
            rels_commanddrug,
            "command_drug",
            "Common Drug",
        )
        self.create_relationship(
            "Disease",
            "Drug",
            rels_drug_producer,
            "drugs_of",
            "Drug Manufacturer",
        )
        self.create_relationship(
            "Disease",
            "Check",
            rels_check,
            "need_check",
            "Diagnostic Check",
        )
        self.create_relationship(
            "Disease",
            "Disease",
            rels_acompany,
            "acompany_with",
            "Complication",
        )
        self.create_relationship(
            "Disease",
            "Department",
            rels_category,
            "belongs_to",
            "Department",
        )

    # Helper method to create relationship edges
    def create_relationship(
        self, start_node, end_node, edges, rel_type, rel_name
    ):
        # Deduplicate relationships
        set_edges = []
        for edge in edges:
            set_edges.append("###".join(edge))
        num_edges = len(set(set_edges))
        print("Creating relationship {}, num_edges = {}".format(rel_name, num_edges))

        # Instantiate Neo4j driver
        driver = GraphDatabase.driver(**NEO4J_CONFIG)
        with driver.session() as session:
            n, m = 0, 0
            for edge in set(set_edges):
                edge = edge.split("###")
                p = edge[0]
                q = edge[1]

                # Match nodes and create the relationship tuple
                cypher = (
                    "match(p:%s), (q:%s) where p.name='%s' and q.name='%s' create "
                    "(p)-[rel:%s{name:'%s'}]->(q)"
                    % (start_node, end_node, p, q, rel_type, rel_name)
                )
                try:
                    n += 1
                    session.run(cypher)
                except Exception as e:
                    m += 1

                if n % 5000 == 0:
                    print("n = ", n)
            print(
                "Current relationship: {}, processed: {}, errors: {}".format(
                    rel_name, n, m
                )
            )
            print(
                "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            )
        return


if __name__ == "__main__":
    mg = MedicalGraph()
    print("Starting knowledge graph creation (nodes and relationships)...")
    mg.create_graphnodes_and_graphrels()