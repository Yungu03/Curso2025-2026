#!/usr/bin/env python
# coding: utf-8

# **Task 06: Modifying RDF(s)**

# In[ ]:


import urllib.request
url = 'https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py'
urllib.request.urlretrieve(url, 'validation.py')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials"

# Import RDFLib main methods

# In[5]:


from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS
from validation import Report
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
r = Report()

# Create a new class named Researcher

# In[6]:


ns = Namespace("http://mydomain.org#")
g.add((ns.Researcher, RDF.type, RDFS.Class))
for s, p, o in g:
  print(s,p,o)

# **Task 6.0: Create new prefixes for "ontology" and "person" as shown in slide 14 of the Slidedeck 01a.RDF(s)-SPARQL shown in class.**

# In[ ]:


# this task is validated in the next step

# **TASK 6.1: Reproduce the taxonomy of classes shown in slide 34 in class (all the classes under "Vocabulario", Slidedeck: 01a.RDF(s)-SPARQL). Add labels for each of them as they are in the diagram (exactly) with no language tags. Remember adding the correct datatype (xsd:String) when appropriate**
# 

# In[7]:


# Create the class hierarchy
ontology = Namespace("http://oeg.fi.upm.es/def/people#")
person = ontology.Person
professor = ontology.Professor
associate_professor = ontology.AssociateProfessor
full_professor = ontology.FullProfessor
interim_associate_professor = ontology.InterimAssociateProfessor

# Add classes to the graph
g.add((person, RDF.type, RDFS.Class))
g.add((person, RDFS.label, Literal("Person", datatype=XSD.string)))

g.add((professor, RDF.type, RDFS.Class))
g.add((professor, RDFS.label, Literal("Professor", datatype=XSD.string)))
g.add((professor, RDFS.subClassOf, person))

g.add((associate_professor, RDF.type, RDFS.Class))
g.add((associate_professor, RDFS.label, Literal("AssociateProfessor", datatype=XSD.string)))
g.add((associate_professor, RDFS.subClassOf, professor))

g.add((full_professor, RDF.type, RDFS.Class))
g.add((full_professor, RDFS.label, Literal("FullProfessor", datatype=XSD.string)))
g.add((full_professor, RDFS.subClassOf, professor))

g.add((interim_associate_professor, RDF.type, RDFS.Class))
g.add((interim_associate_professor, RDFS.label, Literal("InterimAssociateProfessor", datatype=XSD.string)))
g.add((interim_associate_professor, RDFS.subClassOf, associate_professor))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# In[8]:


# Validation. Do not remove
r.validate_task_06_01(g)

# **TASK 6.2: Add the 3 properties shown in slide 36. Add labels for each of them (exactly as they are in the slide, with no language tags), and their corresponding domains and ranges using RDFS. Remember adding the correct datatype (xsd:String) when appropriate. If a property has no range, make it a literal (string)**

# In[9]:


# Create the properties
has_colleague = ontology.hasColleague
has_name = ontology.hasName
has_home_page = ontology.hasHomePage

# Add properties with labels and domain/range
g.add((has_colleague, RDF.type, RDF.Property))
g.add((has_colleague, RDFS.label, Literal("hasColleague", datatype=XSD.string)))
g.add((has_colleague, RDFS.domain, person))
g.add((has_colleague, RDFS.range, person))

g.add((has_name, RDF.type, RDF.Property))
g.add((has_name, RDFS.label, Literal("hasName", datatype=XSD.string)))
g.add((has_name, RDFS.domain, person))
g.add((has_name, RDFS.range, RDFS.Literal))

g.add((has_home_page, RDF.type, RDF.Property))
g.add((has_home_page, RDFS.label, Literal("hasHomePage", datatype=XSD.string)))
g.add((has_home_page, RDFS.domain, full_professor))
g.add((has_home_page, RDFS.range, RDFS.Literal))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# In[10]:


# Validation. Do not remove
r.validate_task_06_02(g)

# **TASK 6.3: Create the individuals shown in slide 36 under "Datos". Link them with the same relationships shown in the diagram."**

# In[11]:


# Create individuals
person_ns = Namespace("http://oeg.fi.upm.es/resource/person/")
oscar = person_ns.Oscar
asun = person_ns.Asun
raul = person_ns.Raul

# Add Oscar (AssociateProfessor)
g.add((oscar, RDF.type, associate_professor))
g.add((oscar, RDFS.label, Literal("Oscar", datatype=XSD.string)))
g.add((oscar, has_colleague, asun))
g.add((oscar, has_name, Literal("Oscar Corcho García", datatype=XSD.string)))

# Add Asun (FullProfessor)
g.add((asun, RDF.type, full_professor))
g.add((asun, RDFS.label, Literal("Asun", datatype=XSD.string)))
g.add((asun, has_colleague, raul))
g.add((asun, has_home_page, Literal("http://www.oeg-upm.net/", datatype=XSD.string)))

# Add Raul (InterimAssociateProfessor)
g.add((raul, RDF.type, interim_associate_professor))
g.add((raul, RDFS.label, Literal("Raul", datatype=XSD.string)))
g.add((raul, has_colleague, asun))
g.add((raul, has_name, Literal("Raul Moreno", datatype=XSD.string)))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# In[12]:


r.validate_task_06_03(g)

# **TASK 6.4: Add to the individual person:Oscar the email address, given and family names. Use the properties already included in example 4 to describe Jane and John (https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials/rdf/example4.rdf). Do not import the namespaces, add them manually**
# 

# In[13]:


# Add properties to Oscar using VCARD and FOAF namespaces
vcard = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
foaf = Namespace("http://xmlns.com/foaf/0.1/")

# Add email, given name and family name to Oscar
g.add((oscar, foaf.email, Literal("oscar@example.com", datatype=XSD.string)))
g.add((oscar, vcard.Given, Literal("Oscar", datatype=XSD.string)))
g.add((oscar, vcard.Family, Literal("Corcho García", datatype=XSD.string)))

# Visualize the results
for s, p, o in g:
  print(s,p,o)

# In[14]:


# Validation. Do not remove
r.validate_task_06_04(g)
r.save_report("_Task_06")
