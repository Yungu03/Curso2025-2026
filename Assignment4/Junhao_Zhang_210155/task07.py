#!/usr/bin/env python
# coding: utf-8

# **Task 07: Querying RDF(s)**

# In[1]:


#get_ipython().system('pip install rdflib')
import urllib.request
url = 'https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py'
urllib.request.urlretrieve(url, 'validation.py')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials"


# In[2]:


from validation import Report


# First let's read the RDF file

# In[3]:


from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
# Do not change the name of the variables
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.parse(github_storage+"/rdf/data06.ttl", format="TTL")
report = Report()


# **TASK 7.1a: For all classes, list each classURI. If the class belogs to another class, then list its superclass.**
# **Do the exercise in RDFLib returning a list of Tuples: (class, superclass) called "result". If a class does not have a super class, then return None as the superclass**

# In[4]:


# TO DO

# Obtener todas las clases definidas en el grafo
defined_classes = set(cls for cls in g.subjects(RDF.type, RDFS.Class))

# Lista de resultados
result = []
for class_uri in defined_classes:
    super_classes = list(g.objects(class_uri, RDFS.subClassOf))
    if super_classes:
        for parent_class in super_classes:
            result.append((class_uri, parent_class))
    else:
        result.append((class_uri, None))

# Visualize the results
for r in result:
  print(r)


# In[5]:


## Validation: Do not remove
report.validate_07_1a(result)


# **TASK 7.1b: Repeat the same exercise in SPARQL, returning the variables ?c (class) and ?sc (superclass)**

# In[6]:


query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?c ?sc
WHERE {
  ?c a rdfs:Class .
  OPTIONAL { ?c rdfs:subClassOf ?sc . }
}
"""

for r in g.query(query):
  print(r.c, r.sc)


# In[7]:


## Validation: Do not remove
report.validate_07_1b(query,g)


# **TASK 7.2a: List all individuals of "Person" with RDFLib (remember the subClasses). Return the individual URIs in a list called "individuals"**
# 

# In[8]:


ns = Namespace("http://oeg.fi.upm.es/def/people#")

# Obtener todas las subclases de Person
person_classes = set([ns.Person])
to_visit = [ns.Person]

while to_visit:
    current_class = to_visit.pop()
    for subclass in g.subjects(RDFS.subClassOf, current_class):
        if subclass not in person_classes:
            person_classes.add(subclass)
            to_visit.append(subclass)

# Recoger todos los individuos que pertenecen a esas clases
all_individuals = set()
for cls in person_classes:
    for individual in g.subjects(RDF.type, cls):
        all_individuals.add(individual)

# variable to return
individuals = list(all_individuals)
# visualize results
for i in individuals:
  print(i)


# In[9]:


# validation. Do not remove
report.validate_07_02a(individuals)


# **TASK 7.2b: Repeat the same exercise in SPARQL, returning the individual URIs in a variable ?ind**

# In[10]:


query = """
PREFIX ns: <http://oeg.fi.upm.es/def/people#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?ind
WHERE {
  ?ind rdf:type ?cls .
  ?cls rdfs:subClassOf* ns:Person .
}
"""

# Visualize the results
for r in g.query(query):
  print(r.ind)


# In[11]:


## Validation: Do not remove
report.validate_07_02b(g, query)


# **TASK 7.3:  List the name and type of those who know Rocky (in SPARQL only). Use name and type as variables in the query**

# In[12]:


# TO DO

query = """
PREFIX ns:   <http://oeg.fi.upm.es/def/people#>
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?type
WHERE {
  ?x ns:knows ns:Rocky .
  ?x rdf:type ?type .
  ?x rdfs:label ?name .
}
"""
# Visualize the results
for r in g.query(query):
  print(r.name, r.type)


# In[13]:


## Validation: Do not remove
report.validate_07_03(g, query)


# **Task 7.4: List the name of those entities who have a colleague with a dog, or that have a collegue who has a colleague who has a dog (in SPARQL). Return the results in a variable called name**

# In[14]:


# TO DO
query = """
PREFIX ns: <http://oeg.fi.upm.es/def/people#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?name
WHERE {
  {
    # Caso 1: el individuo tiene un colega con perro
    ?x ns:hasColleague ?y .
    ?y ns:ownsPet ?p .
    ?p rdf:type ns:Animal .
    ?x rdfs:label ?name .
  }
  UNION
  {
    # Caso 2: el individuo tiene un colega que tiene un colega con perro
    ?x ns:hasColleague ?y .
    ?y ns:hasColleague ?z .
    ?z ns:ownsPet ?p .
    ?p rdf:type ns:Animal .
    ?x rdfs:label ?name .
  }
}
"""

# Visualize the results
for r in g.query(query):
  print(r.name)


# In[15]:


## Validation: Do not remove
report.validate_07_04(g,query)
report.save_report("_Task_07")


# In[ ]:




