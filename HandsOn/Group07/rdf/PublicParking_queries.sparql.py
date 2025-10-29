from rdflib import Graph

# Cargar el archivo RDF
g = Graph()
g.parse("PublicParking.rdf.ttl", format="turtle")

print(f"Triples cargados: {len(g)}")

# ------------------------------
# QUERY 1 – Lista de aparcamientos con nombre
# ------------------------------
query1 = """
PREFIX mm: <http://movemadrid.org/ontology/movilidad#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?parking ?name
WHERE {
  ?parking a mm:CarParking ;
           mm:carParkingName ?name .
}
ORDER BY ?name
"""

# Ejecutar la query
print("\n--- QUERY 1 ---")
for row in g.query(query1):
    print(f"{row.parking} → {row.name}")

# ------------------------------
# QUERY 2 – Nombre, coordenadas y link
# ------------------------------
query2 = """
PREFIX mm: <http://movemadrid.org/ontology/movilidad#>

SELECT ?parking ?name ?lat ?long ?link
WHERE {
  ?parking a mm:CarParking ;
           mm:carParkingName ?name .
  OPTIONAL { ?parking mm:carParkingLatitude ?lat . }
  OPTIONAL { ?parking mm:carParkingLongitude ?long . }
  OPTIONAL { ?parking mm:carParkingLink ?link . }
}
ORDER BY ?name
"""

print("\n--- QUERY 2 ---")
for row in g.query(query2):
    print(f"{row.name} | lat={row.lat} | long={row.long} | link={row.link}")

# ------------------------------
# QUERY 3 – Aparcamientos por distrito
# ------------------------------
query3 = """
PREFIX mm: <http://movemadrid.org/ontology/movilidad#>

SELECT ?parking ?name ?district
WHERE {
  ?parking a mm:CarParking ;
           mm:carParkingName ?name ;
           mm:facilityDistrict ?district .
  FILTER(str(?district) = "USERA")
}
ORDER BY ?name
"""

print("\n--- QUERY 3 ---")
for row in g.query(query3):
    print(f"{row.name} ({row.district})")

# ------------------------------
# QUERY 4 – Extraer número de plazas desde la descripción
# ------------------------------
query4 = """
PREFIX mm: <http://movemadrid.org/ontology/movilidad#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?parking ?name ?desc
WHERE {
  ?parking a mm:CarParking ;
           mm:carParkingName ?name ;
           mm:carParkingDescription ?desc .
  FILTER(CONTAINS(?desc, "Plazas:"))
}
LIMIT 10
"""

print("\n--- QUERY 4 ---")
for row in g.query(query4):
    print(f"{row.name}: {row.desc}")
