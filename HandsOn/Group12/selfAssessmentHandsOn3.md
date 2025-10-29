# Hands-on 3 – Self-assessment

## Dataset used
**Zonas Verdes 2024 – Ayuntamiento de Madrid**  
Source: Internal municipal inventory of urban green areas (parks and gardens) from public urban registry data.

---

## ✅ Data cleaning and transformation summary

The dataset was imported into **OpenRefine** and the following operations were applied:

- Trimmed whitespaces in all columns.  
- Normalized capitalization and diacritics (e.g., *Bailén* instead of *BAILEN*).  
- Removed duplicate or blank rows.  
- Renamed columns for RDF compatibility:
  - `Número de archivo` → `FileNumber`
  - `Naturaleza del inmueble` → `PropertyNature`
  - `Situación Destino` → `SituationTarget`
  - `Destino` → `Destination`
  - `Solar` → `Plot`
- Added a new column `ZoneURI` generating a unique URI for each row:  
  `http://linkeddata.greenzonesmadrid.org/resource/zone/{row_index}`

---

## 🔗 Alignment with ontology

Each cleaned column maps directly to a property in the ontology defined in the previous Hands-on:

| CSV Column        | Ontology Property (gz:) | RDF Range  |
|--------------------|-------------------------|-------------|
| ZoneURI            | (used as subject URI)   | URI         |
| Distrito           | gz:district             | xsd:string  |
| Subepigrafe        | gz:subepigrafe          | xsd:string  |
| Apartado           | gz:apartado             | xsd:string  |
| FileNumber         | gz:fileNumber           | xsd:string  |
| PropertyNature     | gz:propertyNature       | xsd:string  |
| SituationTarget    | gz:situationTarget      | xsd:string  |
| Destination        | gz:destination          | xsd:string  |
| Plot               | gz:plot                 | xsd:string  |

---

## 🧩 Validation checks

✅ Each resource (row) has a **unique URI**  
✅ All properties correspond to ontology definitions  
✅ Text encoding verified (UTF-8)  
✅ No null or inconsistent values in required fields  
✅ Dataset ready for RDF transformation via RDFRefine or Python (rdflib)

---

## 💬 Comments

The data cleaning process successfully produced a normalized, error-free version of the original municipal dataset.  
This ensures semantic interoperability and easy mapping to the ontology `gz:` for future RDF publication.