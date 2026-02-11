# Animal-Cafe-BI-Solution
End-to-end BI solution: Python data generation, SSIS ETL pipeline (SCD Type 2), SQL Server Data Warehouse, and Power BI analytics for an Animal Cafe.

Ez a projekt egy fiktív állatos kávézó teljes üzleti intelligencia (BI) megoldását mutatja be. A folyamat az adatgenerálástól kezdve, egy háromrétegű adattárház (DWH) felépítésén és SSIS alapú ETL folyamatokon keresztül a Power BI vizualizációig tart.

## 🚀 Technológiai Stack
*   **Adatgenerálás:** Python (Faker könyvtár)
*   **Adatbázis:** Microsoft SQL Server
*   **ETL folyamatok:** Microsoft SSIS (SQL Server Integration Services)
*   **Adatmodellezés:** Csillagséma (Star Schema)
*   **Vizualizáció:** Power BI

---

## 📊 1. Adatforrás és Modellezés
A projekt alapját egy Python scripttel generált relációs adatbázis adja, amely egy kávézó mindennapi működését szimulálja (rendelések, foglalások, állatok egészségügyi adatai, vásárlók, előfizetések).

**Forrás adatbázis modell:**
![KÉP: Itt a PDF 2. oldalán lévő erd.dbdesigner-es modellt használd](docs/images/source_db_model.png)

---

## 🏗️ 2. Adattárház Architektúra (DWH)
A megoldás egy klasszikus háromrétegű architektúrára épül a maximális adatminőség és nyomonkövethetőség érdekében:

### A. STAGE Réteg
Az adatok egységesítése itt történik. Minden mező szöveges (`string`) típusú, nincsenek kényszerek (Constraints), így a betöltés gyors és hibatűrő.
*   **Cél:** A forrásrendszer tehermentesítése és az adatok gyors átemelése.

### B. HST (History) Réteg
Ebben a rétegben történik az adatok historizálása és az adattípusok véglegesítése.
*   **SCD Type 2:** Minden tábla tartalmaz `START_DATE` és `END_DATE` mezőket a változások követésére.
*   ![KÉP: PDF 5. oldali HST modell](docs/images/hst_model.png)

### C. DM (Data Mart) Réteg
A végfelhasználók számára előkészített, Csillagsémába rendezett adatok.
*   **Ténytábla:** `FactSales` (Értékesítések)
*   **Dimenziók:** `DimProduct`, `DimCustomer`, `DimDate`
*   ![KÉP: PDF 6. oldali Csillagséma kép](docs/images/star_schema.png)

---

## 🔄 3. ETL Folyamat (SSIS)
A teljes adatmozgatást **SQL Server Integration Services (SSIS)** csomagok végzik.

### Extract folyamat
Minden futás elején egy `Execute SQL Task` kiüríti a STAGE táblákat (`TRUNCATE`), majd feltölti azokat az aktuális adatokkal.
![KÉP: PDF 7. oldal, STAGE folyamat](docs/images/extract_process.png)

### Transform & Load
A historizálásért a **Slowly Changing Dimension (SCD)** komponens felel. A ténytábla feltöltésekor **Lookup** komponensek segítségével képezzük le az üzleti kulcsokat technikai kulcsokra (Surrogate Keys).
![KÉP: PDF 10. oldal, Tény tábla feltöltése](docs/images/load_fact.png)

---

## 📈 4. Power BI Analitika
A Power BI riport az alábbi üzleti kérdésekre ad választ:
*   Melyek a legnépszerűbb termékkategóriák?
*   Hogyan alakul a bevétel szezonalitása (negyedéves bontás)?
*   Kik a top vásárlók és mik a kedvenc termékeik?# Global Supply Chain & Sustainability BI Solution

**End-to-end Enterprise Data Warehouse (DWH) solution: Python data telemetry, SSIS ETL pipeline (SCD Type 2), SQL Server storage, and Power BI Analytics for Lifecycle Assessment (LCA).**

## 🚀 Project Overview
This project demonstrates a comprehensive Business Intelligence solution designed for a global manufacturing and supply chain network. It simulates real-time monitoring of factory emissions, material usage, and logistics efficiency.

The pipeline covers the entire data lifecycle:
1.  **Data Generation:** Synthetic telemetry simulating global factory nodes.
2.  **Data Warehousing:** A three-layer architecture (Stage, History, Data Mart).
3.  **ETL Orchestration:** Complex data transformation using SSIS.
4.  **Analytics:** Lifecycle Assessment (LCA) dashboarding.

---

## 🛠️ Technical Stack
*   **Data Generation:** Python (`Faker` library) - Simulating IoT sensor data & logistics logs.
*   **Database Engine:** Microsoft SQL Server (2019+).
*   **ETL Orchestration:** Microsoft SSIS (SQL Server Integration Services).
*   **Data Modeling:** Dimensional Modeling (Star Schema) & SCD Type 2.
*   **BI & Analytics:** Microsoft Power BI (DAX).

