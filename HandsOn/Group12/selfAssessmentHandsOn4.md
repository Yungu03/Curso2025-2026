# Self-assessment HO4 — RDF Generation (RML/YARRRML)

**Grupo:** Group12  
**Miembro:** Fernando Delgado Merino (@fernan9976)  
**Dataset:** Inventario de zonas verdes del Ayuntamiento de Madrid (2024)  
**Fecha:** 10/10/2025  
**Profesor:** Daniel Garijo

---

## 1. Pre-requisitos

- ✅ Se han leído las especificaciones de **RML** y **YARRRML** para comprender la transformación de datos semi-estructurados a RDF.  
- ✅ Se ha instalado **Python** y se ha descargado la herramienta **Morph-KGC**.  
- ✅ Se han revisado los materiales adicionales proporcionados: diapositivas completas de transformación de datos, cheatsheet y guías de datos.gob.

---

## 2. Dataset y limpieza de datos

El dataset seleccionado es el **Inventario de zonas verdes del Ayuntamiento de Madrid (2024)**. Este contiene información sobre parques, jardines y otros espacios verdes públicos clasificados por distrito.

- Columnas originales del CSV:
  - `Distrito`
  - `Subepígrafe`
  - `Apartado`
  - `Número de archivo`
  - `Naturaleza del inmueble`
  - `Situación Destino`
  - `Destino`
  - `Solar`

🔧 **Limpieza y transformación:**  
Se ha utilizado **OpenRefine** para realizar las siguientes operaciones (ver `operations.json`):

1. Eliminación de espacios en blanco al inicio y final de las celdas.  
2. Normalización de valores (ej.: “centro” → “CENTRO”).  
3. Renombrado de columnas para facilitar el mapeo RDF:
   - `Número de archivo` → `FileNumber`  
   - `Naturaleza del inmueble` → `PropertyNature`  
   - `Situación Destino` → `SituationTarget`  
   - `Destino` → `Destination`  
   - `Solar` → `Plot`  
4. Creación de una columna adicional `ZoneURI` con URIs únicas para cada zona:  
   `http://linkeddata.greenzonesmadrid.org/resource/zone/{row_index}`

---

## 3. Ontología

Se ha diseñado una ontología ligera (`gz-ontology.ttl`) que define la clase principal:

- `gz:GreenZone` — Representa una zona verde del inventario.

Y las propiedades de datos asociadas:

- `gz:district`
- `gz:subepigrafe`
- `gz:apartado`
- `gz:fileNumber`
- `gz:propertyNature`
- `gz:situationTarget`
- `gz:destination`
- `gz:plot`

Esta ontología permite representar cada fila del CSV como un recurso RDF con sus propiedades correspondientes.

---

## 4. Mapeo y generación RDF

Se han creado los mapeos necesarios para la transformación de los datos CSV en RDF utilizando RML:

- 📄 `mappings/greenzones.rml`: archivo con las reglas de mapeo RML.  
- 📄 `mappings/greenzones.yml`: versión equivalente en YARRRML (opcional).

El proceso de transformación se ha llevado a cabo con **RMLMapper** y **Morph-KGC**, generando un archivo RDF en formato Turtle:

- 📄 `rdf/greenzones.ttl`: contiene las instancias RDF de todas las zonas verdes.

Cada fila del CSV se convierte en una instancia de `gz:GreenZone`, con propiedades correspondientes a las columnas.

---

## 5. Consultas SPARQL de verificación

Se han definido consultas SPARQL para comprobar que los datos se han transformado correctamente (`rdf/queries.sparql`):

1. Número total de zonas transformadas.
2. Selección de cinco zonas con sus propiedades principales.
3. Filtrado por distrito (`CENTRO`).
4. Búsqueda de zonas cuyo destino contenga la palabra “BÁSICO”.
5. Visualización de las superficies de las zonas (`plot`).

Estas consultas permiten verificar la integridad y consistencia del RDF generado.

---

## 6. Reproducibilidad y estructura del proyecto

La estructura final del repositorio sigue la siguiente organización:

HandsOn/
└── Group12/
├── mappings/
│ ├── greenzones.rml
│ └── greenzones.yml
├── rdf/
│ ├── greenzones.ttl
│ └── queries.sparql
├── ontology/
│ └── gz-ontology.ttl
├── data/
│ └── zonas-verdes-updated.csv
├── operations.json
└── selfAssessmentHandsOn4.md


Este esquema facilita la ejecución reproducible del proceso completo: limpieza, mapeo, transformación y verificación.

---

## 7. Observaciones y mejoras futuras

- La propiedad `gz:plot` se mantiene como cadena de texto con sufijo “m2”. En una versión futura se puede extraer el valor numérico y tiparlo como `xsd:decimal`.
- Podrían enlazarse los distritos (`gz:district`) a vocabularios externos como **GeoNames** o a ontologías oficiales del Ayuntamiento de Madrid para mejorar la interoperabilidad.
- Se recomienda automatizar el pipeline de transformación con un script o `Makefile`.

---

## 8. Checklist de entrega

✅ `mappings/greenzones.rml`  
✅ `mappings/greenzones.yml` (opcional)  
✅ `rdf/greenzones.ttl`  
✅ `rdf/queries.sparql`  
✅ `selfAssessmentHandsOn4.md`

---

## 9. Conclusión

Este trabajo ha permitido comprender de forma práctica cómo transformar datos semi-estructurados (CSV) en RDF utilizando **RML** y **YARRRML**, cómo diseñar una ontología ligera y cómo validar los datos transformados mediante consultas SPARQL. Además, se ha conseguido un dataset enlazable y reutilizable en el contexto de la Web Semántica.
