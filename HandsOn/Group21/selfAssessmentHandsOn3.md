# Hands-on assignment 3 – Self assessment

## Checklist

**Every resource described in the CSV file:**

- [✔️] Has a unique identifier in a column (not an auto-increased integer)
- [✔️] Is related to a class in the ontology

**Every class in the ontology:**

- [✔️] Is related to a resource described in the CSV file

**Every column in the CSV file:**

- [✔️] Is trimmed
- [✔️] Is properly encoded (e.g., dates, booleans)
- [✔️] Is related to a property in the ontology

**Every property in the ontology:**

- [✔️] Is related to a column in the CSV file

## Comments on the self-assessment
We worked with three open datasets from the Madrid City Council portal:  
- Traffic accidents (2025)  
- Fixed speed cameras (Radares fijos DGT)  
- Population by district (1 January)  

All datasets were cleaned and standardized using OpenRefine.  
Operations included removing duplicates, fixing text inconsistencies, normalizing names, converting data types, and ensuring coherence among datasets for future RDF linkage.
