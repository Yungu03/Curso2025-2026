# -*- coding: utf-8 -*-
"""
Task 07: Querying RDF(s)
Alumno: [Francisco de Borja Sánchez González]
ID: [220091]
"""

import urllib.request
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

# Descargar validación
url = 'https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/refs/heads/master/Assignment4/course_materials/python/validation.py'
urllib.request.urlretrieve(url, 'validation.py')
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials"

from validation import Report

# Inicializar grafo y cargar datos
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.parse(github_storage + "/rdf/data06.ttl", format="TTL")
report = Report()

# Namespace del dominio
people_ns = Namespace("http://oeg.fi.upm.es/def/people#")

print("=" * 70)
print("TASK 07: QUERYING RDF(s)")
print("=" * 70)

# =============================================================================
# TASK 7.1a: Listar clases y superclases con RDFLib
# =============================================================================

print("\n" + "=" * 70)
print("TASK 7.1a: Clases y superclases (RDFLib)")
print("=" * 70)

result = []

# Buscar todas las entidades que son clases
clases_encontradas = list(g.subjects(RDF.type, RDFS.Class))

# Para cada clase, buscar su superclase (si existe)
for clase in clases_encontradas:
    # Buscar superclase usando g.value (devuelve None si no existe)
    superclase = g.value(subject=clase, predicate=RDFS.subClassOf)
    
    # Añadir tupla (clase, superclase) al resultado
    result.append((clase, superclase))

# Visualizar resultados
print(f"\nTotal de clases encontradas: {len(result)}")
for clase, superclase in result:
    if superclase:
        print(f"  {clase.split('#')[-1]} -> subClassOf -> {superclase.split('#')[-1]}")
    else:
        print(f"  {clase.split('#')[-1]} (sin superclase)")

# Validación
report.validate_07_1a(result)

# =============================================================================
# TASK 7.1b: Repetir con SPARQL
# =============================================================================

print("\n" + "=" * 70)
print("TASK 7.1b: Clases y superclases (SPARQL)")
print("=" * 70)

query = """
SELECT DISTINCT ?c ?sc
WHERE {
    ?c rdf:type rdfs:Class .
    OPTIONAL {
        ?c rdfs:subClassOf ?sc .
    }
}
"""

print("\nResultados SPARQL:")
contador = 0
for resultado in g.query(query):
    contador += 1
    clase_nombre = resultado.c.split('#')[-1] if '#' in str(resultado.c) else str(resultado.c)
    if resultado.sc:
        sc_nombre = resultado.sc.split('#')[-1] if '#' in str(resultado.sc) else str(resultado.sc)
        print(f"  {clase_nombre} -> {sc_nombre}")
    else:
        print(f"  {clase_nombre} (raíz)")

print(f"\nTotal: {contador} clases")

# Validación
report.validate_07_1b(query, g)

# =============================================================================
# TASK 7.2a: Listar individuos de Person (RDFLib)
# =============================================================================

print("\n" + "=" * 70)
print("TASK 7.2a: Individuos de Person (RDFLib)")
print("=" * 70)

individuals = []

# Función recursiva para obtener todas las subclases (incluida la clase misma)
def obtener_subclases_recursivas(clase_base):
    """Devuelve un conjunto con la clase y todas sus subclases transitivamente"""
    subclases = {clase_base}
    
    # Buscar todas las clases que tienen clase_base como superclase
    for subclase in g.subjects(RDFS.subClassOf, clase_base):
        # Añadir la subclase y sus subclases recursivamente
        subclases.update(obtener_subclases_recursivas(subclase))
    
    return subclases

# Obtener Person y todas sus subclases
todas_clases_person = obtener_subclases_recursivas(people_ns.Person)

print(f"\nClases de Person encontradas: {len(todas_clases_person)}")
for clase in todas_clases_person:
    print(f"  - {clase.split('#')[-1]}")

# Buscar todos los individuos de estas clases
individuos_encontrados = set()
for clase in todas_clases_person:
    for individuo in g.subjects(RDF.type, clase):
        individuos_encontrados.add(individuo)

# Convertir a lista ordenada (para reproducibilidad)
individuals = sorted(list(individuos_encontrados), key=str)

print(f"\nIndividuos encontrados: {len(individuals)}")
for individuo in individuals:
    tipo = g.value(subject=individuo, predicate=RDF.type)
    tipo_nombre = tipo.split('#')[-1] if tipo else "?"
    print(f"  {individuo} (tipo: {tipo_nombre})")

# Validación
report.validate_07_02a(individuals)

# =============================================================================
# TASK 7.2b: Repetir con SPARQL
# =============================================================================

print("\n" + "=" * 70)
print("TASK 7.2b: Individuos de Person (SPARQL)")
print("=" * 70)

# Usar prepareQuery con initNs para definir el prefix
query = prepareQuery("""
SELECT DISTINCT ?ind
WHERE {
    ?ind rdf:type ?tipo .
    ?tipo rdfs:subClassOf* people:Person .
}
""", initNs={"people": people_ns, "rdf": RDF, "rdfs": RDFS})

print("\nResultados SPARQL:")
for resultado in g.query(query):
    print(f"  {resultado.ind}")

# Validación
report.validate_07_02b(g, query)

# =============================================================================
# TASK 7.3: Nombre y tipo de quienes conocen a Rocky (SPARQL)
# =============================================================================

print("\n" + "=" * 70)
print("TASK 7.3: Quién conoce a Rocky")
print("=" * 70)

query = prepareQuery("""
SELECT ?name ?type
WHERE {
    ?persona people:knows people:Rocky .
    ?persona rdf:type ?type .
    
    # Rocky puede tener nombre en hasName o en label
    {
        ?persona people:hasName ?name .
    }
    UNION
    {
        ?persona rdfs:label ?name .
    }
}
""", initNs={"people": people_ns, "rdf": RDF, "rdfs": RDFS})

print("\nPersonas que conocen a Rocky:")
for resultado in g.query(query):
    tipo_nombre = resultado.type.split('#')[-1] if '#' in str(resultado.type) else str(resultado.type)
    print(f"  {resultado.name} (tipo: {tipo_nombre})")

# Validación
report.validate_07_03(g, query)

# =============================================================================
# TASK 7.4: Colega con perro o colega de colega con perro (SPARQL)
# =============================================================================

print("\n" + "=" * 70)
print("TASK 7.4: Colegas con mascotas (perros)")
print("=" * 70)

query = prepareQuery("""
SELECT DISTINCT ?name
WHERE {
    ?persona rdfs:label ?name .
    
    # Tiene un colega (uno o más niveles)
    ?persona people:hasColleague+ ?colega_con_mascota .
    
    # Ese colega tiene una mascota
    ?colega_con_mascota people:ownsPet ?mascota .
}
""", initNs={"people": people_ns, "rdfs": RDFS})

print("\nPersonas con colegas que tienen mascotas:")
for resultado in g.query(query):
    print(f"  {resultado.name}")

# Validación
report.validate_07_04(g, query)

# =============================================================================
# Guardar reporte final
# =============================================================================

report.save_report("_Task_07")

print("\n" + "=" * 70)
print("TASK 07 COMPLETADA - Reporte guardado")
print("=" * 70)

# Estadísticas finales
print("\n📊 ESTADÍSTICAS DEL GRAFO:")
print(f"  Total de triples: {len(g)}")
print(f"  Total de clases: {len(list(g.subjects(RDF.type, RDFS.Class)))}")
print(f"  Total de individuos Person: {len(individuals)}")
