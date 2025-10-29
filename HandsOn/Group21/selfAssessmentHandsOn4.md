# Hands-on assignment 4 – Self assessment

## Checklist

**Every RDF file:**

- [ ✔️] Uses the .nt extension
- [✔️ ] Is serialized in the NTriples format
- [ ✔️] Follows the resource naming strategy
- [✔️ ] Uses class and property URIs that are the same as those used in the ontology

**Every URI in the RDF files:**

- [ ✔️] Is "readable" and has some meaning (e.g., it is not an auto-increased integer) 
- [✔️ ] Is not encoded as a string
- [✔️ ] Does not contain a double slash (i.e., “//”)

**Every individual in the RDF files:**

- [✔️ ] Has a label with the name of the individual
- [✔️ ] Has a type

**Every value in the RDF files:**

- [ ✔️] Is trimmed
- [✔️ ] Is properly encoded (e.g., dates, booleans)
- [✔️ ] Includes its datatype
- [ ✔️] Uses the correct datatype (e.g., values of 0-1 may be booleans and not integers, not every string made of numbers is a number)

## Comments on the self-assessment
- The CSV-to-RDF transformation is defined with clear RML mappings aligned with the ontology and the provided templates; subject construction is stable and reproducible.
- The pipeline executes with RMLMapper and/or morph-kgc and generates a Turtle file that parses without errors while keeping prefix/URI consistency.
- SPARQL queries validate core aspects (entity counts, key relationships, datatype correctness) and their results are consistent with the transformed dataset.
- The repository structure matches the requirements (`mappings/*.rml`, optional `mappings/*.yml`, `rdf/*.ttl`, `rdf/queries.sparql`, and `selfAssessmentHandsOn4.md` at the root) with relative paths and concise run instructions.
- Literals are handled correctly (dates, booleans, and language tags when needed) and no unintended duplicate resources were found.
- As a minor improvement, consider adding one validating query per mapping rule and documenting URI patterns and any CSV preprocessing choices.
