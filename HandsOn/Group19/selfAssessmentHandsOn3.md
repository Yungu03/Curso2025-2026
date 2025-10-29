# Hands-on 3: OpenRefine Data Cleaning – Self-Assessment

_Date: 2025-10-09_

## 1. Objective
The goal of this hands-on was to get familiar with **data cleaning and preparation using OpenRefine**.  
We worked with three different CSV datasets related to public information in Madrid and prepared them for further **RDF conversion**.  

Each dataset was imported into OpenRefine, analyzed, cleaned, and exported again after applying a sequence of transformations.  
The corresponding OpenRefine operation histories (`.json` files) reproduce exactly the same steps that were applied manually.

---

## 2. Datasets Processed

### 2.1 Aparcamientos Públicos
- **Raw file:** `202625-0-aparcamientos-publicos.csv`  
- **Cleaned file:** `202625-0-aparcamientos-publicos-updated.csv`  
- **OpenRefine operations:** `openrefine/history-202625-0-aparcamientos-publicos.json`
- **Encoding:** Latin-1  
- **Separator:** `;`
- **Columns (raw → final):**  
  `PK, NOMBRE, DESCRIPCION-ENTIDAD, ... , LONGITUD` → `id, name, openingHours, latitud, longitude`
- **Cleaning summary:**
  - Normalized headers to English, lowercase, and meaningful field names.  
  - Trimmed whitespace in all textual fields.  
  - Standardized null-like values (e.g. `-`, `N/A`, `NULL`).  
  - Selected and reordered only essential columns for RDF export.  
  - Converted latitude and longitude fields to numeric.

---

### 2.2 I.M.D. Laborables 2024–2025
- **Raw file:** `I.M.D. LABORABLES 2024 -2025.csv`  
- **Cleaned file:** `I-M-D-LABORABLES-2024-2025-updated.csv`  
- **OpenRefine operations:** `openrefine/history-I-M-D-LABORABLES-2024-2025-updated.json`
- **Encoding:** UTF-8  
- **Separator:** `;`
- **Columns (raw → final):**  
  `Año, Mes, Interior 1er cinturón, ..., Exterior a M-40` → `year, month, zone, intensity`
- **Cleaning summary:**
  - Unified column naming to English and normalized case/accents.  
  - Removed all intermediate “zone” columns to create a normalized representation of one “zone–intensity” pair per row.  
  - Trimmed whitespace and standardized missing values.  
  - Ensured numeric columns (`year`, `intensity`) are typed as numbers and dates are parsed correctly.

---

### 2.3 BiciMAD Stations
- **Raw file:** `bikestationbicimad_csv.csv`  
- **Cleaned file:** `bikestationbicimad_csv-updated.csv`  
- **OpenRefine operations:** `history-bikestationbicimad_csv-updated.json`
- **Encoding:** UTF-8  
- **Separator:** `;`
- **Columns (raw → final):**  
  `FID, Shape, IdStation, Address, DockBikes, ... , POINT_Y` →  
  `id, name, address, totalDocks, availableDocks, latitude, longitude`
- **Cleaning summary:**
  - Renamed columns to clear identifiers suitable for RDF properties.  
  - Removed irrelevant operational fields (`Shape`, `NoAvailabl`, `Ligth`, etc.).  
  - Converted coordinate columns (`POINT_X`, `POINT_Y`) into numeric `latitude` and `longitude`.  
  - Ensured all numeric values (dock counts) are stored as numbers.

---

## 3. Cleaning and Transformation Strategy

1. **Column normalization:**  
   - Converted all headers to lowercase, ASCII, and snake_case for RDF predicate compatibility.  
   - Translated names into English when relevant.

2. **Whitespace and null handling:**  
   - Applied `value.trim()` to all columns.  
   - Replaced placeholders like `-`, `N/A`, or `NULL` with blank cells.

3. **Coordinate normalization:**  
   - Split coordinate fields when needed (`lat`, `lon`) and ensured correct numeric ranges.

4. **Duplicate removal (manual verification):**  
   - Checked for duplicate IDs; removed redundant rows and columns.

5. **Export consistency:**  
   - Ensured UTF-8 CSV export.  
   - Verified that exported CSVs match OpenRefine’s output using the provided `.json` operation files.

---

## 4. Relation to RDF Conversion

The cleaned CSVs are now **RDF-ready**, because:
- Column names can map directly to ontology predicates.  
- Numeric and date columns are properly typed (`xsd:decimal`, `xsd:date`).  
- Missing data is represented as absence of triples rather than placeholder strings.  
- Latitude/longitude fields enable linkage to WGS84 vocabularies (`wgs84_pos:lat`, `wgs84_pos:long`).

---

## 5. Reflections and Limitations

- Some manual semantic decisions (e.g., column selection and naming) cannot be inferred automatically.  
- IMD dataset simplification to “zone–intensity” pairs required conceptual normalization, not just cleaning.  
- For RDF export, a future step should define **prefixes and URI patterns** (e.g., base URI, subject template).

---


### Conclusion
This exercise demonstrated how to perform **systematic data cleaning** with OpenRefine, ensuring reproducibility, traceability, and semantic readiness for RDF generation.  
By exporting both the cleaned data and the operation histories, the process is transparent and easily repeatable by anyone in the group.

