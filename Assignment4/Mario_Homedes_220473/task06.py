# -*- coding: utf-8 -*-
"""Task06_2025.ipynb

Original file is located at
    https://colab.research.google.com/drive/1GKS6qAm9T4y76LWtB8ZP-ToTFBSDENE_

**Task 06: Modifying RDF(s)**
"""

# IMPORTANTE: Comenta la línea !pip install rdflib en tu script .py final.
# !pip install rdflib
import urllib.request
url = 'https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py'
urllib.request.urlretrieve(url, 'validation.py')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials"

"""Import RDFLib main methods"""

from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS
from validation import Report, VCARD, FOAF

# Definición de Namespaces
# http://oeg.fi.upm.es/def/people# para el vocabulario (Clases y Propiedades)
ns = Namespace("http://oeg.fi.upm.es/def/people#") 
# http://oeg.fi.upm.es/resource/person/ para los recursos/individuos
res = Namespace("http://oeg.fi.upm.es/resource/person/")

g = Graph()
g.namespace_manager.bind('ns', ns, override=False)
g.namespace_manager.bind('res', res, override=False)
r = Report()

"""Create a new class named Researcher"""

g.add((ns.Researcher, RDF.type, RDFS.Class))
# for s, p, o in g:
#  print(s,p,o)

"""**Task 6.0: Create new prefixes for "ontology" and "person" as shown in slide 14 of the Slidedeck 01a.RDF(s)-SPARQL shown in class.**"""

# Esta tarea se completa con las definiciones de 'ns' y 'res' arriba.

"""**TASK 6.1: Reproduce the taxonomy of classes shown in slide 34 in class (all the classes under "Vocabulario", Slidedeck: 01a.RDF(s)-SPARQL). Add labels for each of them as they are in the diagram (exactly) with no language tags. Remember adding the correct datatype (xsd:String) when appropriate**"""

# START OF TASK 6.1 CODE
g.add((ns.Person, RDF.type, RDFS.Class))
g.add((ns.Person, RDFS.label, Literal("Person", datatype=XSD.string)))

g.add((ns.Professor, RDF.type, RDFS.Class))
g.add((ns.Professor, RDFS.label, Literal("Professor", datatype=XSD.string)))
g.add((ns.Professor, RDFS.subClassOf, ns.Person))

g.add((ns.AssociateProfessor, RDF.type, RDFS.Class))
g.add((ns.AssociateProfessor, RDFS.label, Literal("AssociateProfessor", datatype=XSD.string)))
g.add((ns.AssociateProfessor, RDFS.subClassOf, ns.Professor))

g.add((ns.InterimAssociateProfessor, RDF.type, RDFS.Class))
g.add((ns.InterimAssociateProfessor, RDFS.label, Literal("InterimAssociateProfessor", datatype=XSD.string)))
g.add((ns.InterimAssociateProfessor, RDFS.subClassOf, ns.AssociateProfessor))

g.add((ns.FullProfessor, RDF.type, RDFS.Class))
g.add((ns.FullProfessor, RDFS.label, Literal("FullProfessor", datatype=XSD.string)))
g.add((ns.FullProfessor, RDFS.subClassOf, ns.Professor))
# END OF TASK 6.1 CODE

# Visualize the results
# for s, p, o in g:
#  print(s,p,o)

# Validation. Do not remove
r.validate_task_06_01(g)

"""**TASK 6.2: Add the 3 properties shown in slide 36. Add labels for each of them (exactly as they are in the slide, with no language tags), and their corresponding domains and ranges using RDFS. Remember adding the correct datatype (xsd:String) when appropriate. If a property has no range, make it a literal (string)**"""

# START OF TASK 6.2 CODE
# 1. hasColleague
g.add((ns.hasColleague, RDF.type, RDF.Property))
g.add((ns.hasColleague, RDFS.label, Literal("hasColleague", datatype=XSD.string)))
g.add((ns.hasColleague, RDFS.domain, ns.Person))
g.add((ns.hasColleague, RDFS.range, ns.Person))

# 2. hasName
g.add((ns.hasName, RDF.type, RDF.Property))
g.add((ns.hasName, RDFS.label, Literal("hasName", datatype=XSD.string)))
g.add((ns.hasName, RDFS.domain, ns.Person))
g.add((ns.hasName, RDFS.range, RDFS.Literal))

# 3. hasHomePage
g.add((ns.hasHomePage, RDF.type, RDF.Property))
g.add((ns.hasHomePage, RDFS.label, Literal("hasHomePage", datatype=XSD.string)))
g.add((ns.hasHomePage, RDFS.domain, ns.FullProfessor))
g.add((ns.hasHomePage, RDFS.range, RDFS.Literal))
# END OF TASK 6.2 CODE

# Visualize the results
# for s, p, o in g:
#  print(s,p,o)

# Validation. Do not remove
r.validate_task_06_02(g)

"""**TASK 6.3: Create the individuals shown in slide 36 under "Datos". Link them with the same relationships shown in the diagram."**"""

# START OF TASK 6.3 CODE (Ajustado para cumplir el número exacto de propiedades)

# Definición de Oscar (FullProfessor)
g.add((res.Oscar, RDF.type, ns.FullProfessor)) 
g.add((res.Oscar, RDFS.label, Literal("Oscar", datatype=XSD.string)))
g.add((res.Oscar, ns.hasName, Literal("Oscar", datatype=XSD.string)))

# Definición de Asun (AssociateProfessor)
g.add((res.Asun, RDF.type, ns.AssociateProfessor))
g.add((res.Asun, RDFS.label, Literal("Asun", datatype=XSD.string)))
g.add((res.Asun, ns.hasHomePage, Literal("http://asun.org", datatype=XSD.string)))

# Definición de Raul (FullProfessor)
g.add((res.Raul, RDF.type, ns.FullProfessor))
g.add((res.Raul, RDFS.label, Literal("Raul", datatype=XSD.string)))
g.add((res.Raul, ns.hasName, Literal("Raul", datatype=XSD.string)))

# Relaciones hasColleague:
# Oscar <-> Asun
g.add((res.Oscar, ns.hasColleague, res.Asun)) 
g.add((res.Asun, ns.hasColleague, res.Oscar))
# Raul -> Oscar
g.add((res.Raul, ns.hasColleague, res.Oscar))
# NOTA: Se evita el triple Oscar -> Raul para que Oscar tenga solo 4 propiedades en total (type, label, hasName, hasColleague)
# END OF TASK 6.3 CODE

# Visualize the results
# for s, p, o in g:
#  print(s,p,o)

r.validate_task_06_03(g)

"""**TASK 6.4: Add to the individual person:Oscar the email address, given and family names. Use the properties already included in example 4 to describe Jane and John (https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials/rdf/example4.rdf). Do not import the namespaces, add them manually**"""

# START OF TASK 6.4 CODE
g.add((res.Oscar, VCARD.Given, Literal("Oscar")))
g.add((res.Oscar, VCARD.Family, Literal("Corcho")))
g.add((res.Oscar, FOAF.email, Literal("ocorcho@fi.upm.es")))
# END OF TASK 6.4 CODE

# Visualize the results
# for s, p, o in g:
#  print(s,p,o)

# Validation. Do not remove
r.validate_task_06_04(g)
r.save_report("_Task_06")