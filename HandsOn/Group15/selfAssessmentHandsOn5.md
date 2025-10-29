
# selfAssessmentHandsOn5

- ✅ JSON de operaciones OpenRefine con pasos para enriquecer datos de `stops` (añadir URIs de Wikidata y DBpedia para Madrid).
- ✅ CSVs actualizados con sufijo `-with-links.csv`.
- ✅ Mapeo RML (`gtfs-with-links.rml.ttl`) que genera:
  - `ex:Stop` y su relación `ex:inCity`.
  - Recurso `ex:city/Madrid` con `owl:sameAs` a Wikidata y DBpedia.
- ✅ RDF de ejemplo (`gtfs-with-links.ttl`) y consultas SPARQL para validación.
- 🔁 Para el dataset definitivo, basta con sustituir/añadir filas en `csv/` y volver a ejecutar el mapeo.
