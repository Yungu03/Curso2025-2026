# Hands-on assignment 3 – Self assessment

## Checklist

**Every resource described in the CSV file:**

- [x] Has a unique identifier in a column (not an auto-increased integer)
- [x] Is related to a class in the ontology

**Every class in the ontology:**

- [x] Is related to a resource described in the CSV file

**Every column in the CSV file:**

- [x] Is trimmed
- [x] Is properly encoded (e.g., dates, booleans)
- [x] Is related to a property in the ontology

**Every property in the ontology:**

- [x] Is related to a column in the CSV file

## Comments on the self-assessment
Data cleaning and ontology development are complete.

We found a misunderstanding in the traffic dataset: it included travel time metrics, not weather data.
Therefore, the requirement was adjusted to focus on traffic congestion status instead of meteorology.

The ontology was updated accordingly, adding properties like :hasCongestionFactor and :hasTrafficState to reflect the new information derived from OpenRefine.
