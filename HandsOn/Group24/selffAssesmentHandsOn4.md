# Self-Assessment Hands-On 4

## Work done
We defined RML mappings for our three selected datasets:
- Tree inventory of Madrid (2024)
- Environmental expenditure by industry (Spain)
- NO₂ annual averages (Spain)

We used RMLMapper 4.5.1 to generate RDF in Turtle syntax.

## Tools used
- OpenRefine (for cleaning CSV)
- RMLMapper (Java CLI)
- Visual Studio Code / GitHub Desktop

## Difficulties
- Handling column names with accents and spaces.
- Setting absolute URIs (the "#" prefix caused parsing errors initially).
- Matching CSV schema with ontology properties.

## Results
- Three `.ttl` RDF datasets successfully generated.
- Queries validated the presence of expected triples and structure.
- RML mappings tested locally with consistent outputs.

## Lessons learned
We learned how to define RML mappings, resolve URI issues, and connect CSV data with our ontology.
