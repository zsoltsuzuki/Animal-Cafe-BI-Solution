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
*   Kik a top vásárlók és mik a kedvenc termékeik?

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
