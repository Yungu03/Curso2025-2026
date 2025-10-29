# Self-assessment for Hands-on 2

## What We Have Done

In this assignment, we have performed the foundational steps for generating Linked Data from the datasets selected in the previous assignment for the "Madrid Fluye" application.

The key tasks completed are:

1.  **Data and Schema Analysis:** We analyzed the three CSV files (`aparcamientos-publicos.csv`, `bikestationbicimad_csv.csv`, `I.M.D. LABORABLES 2024 -2025.csv`). We identified the key columns, data types, and the nature of each dataset (entity-based vs. aggregated measurements). A key finding was the need to transform the wide format of the traffic data.

2.  **Licensing Analysis:** We identified the data publishers (Ayuntamiento de Madrid, EMT) and their open licenses (CC0). We proposed using the **CC BY 4.0** license for our generated RDF dataset to ensure attribution while maintaining openness.

3.  **Resource Naming Strategy:** We designed a robust and clean URI strategy. This involved establishing a base domain, separating the ontology (`/ontology/`) from the data (`/csv/`), and defining clear, persistent patterns for identifying each resource (Parkings, Bike Stations, and Traffic Measurements).

4.  **Ontology Development:** We created a lightweight OWL ontology (`ontology.ttl`) using Turtle syntax. The ontology defines three main classes (`Parking`, `BikeStation`, `TrafficMeasurement`) and several datatype properties. Importantly, we prioritized reusing well-known external vocabularies like **Schema.org** and **W3C Basic Geo** to enhance interoperability.

5.  **Sample Instantiation:** We created an example RDF file (`ontology-example.ttl`) to demonstrate how real data from the CSVs would be represented using the ontology. This file includes one instance of each type, correctly linking data attributes to the defined properties.

## What We Have Learned

This assignment has been a practical introduction to the core principles of Linked Data generation.

-   **The Importance of URI Design:** We learned that designing a good URI strategy from the start is critical. It's not just about creating unique identifiers, but about creating ones that are logical, hierarchical, and persistent.
-   **The Power of Reusing Vocabularies:** Instead of inventing properties for everything, reusing terms from `schema.org` (like `name`, `address`, `geo`) and `geo` (like `lat`, `long`) makes the data instantly more understandable and linkable for other applications.
-   **Modeling Different Data Structures:** We faced the challenge of modeling two different types of data: lists of distinct entities (parkings, stations) and aggregated temporal data (traffic). This required creating different modeling patterns within the same ontology.
-   **Practical Turtle (TTL) Syntax:** We have solidified our understanding of writing both ontologies and instance data using the Turtle syntax, including defining classes, properties, domains, ranges, and individuals.