---

## 📊 1. Data Source & Modeling (Python)
The foundation is a Python-based telemetry engine that generates relational data simulating a global supply chain. Unlike static datasets, this script generates dynamic relationships between factories, materials, and energy consumption.

**Source Database Entities:**
*   **Factories:** Metadata about manufacturing locations.
*   **Materials:** Raw materials with specific carbon emission factors.
*   **Logistics:** Shipping routes and transport modes.
*   **Emission Logs:** Transactional data recording energy usage and CO2 output.

![Source DB Model](docs/images/source_db_model.png)

---

## 🏗️ 2. Data Warehouse Architecture
The solution follows a classic **Three-Tier Architecture** to ensure high data quality, historical tracking, and query performance:

### A. STAGE Layer (Landing Zone)
*   **Purpose:** Raw data ingestion.
*   **Design:** All fields are handled as `strings` (varchar) with no constraints.
*   **Logic:** `TRUNCATE` + `INSERT` strategy for high-speed batch loading.

### B. HST (History) Layer - Core DWH
*   **Purpose:** Data type enforcement and historical tracking.
*   **Design:** Implements **Slowly Changing Dimensions (SCD Type 2)**.
*   **Logic:** Every dimension table tracks changes (e.g., if a factory changes its energy source) using `START_DATE`, `END_DATE`, and `IS_CURRENT` flags. This ensures a perfect audit trail for LCA reporting.

![HST Model](docs/images/hst_model.png)

### C. DM (Data Mart) Layer - Analytics
*   **Purpose:** Optimized for BI reporting.
*   **Design:** **Star Schema**.
*   **Fact Table:** `FactEmissions` (Contains measures: Energy usage, CO2 output).
*   **Dimensions:** `DimMaterial`, `DimFactory`, `DimLogistics`, `DimDate`.

![Star Schema](docs/images/star_schema.png)

---

## 🔄 3. ETL Pipeline (SSIS Orchestration)
The integration logic is managed by **SQL Server Integration Services (SSIS)** packages.

### Extract & Load Phase
*   **Control Flow:** An `Execute SQL Task` performs a `TRUNCATE` on STAGE tables before each run.
*   **Data Flow:** Extracts fresh telemetry from the Python-generated source and loads it into the Staging area.

![Extract Process](docs/images/extract_process.png)

### Transformation Phase (SCD Logic)
*   **Historization:** Managed via **SCD Wizard** or custom Merge logic to handle historical updates.
*   **Surrogate Keys:** Uses **Lookup Transformations** to map business keys to technical Surrogate Keys, isolating the DWH from source system changes.

![Load Fact](docs/images/load_fact.png)

---

## 📈 4. Power BI Sustainability Analytics
The final dashboard provides critical insights for **LCA (Lifecycle Assessment)** practitioners:

*   **Carbon Footprint Trends:** Quarterly analysis of CO2 emissions across different manufacturing regions.
*   **Material Efficiency:** Identifying high-impact materials and suggesting sustainable alternatives based on historical data.
*   **Operational KPIs:**
    *   **Total Carbon Footprint (kg CO2e)**
    *   **Energy Intensity (kWh/Unit)**
    *   **Material Circularity Score**

![Power BI Dashboard](docs/images/powerbi_dashboard.png)

---

## ⚙️ Setup & Execution

1.  **Database Initialization:**
    *   Run scripts in `/sql/01_create_source.sql` to setup the operational DB.
    *   Run `/sql/02_create_dwh.sql` to setup Stage, History, and Data Mart schemas.
2.  **Data Generation:**
    *   Execute `python scripts/data_generator.py` to populate the source system.
3.  **ETL Execution:**
    *   Open the SSIS project in Visual Studio.
    *   Configure `Connection Managers` for your local SQL Server instance.
    *   Execute the `Master_Package.dtsx` to trigger the full ETL cycle.
4.  **Analysis:**
    *   Open `reports/Sustainability_Dashboard.pbix` to explore the data.

**Főbb üzleti mutatók (KPI-ok):**
*   Összes bevétel (Total Revenue)
*   Tranzakciószám (Transaction Count)
*   Átlagos kosárérték (Avg Ticket Size)

![KÉP: PDF 12. vagy 15. oldal, a Dashboard-odról egy látványos kép](docs/images/powerbi_dashboard.png)

---

## 🛠️ Telepítés és Használat
1.  Futtasd le a `/sql` mappában található táblalétrehozó scripteket.
2.  Nyisd meg az SSIS projektet Visual Studio-ban.
3.  Állítsd be a `Connection Manager`-ben a saját SQL Server példányodat.
4.  Futtasd le a csomagokat az adatok betöltéséhez.
5.  Nyisd meg a Power BI fájlt az adatok elemzéséhez.
