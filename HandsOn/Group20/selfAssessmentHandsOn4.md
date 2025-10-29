# Checklist
## Assignment 4
### 📁 `mappings` directory

#### 📄 `mappings.rml`
- [x] Includes the mappings
> [Open mappings.rml](./mappings/mappings.rml)

#### 📄 `mapping-rules.yml`
- [x] Includes the mapping rules
> [Open mapping-rules.yml](./mappings/mapping-rules.yml)
---

### 📁 `rdf` directory

#### 📄 `parkings.ttl`
- [x] Includes the data transformed into RDF
- [x] Uses the  `.ttl`  extension and is serialized in the Turtle format
- [x] Follows the resource naming strategy
- [x] Uses class and property URIs that are the same as those used in the ontology
- [x] Has every URI readable, meaningful, not encoded as a string and not containing double slashes
- [x] Has every individual labeled with its name and having a type
- [x] Has every value trimmed, properly encoded, including its datatype and using the correct datatype
> [Open parkings.ttl](./rdf/parkings.ttl)

#### 📄 `queries.sparql`
- [x] Includes queries to verify the data
> [Open queries.sparql](./rdf/queries.sparql)
