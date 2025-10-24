from faker import Faker
import csv
from utils import (
    gen_list_persons,
    gen_list_organizations,
    gen_list_papers,
    compl_nodes,
    gen_list_works_at,
    gen_list_has_written,
    gen_list_has_read,
)

counter = 0

# Generate the fakers
fake_en = Faker("en")
fake_fr = Faker("fr")
fake_it = Faker("it")
fake_de = Faker("de")
fake_es = Faker("es")
fake_pt = Faker("pt")

# Generate the nodes (~1M)
# ------------------
nodes = list()

# 600k persons
print("generate 600k persons...")
persons_en, counter = gen_list_persons(150000, fake_en, counter)
persons_fr, counter = gen_list_persons(110000, fake_fr, counter)
persons_it, counter = gen_list_persons(100000, fake_it, counter)
persons_de, counter = gen_list_persons(90000, fake_de, counter)
persons_es, counter = gen_list_persons(70000, fake_es, counter)
persons_pt, counter = gen_list_persons(80000, fake_pt, counter)

persons_en_ids = list(persons_en.keys())
persons_fr_ids = list(persons_fr.keys())
persons_it_ids = list(persons_it.keys())
persons_de_ids = list(persons_de.keys())
persons_es_ids = list(persons_es.keys())
persons_pt_ids = list(persons_pt.keys())

# max(50k) organisations
print("generate max(50k) organizations...")
organizations_en, counter = gen_list_organizations(15000, fake_en, counter)
organizations_fr, counter = gen_list_organizations(10000, fake_fr, counter)
organizations_it, counter = gen_list_organizations(8000, fake_it, counter)
organizations_de, counter = gen_list_organizations(5000, fake_de, counter)
organizations_es, counter = gen_list_organizations(7000, fake_es, counter)
organizations_pt, counter = gen_list_organizations(5000, fake_pt, counter)

organizations_en_ids = list(organizations_en.keys())
organizations_fr_ids = list(organizations_fr.keys())
organizations_it_ids = list(organizations_it.keys())
organizations_de_ids = list(organizations_de.keys())
organizations_es_ids = list(organizations_es.keys())
organizations_pt_ids = list(organizations_pt.keys())

# Generate 360k papers
print("generate 360k papers...")
papers_en, counter = gen_list_papers(180000, fake_en, counter)
papers_fr, counter = gen_list_papers(40000, fake_fr, counter)
papers_it, counter = gen_list_papers(40000, fake_it, counter)
papers_de, counter = gen_list_papers(40000, fake_de, counter)
papers_es, counter = gen_list_papers(40000, fake_en, counter)
papers_pt, counter = gen_list_papers(180000, fake_pt, counter)

papers_en_ids = list(papers_en.keys())
papers_fr_ids = list(papers_fr.keys())
papers_it_ids = list(papers_it.keys())
papers_de_ids = list(papers_de.keys())
papers_es_ids = list(papers_es.keys())
papers_pt_ids = list(papers_pt.keys())

# Complete nodes
print("complete nodes...")
compl_nodes(
    nodes,
    [persons_en, persons_fr, persons_it, persons_de, persons_es, persons_pt],
    "Person",
)
compl_nodes(
    nodes,
    [
        organizations_en,
        organizations_fr,
        organizations_it,
        organizations_de,
        organizations_es,
        organizations_pt,
    ],
    "Org",
)
compl_nodes(
    nodes,
    [papers_en, papers_fr, papers_it, papers_de, papers_es, papers_pt],
    "Paper",
)

# Store in csv
with open("data/raw/nodes.csv", "w", newline="") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",")
    spamwriter.writerow(["id", "label", "name"])
    for row in nodes:
        spamwriter.writerow(row.values())

# Generate edges (~5M)
# --------------
edges = list()

# Generate "works at" relation for each persons
print("generate 'works at' relations...")
gen_list_works_at(
    edges,
    [persons_en, persons_fr, persons_it, persons_de, persons_es, persons_pt],
    [
        organizations_en_ids,
        organizations_fr_ids,
        organizations_it_ids,
        organizations_de_ids,
        organizations_es_ids,
        organizations_pt_ids,
    ],
)

# Generate 1.1M "has written" relations
print("generate 1.1M 'has written' relations...")
gen_list_has_written(
    edges,
    [300000, 250000, 150000, 200000, 150000, 50000],
    [
        persons_en_ids,
        persons_fr_ids,
        persons_it_ids,
        persons_de_ids,
        persons_es_ids,
        persons_pt_ids,
    ],
    [
        papers_en_ids,
        papers_fr_ids,
        papers_it_ids,
        papers_de_ids,
        papers_es_ids,
        papers_pt_ids,
    ],
)

# Generate 2.8M "has red" relations
print("generate 2.8M 'has read' relations...")
gen_list_has_read(
    edges,
    [500000, 500000, 400000, 500000, 500000, 400000],
    [
        persons_en_ids,
        persons_fr_ids,
        persons_it_ids,
        persons_de_ids,
        persons_es_ids,
        persons_pt_ids,
    ],
    [
        papers_en_ids,
        papers_fr_ids,
        papers_it_ids,
        papers_de_ids,
        papers_es_ids,
        papers_pt_ids,
    ],
)
# Pollute edges
my_dict = dict()
my_dict["src"] = ''
my_dict["dst"] = 48645
my_dict["type"] = "Parasite1"
edges.append(my_dict)
my_dict = dict()
my_dict["src"] = ''
my_dict["dst"] = ''
my_dict["type"] = "Parasite2"
edges.append(my_dict)
my_dict = dict()
my_dict["src"] = 468464
my_dict["dst"] = ''
my_dict["type"] = "Parasite3"
edges.append(my_dict)
my_dict = dict()
my_dict["src"] = ''
my_dict["dst"] = 378385
my_dict["type"] = "Parasite4"
edges.append(my_dict)
my_dict = dict()
my_dict["src"] = ''
my_dict["dst"] = 48645
my_dict["type"] = "Parasite5"
edges.append(my_dict)

# Store in csv
with open("data/raw/edges.csv", "w", newline="") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=",")
    spamwriter.writerow(["src", "dst", "type"])
    for row in edges:
        spamwriter.writerow(row.values())
