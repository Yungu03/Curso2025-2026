# -*- coding: utf-8 -*-
"""
Task 06: Modifying RDF(s)
Alumno: [Francisco de Borja Sáncehz González]
ID: [220091]
"""

import urllib.request
from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS

# Descargar validación
url = 'https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py'
urllib.request.urlretrieve(url, 'validation.py')

from validation import Report

# Inicializar grafo y reporte
g = Graph()
report = Report()

# =============================================================================
# TASK 6.0: Crear prefijos para ontology y person
# =============================================================================

# Definir namespaces según slide 14
ontology_ns = Namespace("http://oeg.fi.upm.es/def/people#")
person_ns = Namespace("http://oeg.fi.upm.es/resource/person/")

# Registrar prefijos en el grafo
g.bind("ontology", ontology_ns)
g.bind("person", person_ns)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)

print("=" * 60)
print("TASK 6.0: Prefijos creados correctamente")
print("=" * 60)

# =============================================================================
# TASK 6.1: Crear taxonomía de clases (slide 34)
# =============================================================================

# Lista de clases a crear
clases = [
    ("Person", None),  # Clase raíz
    ("Professor", "Person"),
    ("AssociateProfessor", "Professor"),
    ("FullProfessor", "Professor"),
    ("InterimAssociateProfessor", "AssociateProfessor")
]

# Iterar sobre cada clase
for nombre_clase, superclase in clases:
    clase_uri = ontology_ns[nombre_clase]
    
    # Añadir declaración de clase
    g.add((clase_uri, RDF.type, RDFS.Class))
    
    # Añadir label exacto con datatype xsd:string
    g.add((clase_uri, RDFS.label, Literal(nombre_clase, datatype=XSD.string)))
    
    # Si tiene superclase, añadir la relación de jerarquía
    if superclase:
        superclase_uri = ontology_ns[superclase]
        g.add((clase_uri, RDFS.subClassOf, superclase_uri))

print("\nTASK 6.1: Clases creadas")
print("-" * 60)
for s, p, o in g.triples((None, RDF.type, RDFS.Class)):
    print(f"Clase: {s}")

# Validación
report.validate_task_06_01(g)

# =============================================================================
# TASK 6.2: Crear 3 propiedades (slide 36)
# =============================================================================

# Definir propiedades con sus dominios y rangos
propiedades = [
    {
        "nombre": "hasColleague",
        "dominio": ontology_ns.Person,
        "rango": ontology_ns.Person
    },
    {
        "nombre": "hasName",
        "dominio": ontology_ns.Person,
        "rango": RDFS.Literal  # Literal (string)
    },
    {
        "nombre": "hasHomePage",
        "dominio": ontology_ns.FullProfessor,
        "rango": RDFS.Literal  # Literal (string)
    }
]

# Crear cada propiedad
for prop_info in propiedades:
    prop_uri = ontology_ns[prop_info["nombre"]]
    
    # Declarar como propiedad RDF
    g.add((prop_uri, RDF.type, RDF.Property))
    
    # Añadir label exacto
    g.add((prop_uri, RDFS.label, Literal(prop_info["nombre"], datatype=XSD.string)))
    
    # Definir dominio
    g.add((prop_uri, RDFS.domain, prop_info["dominio"]))
    
    # Definir rango
    g.add((prop_uri, RDFS.range, prop_info["rango"]))

print("\nTASK 6.2: Propiedades creadas")
print("-" * 60)
for s, p, o in g.triples((None, RDF.type, RDF.Property)):
    print(f"Propiedad: {s}")

# Validación
report.validate_task_06_02(g)

# =============================================================================
# TASK 6.3: Crear individuos y relaciones (slide 36)
# =============================================================================

# Definir individuos con sus tipos
individuos = {
    "Oscar": ontology_ns.AssociateProfessor,
    "Asun": ontology_ns.FullProfessor,
    "Raul": ontology_ns.InterimAssociateProfessor
}

# Crear cada individuo
for nombre, tipo_clase in individuos.items():
    individuo_uri = person_ns[nombre]
    
    # Declarar tipo (rdf:type)
    g.add((individuo_uri, RDF.type, tipo_clase))
    
    # Añadir label con el nombre
    g.add((individuo_uri, RDFS.label, Literal(nombre, datatype=XSD.string)))

# Añadir propiedades específicas a cada individuo
# Oscar: hasName, hasColleague -> Asun
g.add((person_ns.Oscar, ontology_ns.hasName, 
       Literal("Óscar Corcho García", datatype=XSD.string)))
g.add((person_ns.Oscar, ontology_ns.hasColleague, person_ns.Asun))

# Asun: hasHomePage, hasColleague -> Raul
g.add((person_ns.Asun, ontology_ns.hasHomePage, 
       Literal("http://oeg.fi.upm.es/", datatype=XSD.string)))
g.add((person_ns.Asun, ontology_ns.hasColleague, person_ns.Raul))

print("\nTASK 6.3: Individuos creados")
print("-" * 60)
for s, p, o in g.triples((None, RDF.type, None)):
    if person_ns in str(s):  # Solo mostrar individuos
        print(f"Individuo: {s} -> Tipo: {o}")

# Validación
report.validate_task_06_03(g)

# =============================================================================
# TASK 6.4: Añadir VCARD y FOAF a Oscar (sin importar namespaces)
# =============================================================================

# Crear namespaces manualmente (NO importar)
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")

# Añadir propiedades VCARD y FOAF a Oscar
g.add((person_ns.Oscar, FOAF.email, 
       Literal("oscar.corcho@upm.es", datatype=XSD.string)))
g.add((person_ns.Oscar, VCARD.Given, 
       Literal("Oscar", datatype=XSD.string)))
g.add((person_ns.Oscar, VCARD.Family, 
       Literal("Corcho", datatype=XSD.string)))

print("\nTASK 6.4: Propiedades VCARD y FOAF añadidas a Oscar")
print("-" * 60)
for s, p, o in g.triples((person_ns.Oscar, None, None)):
    print(f"{p} -> {o}")

# Validación
report.validate_task_06_04(g)

# =============================================================================
# Guardar reporte final
# =============================================================================
report.save_report("_Task_06")

print("\n" + "=" * 60)
print("TASK 06 COMPLETADA - Reporte guardado")
print("=" * 60)

# Visualización final opcional (comentado para no saturar output)
# print("\nGrafo completo:")
# print(g.serialize(format="turtle"))
