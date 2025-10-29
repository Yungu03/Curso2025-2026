# Hands-on 4 — Group19 — RML → RDF

## Datasets
- Public car parks in Madrid (`202625-0-aparcamientos-publicos-updated.csv`)
- BiciMAD bike stations (`bikestationbicimad_csv-updated.csv`)
- Monthly mobility intensity by ring/zone (`I-M-D-LABORABLES-2024-2025-updated.csv`)

## Namespaces
- Base: `http://group19.linkeddata.es/`
- Resources: `http://group19.linkeddata.es/resource/`
- Ontology: `http://group19.linkeddata.es/def/transport#`
- External: `schema.org`, `wgs84_pos`, `xsd`

## Mapping decisions
- **Parkings → `ont:ParkingFacility`**  
  Each record in the parking CSV is mapped as an individual parking facility, with the following properties:
  - `schema:name` for the name of the parking.
  - `schema:openingHours` for its opening schedule.
  - Coordinates with `wgs:lat` and `wgs:long`.

- **BiciMAD stations → `ont:BikeStation`**  
  Each record in the bike station CSV is represented as a bike station resource, with:
  - `schema:name` and `schema:address` for descriptive data.
  - `schema:capacity` corresponding to `totalDocks`.
  - `ont:availableDocks` for currently available docks.
  - Coordinates via `wgs:lat` and `wgs:long`.

- **Mobility intensity → `ont:MobilityIntensity`**  
  The dataset of monthly intensities by ring/zone represents traffic mobility:
  - `ont:year` — year of the data point.
  - `ont:month` — month name (e.g., “Enero”).
  - `ont:zone` — the spatial area.
  - `ont:intensity` — numeric traffic intensity.

- **URIs and templates**  
  Each dataset defines unique subjects:
  - `http://group19.linkeddata.es/resource/parking/{id}`
  - `http://group19.linkeddata.es/resource/bikestation/{id}`
  - `http://group19.linkeddata.es/resource/mobility/{year}/{month}/{zone}`

## Linking
To demonstrate dataset integration, proximity links were computed between datasets:
- Added `ont:nearbyParking` from each BiciMAD station to its **closest parking facility** within **300 meters** (precomputed in `rdf/data.ttl`).
- These links are not produced directly by the RML file but are included in the final RDF dataset.

## How to generate RDF
- **Option 1 — RMLMapper (Java):**
  ```bash
  java -jar rmlmapper.jar -m mappings/mapping.rml -o rdf/data.ttl
  ```
- **Option 2 — morph-kgc (Python):**
  ```bash
  morph-kgc -m mappings/mapping.yml -o rdf/data.ttl
  ```

> The provided `rdf/data.ttl` in this submission was generated following the same logic and includes the additional proximity links.

## Validation SPARQL
The file `rdf/queries.sparql` contains queries to check that the transformation was correct:
1. Count of total triples.
2. Number of BiciMAD stations and parking facilities.
3. List of stations with available docks.
4. Stations and their nearby parking (if linked).
5. Mobility intensity for January 2024 (inner rings).
6. Stations located near a parking facility (based on the computed link).

## Files
```
HandsOn/Group19/
├── mappings/
│   ├── mapping.rml         # RML (Turtle) mappings
│   └── mapping.yml         # YARRRML (optional)
├── rdf/
│   ├── data.ttl            # Generated RDF (Turtle)
│   └── queries.sparql      # Verification queries
└── selfAssessmentHandsOn4.md
```

## Notes / Limitations
- In the RML template for `mobility`, the `{zone}` variable may include spaces; most engines handle this automatically by URL-encoding it.  
  In the provided RDF file (`data.ttl`), the URIs were slugified for consistency.
- The `ont:` vocabulary is minimal and defined specifically for this assignment, complementing `schema.org` and `wgs84_pos`.
- The RDF file also includes precomputed links between BiciMAD stations and nearby parking spots to demonstrate cross-dataset relationships.

## Authors
- **Group 19**
