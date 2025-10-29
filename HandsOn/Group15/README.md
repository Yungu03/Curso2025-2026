# Group15

**Members**  
- Francisco de Borjan Sánchez González — GitHub: **fransanchez6**
- Alberto Aragón Calvo — GitHub: **Abielmenda** 
- Ester Alvarez García — GitHub: **esteralvarez1**
- Joan Fernando Moncayo Pozo — GitHub: **Fentro2121**
- ChengJian Zhou — GitHub: **ChengJianZhou**

## Chosen domain
**Smart City → Environmental monitoring (Air Quality in Madrid).**

## Selected dataset(s)
- **Calidad del aire Madrid (mediciones diarias)** — Ayuntamiento de Madrid (CSV abierto).  
  Portal: https://datos.madrid.es  
  Ejemplo de recurso mensual CSV (septiembre 2025):  
  https://datos.madrid.es/FWProjects/egob/Catalogo/MedioAmbiente/CalidadAire/CalidadAireDiaria/Ficheros/2025/202509_calidad_aire.csv

> Nota: Los CSV reales son pesados; en este repo incluimos una **muestra representativa** en `csv/madrid_air_quality_sample.csv` para revisión rápida.

**Deliverables**
- `analysis.html`
- `ontology/ontology.ttl`
- `ontology/ontology-example.ttl`
- `selfAssessmentHandsOn2.md`

**Notes**
- URIs follow slash strategy and persistence policy.
- Data sets have linkability by location properties.
- License requires atribution and can be redistributed and comerciated

# Group15 — Hands-on 4: RML mappings

Run with RMLMapper (example):
```
java -jar rmlmapper.jar -m mappings/gtfs-madrid.rml.ttl -o rdf/out.ttl
```
Expected CSVs (from HandsOn3) under `csv/`: `stops-updated.csv`, `routes-updated.csv`, `stop_times-updated.csv`.

# Group15 — Hands-on 5: Data Linking

This folder contains the deliverables for **Session 10: Data Linking**.  
Dataset family: **GTFS Madrid (stops/routes/stop_times)**.

## What we linked
- We link each `Stop` to the **City of Madrid** via `ex:inCity`.
- We assert external identity links for that city:  
  `owl:sameAs` → Wikidata **Q2807** and DBpedia **dbr:Madrid**.

## How to regenerate RDF
We used RML-style mappings (CSV logical sources). To materialize them you can use any RML engine (e.g., RMLMapper):

```bash
java -jar rmlmapper.jar   -m mappings/gtfs-with-links.rml.ttl   -o rdf/out.nt -s ntriples
```

or Turtle:

```bash
java -jar rmlmapper.jar   -m mappings/gtfs-with-links.rml.ttl   -o rdf/out.ttl -s turtle
```

## Files
- `csv/*-with-links.csv` — CSVs enriched for linking
- `openrefine/stops-with-links.json` — recipe of operations applied
- `mappings/gtfs-with-links.rml.ttl` — RML mappings including `owl:sameAs`
- `rdf/gtfs-with-links.ttl` — sample output for the provided CSV
- `rdf/queries-with-links.sparql` — verification queries
