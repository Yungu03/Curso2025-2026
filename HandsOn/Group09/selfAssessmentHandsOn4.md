# Hands-on Assignment 4 – Self Assessment

## Checklist

**Data import and cleaning:**

- [x] Imported the selected dataset(s) into OpenRefine
- [x] Verified the format and encoding of CSV files
- [x] Ensured all columns were correctly recognized
- [x] Analysed the dataset for inconsistencies, missing values, and errors
- [x] Fixed errors and standardized values
- [x] Removed duplicates and irrelevant data
- [x] Applied transformations to facilitate RDF generation

**RML mappings:**

- [x] Created an RML mapping file (`mappings/*.rml`) defining subject maps and predicate-object maps for all relevant fields.
- [x] Used meaningful IRIs based on entity names rather than codes.
- [x] Defined mappings for all classes (e.g., Museum, Neighbourhood, District, Location, Province).
- [x] Ensured proper linking between entities through object properties (e.g., `ns:hasNeighbourhood`, `ns:hasDistrict`).
- [x] Validated the mapping file for syntax errors.

**RDF transformation:**

- [x] Executed the RML mappings using RMLMapper.
- [x] Generated an RDF file in Turtle syntax (`rdf/*.ttl`).
- [x] Verified that IRIs and properties are consistent with the ontology.
- [x] Checked that all expected triples were generated.

**Queries:**

- [x] Created a SPARQL file with validation queries (`rdf/queries.sparql`).
- [x] Tested queries to verify data correctness and relationships (e.g., list of museums by district, count of museums per neighbourhood).

**Deliverables:**

- [x] RML file: `mappings/*.rml`
- [ ] YAML file (optional): `mappings/*.yml`
- [x] RDF file in Turtle syntax: `rdf/*.ttl`
- [x] SPARQL queries file: `rdf/queries.sparql`
- [x] Markdown self-assessment: `selfAssessmentHandsOn4.md` in the group root directory
