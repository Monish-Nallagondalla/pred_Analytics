---

# **Project Plan: Smart Manufacturing Analytics Prototype**

## **1. Project Objective**

The goal of this project is to **simulate a manufacturing unit** and build a **state-of-the-art predictive maintenance and analytics dashboard** using generated realistic data. This prototype will be used to demonstrate to clients:

1. Machine performance monitoring (realistic sensor data).
2. Predictive maintenance (RUL, fault detection, anomaly detection).
3. Material flow tracking across the manufacturing line.
4. Andon-style alerts for machine faults and process issues.
5. Real-time KPIs and visualizations for technical and non-technical users.
6. Process-level insights for operations optimization.

> **Key Constraints:**

* No real data available → generate **one-time realistic synthetic data**.
* Models trained and saved once (`.pkl`) → dashboard uses precomputed results.
* Modular, maintainable code for future expansion.

---

## **2. Manufacturing Scenario**

We will model a **sheet metal + injection molding manufacturing unit**, with the following processes:

### **Sheet Metal Line:**

1. Material application → requisition tracking.
2. Blanking → CNC shears, laser cutting.
3. Punching/Cutting → CNC punching, die-cut.
4. Bending → Press brakes.
5. Fitter → Riveting, mechanical processing.
6. Welding → ARC, MIG/TIG, spot welding.
7. Polishing → Surface finishing.
8. Surface treatment → Painting, oxidation.
9. Semi-finished inspection → Dimension & appearance check.
10. Silk printing → Logo/text etching.
11. Final assembly → Screws, rivets, pins.
12. Quality inspection → Final QC.
13. Warehousing/packaging.
14. Ready for shipment.

### **Injection Molding Line:**

1. Moulding/die preparation.
2. Machine selection.
3. Material selection → plastic granules.
4. Preheating.
5. Injection.
6. Cooling/curing.
7. Component ejection.
8. Degating.
9. Surface treatment (primer/painting).
10. QC & packing.

> **Material Flow:** The system must show **step-by-step movement of each batch/order through all machines**, including status, time spent, and defects.

---

## **3. Machines and Sensors**

Here are **realistic machine types with example specifications** to generate data:

| Process            | Machine Type               | Key Sensors/Specs                                                  | Notes                                  |
| ------------------ | -------------------------- | ------------------------------------------------------------------ | -------------------------------------- |
| Blanking           | Trumpf TruPunch 1000       | Axis position, spindle load, vibration, motor current, temperature | Sheet thickness, plate size, punch die |
| CNC Punching       | Amada EM2510NT             | Motor torque, feed rate, cutting force, axis positions             | Power, precision logs                  |
| Laser Cutting      | Bystronic ByStar Fiber     | Laser power, focus position, gas flow, temperature                 | Material type & thickness              |
| Press Brake        | LVD PPEB 220               | Ram position, hydraulic pressure, bending angle, tool temp         | Sequence, interference logging         |
| Welding            | Lincoln Electric Power MIG | Welding current, voltage, wire feed rate, gas flow                 | Weld time, temperature                 |
| Polishing          | Rösler Vibrofinisher       | RPM, vibration, load, coolant flow                                 | Polishing time, tool wear              |
| Surface Treatment  | Nordson Spray Booth        | Coating thickness, nozzle pressure, oven temp                      | Spray duration, curing time            |
| Assembly           | Manual/Robot Arm           | Torque sensors, joint positions                                    | Time per assembly                      |
| Injection Molding  | Engel e-mac                | Barrel temp, injection pressure, cooling time, screw speed         | Mold temp, cycle time                  |
| Quality Inspection | CMM Machine                | Dimension deviations, surface roughness                            | Sampling rate                          |

> Each machine will generate **time-series data**, batch status, and occasional **faults/anomalies** based on real failure probabilities.

---

## **4. Modular Project Structure**

```
smart_mfg_project/
│
├── config/                 # Machine, sensor, thresholds, and process config files
│   ├── machines.yaml
│   ├── sensors.yaml
│   ├── thresholds.yaml
│   └── dashboard.yaml
│
├── artifacts/              # Precomputed data & model files
│   ├── data.pkl            # Generated machine telemetry, order flows
│   ├── models/             
│       ├── anomaly_detector.pkl
│       ├── rul_predictor.pkl
│       └── fault_classifier.pkl
│   └── reports/            # CSV/Excel exports of KPIs
│
├── src/                    # Core Python modules
│   ├── data_generation.py  # Synthetic data generator
│   ├── ml_models.py        # Model training, prediction
│   ├── flow_simulator.py   # Material and batch flow
│   ├── andon_system.py     # Alert generation based on thresholds
│   ├── dashboard.py        # Streamlit app
│   ├── kpi_calculator.py   # Compute KPIs from generated data
│   └── utils.py            # Common functions
│
├── notebooks/              # Jupyter notebooks for prototyping & analysis
├── tests/                  # Unit tests for modules
└── main.py                 # App entry point for Streamlit
```

> **Important:** Only generate data once → save in `artifacts/data.pkl`.
> Train models once → save in `artifacts/models/*.pkl`.

---

## **5. Data Generation Plan**

1. **Order-level Data:**

   * Order ID, product type, batch size, material type.
   * Planned production time per machine.
   * Assigned operator/engineer.

2. **Machine-level Telemetry:**

   * Sensors: vibration, temperature, motor current, axis positions, speed, hydraulic pressure.
   * Batch ID, timestamps.
   * Simulate anomalies/faults randomly (with probabilities).

3. **Process Flow Data:**

   * Timestamped **material movement between machines**.
   * Record delays, bottlenecks, maintenance actions.
   * Include **quality checks & defects** per batch.

4. **Maintenance Data:**

   * Historical failures (simulated).
   * RUL values for predictive modeling.
   * Maintenance actions & downtime.

5. **KPIs Calculation:**

   * MTBF, MTTR, OEE.
   * Scrap rate, rework rate, process yield.
   * Cycle time per machine/process.

6. **Data Storage:**

   * Save in `.pkl` (Python pickle) → fast load in dashboard.
   * Optional: export CSV for reports.

---

## **6. Machine Learning Models**

**All models will be trained once on synthetic data and saved for inference:**

| Task                 | Algorithm                               | Input                         | Output                     |
| -------------------- | --------------------------------------- | ----------------------------- | -------------------------- |
| Anomaly Detection    | Isolation Forest (unsupervised)         | Sensor telemetry              | Binary anomaly flag        |
| RUL Prediction       | Multi-Layer Perceptron (MLP Regression) | Sliding window of sensor data | Predicted hours to failure |
| Fault Classification | Random Forest                           | Sensor + categorical features | Fault type probabilities   |

**Notes:**

* Preprocess features (standardization, sliding windows).
* Validate model using synthetic historical data.
* Save models in `.pkl` → dashboard only runs inference.

---

## **7. Streamlit Dashboard Design**

### **A. Layout**

* **Sidebar:**

  * Machine selection filter
  * Process stage filter
  * Batch/order selection
  * Time range filter
  * Export reports (CSV/Excel)
* **Main Page:**

  * **Overview Tab**

    * Company logo, production line image.
    * Summary KPIs: OEE, MTBF, MTTR, Scrap %, Production count.
    * Overall material flow diagram (Sankey or network graph).
  * **Machine Telemetry Tab**

    * Interactive line charts for sensors (temp, vibration, torque, pressure).
    * Fault/anomaly overlay.
    * Zoom/filter by batch or machine.
  * **Predictive Maintenance Tab**

    * RUL prediction dashboard (bar chart of machines ordered by urgency).
    * Anomaly and fault probability heatmap.
    * Historical maintenance events timeline.
  * **Production Flow Tab**

    * Batch/order movement through all machines.
    * Highlight bottlenecks & delays.
    * Gantt chart for order timelines.
  * **Quality & Inspection Tab**

    * Defect rates per process.
    * Sample QC images placeholder (optional for demo).
    * Inspection pass/fail trends.
  * **Andon Alert Tab**

    * Live-like alert table (from generated anomalies).
    * Severity color coding (Green, Yellow, Red, Critical).
    * Alert timestamps, affected machine, batch info.
  * **Reports Tab**

    * Download KPI reports, machine stats, flow stats as CSV/Excel.
    * Summary PDF generation placeholder (optional).

### **B. Visualization Recommendations**

* **Sensor Trends:** Line charts with thresholds.
* **Material Flow:** Sankey diagram or network graph.
* **RUL & Faults:** Heatmaps or color-coded bars.
* **Bottleneck Detection:** Highlight with red/amber.
* **Alerts:** Dynamic table with severity icons.
* **KPIs:** Cards with numeric summary and sparkline trends.

---

## **8. Technology Stack Recommendation**

* **Python 3.8+**
* **Data Science:** pandas, numpy, scikit-learn, matplotlib, seaborn
* **Dashboard:** Streamlit, Plotly for interactive charts, NetworkX for flow
* **Storage:** pickle (`.pkl`) for datasets & models
* **Others:** pydantic/yaml for configuration, fpdf or similar for report export

> Rationale: Lightweight, fast development, reproducible, modular.

---

## **9. Project Timeline (Prototype)**

| Phase | Tasks                                    | Duration |
| ----- | ---------------------------------------- | -------- |
| 1     | Requirements analysis, process mapping   | 2 days   |
| 2     | Define machine list, sensors, thresholds | 1 day    |
| 3     | Data generation module                   | 3 days   |
| 4     | ML model training and saving             | 2 days   |
| 5     | KPI computation & flow simulation        | 2 days   |
| 6     | Streamlit dashboard design & integration | 3 days   |
| 7     | Testing, validation, and demo prep       | 2 days   |
| 8     | Documentation and client-ready prototype | 1 day    |

---

## **10. Deliverables**

1. **Generated dataset (`data.pkl`)** → all machines, batches, sensors, QC, flow.
2. **Trained ML models (`.pkl`)** → anomaly detector, RUL predictor, fault classifier.
3. **Streamlit dashboard** → full visualization of processes, KPIs, machine telemetry, material flow, predictive maintenance.
4. **Reports** → exportable CSV/Excel for KPIs, maintenance logs, flow stats.
5. **Project documentation** → instructions for future devs to extend system.

---

## **11. Key Notes for Prototype Development**

1. Generate **realistic sensor patterns** including degradation, batch anomalies, and random failures.
2. Only **one-time data generation** and **model training** → dashboard purely visualizes precomputed results.
3. Keep **modular code** → config files for machines, sensors, thresholds; artifacts for saved data/models; src for logic.
4. Include **technical and non-technical KPIs**: MTBF, MTTR, OEE, scrap %, production throughput, defect counts.
5. Material flow visualization should cover **all 15 sheet metal + injection molding steps**.
6. All graphs and dashboards should **reflect what a real manufacturing unit expects**, making it demo-ready for clients.





make sure the Dashboard , the models made and the data generated all match the plan in  @project_plan.md 



---

# **Streamlit Dashboard Plan – Smart Manufacturing Prototype**

## **1. Overall Design Principles**

* **User-Centric**: Designed for non-technical users – visual, simple, color-coded.
* **Interactive but Simple**: Dropdowns, filters, and tabs to explore data without overwhelming.
* **Story-Driven**: Material flows, machine status, maintenance alerts, production progress.
* **Realistic Visuals**: Sankey diagrams for flows, heatmaps for machine health, gauges for KPIs.
* **All-in-One**: No switching apps – everything visible in the same dashboard.
* **Data & Models Precomputed**: Dashboard only loads data and predictions (from `.pkl`).

---

## **2. App Structure & Navigation**

### **Sidebar Controls**

* **Filter by Production Line**: Sheet Metal / Injection Molding.
* **Filter by Machine**: Dropdown to select one or multiple machines.
* **Filter by Batch / Order**: Track specific customer orders.
* **Date/Time Range**: Select period of interest.
* **Export Options**: Download KPI reports, flow reports, maintenance logs.
* **Alert Settings**: Optional toggle to show only active critical alerts.

### **Main Page Tabs**

| Tab                                  | Purpose                              | Key Components                                                                                                                                                                                                                                                      |
| ------------------------------------ | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Overview / Dashboard Home**     | High-level production snapshot       | - KPI cards: OEE, MTBF, MTTR, Scrap Rate, Production Count<br>- Gauge charts for machine utilization<br>- Material flow Sankey diagram (from raw material to finished goods)<br>- Pie chart: % of orders on-time vs delayed                                         |
| **2. Machine Health & Telemetry**    | Track individual machine performance | - Interactive line charts: Temperature, Vibration, Current, Pressure, RPM<br>- Color-coded thresholds (green/yellow/red) overlay<br>- Anomaly markers on charts<br>- Historical maintenance log table<br>- RUL bar chart: Machines ordered by remaining useful life |
| **3. Production Flow & Bottlenecks** | Visualize batch movement             | - Gantt chart: Order progress across machines<br>- Flow diagram / Sankey chart: Material moving between machines<br>- Bottleneck highlight: red or amber colored nodes<br>- Average cycle time per machine/process                                                  |
| **4. Predictive Maintenance**        | Maintenance insights                 | - Heatmap of fault probabilities per machine<br>- Top 5 most at-risk machines for the week<br>- Maintenance history timeline<br>- Predictive RUL chart (with threshold alerts)<br>- Option to download suggested maintenance schedule                               |
| **5. Quality & Inspection**          | Process QA visualization             | - Defects per machine/process bar chart<br>- QC pass/fail pie chart<br>- Trend chart of scrap/rework rate<br>- Sample inspection table (fake images or placeholders)<br>- Alerts for abnormal defect rate                                                           |
| **6. Andon Alerts**                  | Real-time alerts & escalation        | - Dynamic table of active alerts with severity color code<br>- Machine, batch, timestamp, description<br>- Filter by severity (Critical, High, Medium, Low)<br>- Historical alert trend chart                                                                       |
| **7. Reports & Downloads**           | Stakeholder-ready export             | - Download KPIs (CSV/Excel)<br>- Download machine performance logs<br>- Download material flow / bottleneck reports<br>- Optional PDF summary report (company-ready)                                                                                                |

---

## **3. Key Visualizations & Widgets**

| Metric / Concept            | Visualization Type                | Notes / UX Tips                                     |
| --------------------------- | --------------------------------- | --------------------------------------------------- |
| Machine Utilization         | Gauge / Circular Progress         | Show % of scheduled time machine was active         |
| Machine Health              | Line Chart + Threshold bands      | Green/yellow/red zones for easy interpretation      |
| RUL (Remaining Useful Life) | Horizontal Bar                    | Machines sorted by urgency, red = low RUL           |
| Fault Probability           | Heatmap                           | Rows = machines, Columns = fault types              |
| Material Flow               | Sankey / NetworkX graph           | Color-coded by process stage or bottleneck severity |
| Production Cycle Time       | Bar Chart / Box Plot              | Average, min/max, per machine                       |
| QC Defects                  | Bar chart, Pie chart              | By process or batch                                 |
| Active Alerts               | Table with colored severity icons | Clickable rows to view details                      |
| Historical Alerts           | Line chart / stacked area         | Show alert trends over time                         |

> Use **hover tooltips** to explain technical terms for non-IT users (e.g., “MTTR = Mean Time to Repair”).

---

## **4. KPI Summary Cards (Home Tab)**

1. **OEE (Overall Equipment Effectiveness)** – % of planned production actually achieved.
2. **MTBF (Mean Time Between Failures)** – average hours between breakdowns.
3. **MTTR (Mean Time to Repair)** – average downtime per failure.
4. **Scrap / Rework Rate** – % of products needing correction.
5. **Production Count** – number of units completed in period.
6. **Active Machines** – # of machines currently running.
7. **Critical Alerts** – # of ongoing severe issues.

> Each card shows **current value + small trend sparkline**.

---

## **5. Material Flow & Bottlenecks Visualization**

* **Sankey Diagram**: Each node = machine/process, width = number of items.
* **Bottleneck Highlighting**: Nodes in red/amber where average cycle time is > threshold.
* **Batch Tracking**: Hover shows Batch ID, planned vs actual processing time.
* **Optional animation**: Material moving through stages over time (for demo effect).

---

## **6. Predictive Maintenance Insights**

* **RUL Visualization**: Horizontal bar chart for all machines → red = urgent maintenance.
* **Fault Probability Heatmap**: Machines x fault types → probability from 0–100%.
* **Maintenance Schedule Suggestion Table**: Machine, predicted failure, recommended action.
* **Anomaly Highlighting**: Timeline of unusual readings per machine.

---

## **7. Quality & Inspection Tab**

* **Defect per Process Bar Chart**: Identify weak points.
* **QC Pass/Fail Pie Chart**: Easy visual ratio.
* **Trend Over Time**: Scrap rate per week/day.
* **Sample Inspection Table**: Include notes like “Surface scratches” or “Bending deviation”.
* **Alerts for abnormal defect rate**: Flag for management attention.

---

## **8. Andon Alerts Tab**

* **Dynamic Table**: Columns: Timestamp, Machine, Batch, Severity, Description.
* **Severity Coloring**: Green/Yellow/Red/Critical.
* **Filter Options**: Machine, severity, time range.
* **Historical Trends**: Line chart of alerts over last N days.

> Goal: Stakeholders immediately know what needs attention without technical jargon.

---

## **9. Reports & Downloads Tab**

* **Export Options**: CSV/Excel/PDF.
* **Content**:

  * Machine telemetry summary
  * KPI snapshots
  * Production flow / bottleneck summary
  * Maintenance log & predictions
  * Quality inspection summary

> PDF reports can have **visual summaries + KPI cards** for board-level presentations.

---

## **10. UX / Design Notes for Non-Technical Users**

1. **Color Coding:** Always use intuitive colors (Red = critical, Green = normal).
2. **Tooltips & Info Buttons:** Explain terms like MTBF, RUL, OEE.
3. **Hover-over details:** Minimal tables by default; details appear on hover.
4. **Dashboard Story:** Start with Overview → Machine Health → Flow → Maintenance → Quality → Alerts → Reports.
5. **Minimal Text:** Use visuals and icons rather than tables and numbers where possible.
6. **Responsive & Interactive:** Dropdown filters and clickable charts to explore data by machine, batch, or time period.
7. **Placeholder Images:** For QC or assembly processes, use simple icons or images to enhance visualization.

---

## **11. Data & Model Flow in Dashboard**

1. **Load Data Once**: `data.pkl` → includes telemetry, batch flow, QC, maintenance logs.
2. **Load ML Models Once**: `.pkl` files → RUL, anomalies, fault classification.
3. **Compute KPIs**: Once on data load → cache results to improve responsiveness.
4. **Render Visuals**: Interactive charts, Sankey diagrams, dashboards.
5. **Alerts / Andon System**: Rule-based triggers applied on loaded telemetry.
6. **Downloads**: Export precomputed data or summarized KPIs.

---

## ✅ **Summary of Tab Flow**

1. **Overview / Dashboard Home** → High-level KPIs + material flow.
2. **Machine Health & Telemetry** → Sensor trends, anomalies, RUL.
3. **Production Flow & Bottlenecks** → Batch movement, delays, cycle times.
4. **Predictive Maintenance** → Heatmaps, RUL, maintenance schedules.
5. **Quality & Inspection** → Scrap/rework, QC pass/fail, defect trends.
6. **Andon Alerts** → Active and historical alerts, severity-coded.
7. **Reports & Downloads** → Stakeholder-ready exportable reports.

> This dashboard ensures **all technical and non-technical stakeholders** can monitor, interpret, and act on manufacturing insights in one place.

---











---

# **Smart Manufacturing Dummy Data Schema**

## **1. Orders / Batch Table**

Tracks all customer orders and batch-level info.

| Column             | Type     | Description              | Example / Range                    |
| ------------------ | -------- | ------------------------ | ---------------------------------- |
| order_id           | string   | Unique order identifier  | ORD_1001                           |
| product_type       | string   | Product model/type       | SheetMetalBox_A                    |
| batch_id           | string   | Batch identifier         | BATCH_001                          |
| batch_size         | int      | Number of parts          | 50–500                             |
| material_type      | string   | Raw material type        | Stainless Steel 304, Aluminum 6061 |
| material_thickness | float    | Thickness in mm          | 1–5                                |
| order_date         | datetime | Order placement date     | 2025-10-08 08:00                   |
| planned_start      | datetime | Planned production start | 2025-10-08 09:00                   |
| planned_end        | datetime | Planned production end   | 2025-10-08 17:00                   |
| assigned_engineer  | string   | Responsible engineer     | John Doe                           |
| status             | string   | Order status             | planned / in-progress / completed  |

---

## **2. Machine Inventory Table**

Defines each machine, type, and specifications.

| Column            | Type     | Description                | Example / Range                                                       |
| ----------------- | -------- | -------------------------- | --------------------------------------------------------------------- |
| machine_id        | string   | Unique machine ID          | CNC_PUNCH_01                                                          |
| machine_type      | string   | Category                   | CNC Punch, Laser Cutter, Bender, Welder, Polisher, Injection Moulding |
| manufacturer      | string   | Vendor                     | Trumpf, Amada, Mazak, Bosch                                           |
| model             | string   | Model                      | TruPunch 1000, LC-3015                                                |
| max_capacity      | float    | Max throughput per hour    | 50–200 units                                                          |
| power_rating      | float    | kW                         | 5–50                                                                  |
| location          | string   | Factory location / cell    | Cell A1                                                               |
| installation_date | datetime | Installed date             | 2022-01-15                                                            |
| last_service_date | datetime | Last maintenance           | 2025-09-15                                                            |
| sensor_list       | JSON     | List of sensors on machine | ["temp", "vibration_x", "motor_current"]                              |

---

## **3. Machine Telemetry Table**

Time-series sensor data for each machine. **Each machine type has specific sensors.**

| Column             | Type     | Description               | Example / Range     |
| ------------------ | -------- | ------------------------- | ------------------- |
| timestamp          | datetime | Sensor reading time       | 2025-10-08 09:05:00 |
| machine_id         | string   | Machine ID                | CNC_PUNCH_01        |
| batch_id           | string   | Batch processed           | BATCH_001           |
| spindle_rpm        | float    | Spindle speed (CNC/Drill) | 500–3000            |
| feed_rate          | float    | Feed mm/min               | 50–500              |
| cutting_force      | float    | N                         | 200–2000            |
| vibration_x/y/z    | float    | mm/s                      | 0–5                 |
| motor_current      | float    | A                         | 5–25                |
| motor_voltage      | float    | V                         | 380–480             |
| temperature        | float    | °C                        | 30–90               |
| hydraulic_pressure | float    | bar                       | 50–250              |
| coolant_flow       | float    | L/min                     | 0–20                |
| tool_wear          | float    | % wear                    | 0–100               |
| cycle_time         | float    | sec                       | 10–300              |
| status_flag        | string   | Normal / Anomaly / Fault  | Normal              |

> **Machine-specific sensors:**

* **CNC Punch:** spindle_rpm, feed_rate, cutting_force, motor_current, vibration, temperature
* **Laser Cutter:** laser_power, cutting_speed, head_temp, lens_status
* **Bender / Press Brake:** hydraulic_pressure, angle, bend_force, tool_wear
* **Welder:** current, voltage, arc_length, cooling_flow
* **Polisher:** spindle_rpm, vibration, temperature
* **Injection Moulding:** barrel_temp, screw_rpm, injection_pressure, mold_temp

---

## **4. Process Flow / Material Tracking Table**

Tracks **batch movement** and timing across machines.

| Column         | Type     | Description                   | Example / Range              |
| -------------- | -------- | ----------------------------- | ---------------------------- |
| batch_id       | string   | Batch ID                      | BATCH_001                    |
| process_step   | string   | Process name                  | Punching / Bending / Welding |
| machine_id     | string   | Machine executing step        | CNC_PUNCH_01                 |
| start_time     | datetime | Step start                    | 2025-10-08 09:05             |
| end_time       | datetime | Step end                      | 2025-10-08 09:15             |
| duration       | float    | minutes                       | 5–60                         |
| operator       | string   | Operator name                 | Alice                        |
| quality_flag   | string   | Pass / Fail / Scrap           | Pass                         |
| defect_type    | string   | If defect occurs              | Burr / Crack / Misalignment  |
| remarks        | string   | Notes / delays                | Tool change / Power surge    |
| material_moved | bool     | True if moved to next process | True                         |

---

## **5. Maintenance Table**

Track machine failures, RUL, and corrective/preventive maintenance.

| Column           | Type     | Description                     | Example / Range            |
| ---------------- | -------- | ------------------------------- | -------------------------- |
| machine_id       | string   | Machine under maintenance       | CNC_PUNCH_01               |
| failure_id       | string   | Unique failure ID               | F_001                      |
| failure_type     | string   | Wear / Breakdown / Sensor Fault | Wear                       |
| start_time       | datetime | Failure occurrence              | 2025-10-08 12:30           |
| end_time         | datetime | Maintenance completed           | 2025-10-08 13:15           |
| downtime         | float    | minutes                         | 5–120                      |
| maintenance_type | string   | Corrective / Preventive         | Corrective                 |
| parts_replaced   | string   | Parts replaced                  | Tool Bit, Hydraulic Hose   |
| notes            | string   | Any extra info                  | Minor spindle misalignment |

---

## **6. Quality Inspection Table**

Track quality at intermediate steps and final inspection.

| Column          | Type     | Description              | Example / Range                     |
| --------------- | -------- | ------------------------ | ----------------------------------- |
| batch_id        | string   | Batch ID                 | BATCH_001                           |
| inspection_step | string   | Step where inspected     | Punching / Welding / Final Assembly |
| inspector       | string   | Inspector name           | Bob                                 |
| dimension_ok    | bool     | True if dimension OK     | True                                |
| surface_ok      | bool     | True if surface OK       | True                                |
| assembly_ok     | bool     | True if assembly correct | True                                |
| defects_found   | string   | List of defects          | Burr, Scratch                       |
| rework_required | bool     | True if rework needed    | False                               |
| inspection_time | datetime | Inspection timestamp     | 2025-10-08 13:20                    |

---

## **7. KPIs / Performance Metrics Table**

Derived metrics for dashboard visualization:

| Column            | Type   | Description                       | Example / Range |
| ----------------- | ------ | --------------------------------- | --------------- |
| machine_id        | string | Machine ID                        | CNC_PUNCH_01    |
| batch_id          | string | Batch processed                   | BATCH_001       |
| utilization       | float  | % machine utilization             | 70–100          |
| availability      | float  | % uptime                          | 85–100          |
| OEE               | float  | Overall Equipment Effectiveness % | 65–95           |
| avg_cycle_time    | float  | Average cycle time                | 10–300 sec      |
| defect_rate       | float  | Defects / total units %           | 0–5             |
| maintenance_count | int    | Maintenance events per period     | 0–5             |
| downtime          | float  | Minutes of downtime               | 0–120           |

---

## **8. Derived Analytics / ML Features**

For predictive models (RUL, anomaly, optimization):

| Column               | Type   | Description                          | Example / Range                     |
| -------------------- | ------ | ------------------------------------ | ----------------------------------- |
| machine_id           | string | Machine ID                           | CNC_PUNCH_01                        |
| sensor_features      | JSON   | Aggregated sensor readings per batch | {"temp_avg":75,"vibration_max":3.2} |
| rolling_mean         | float  | Rolling mean over last N readings    | 0–100                               |
| rolling_std          | float  | Rolling std deviation                | 0–5                                 |
| anomaly_flag         | bool   | True if anomaly detected             | False                               |
| RUL_pred             | float  | Remaining useful life in hours       | 10–200                              |
| maintenance_required | bool   | True if preventive maintenance due   | False                               |

---

## **9. Material & Inventory Tracking Table**

Track raw material consumption and inventory status.

| Column           | Type   | Description                | Example / Range |
| ---------------- | ------ | -------------------------- | --------------- |
| material_id      | string | Material ID                | MAT_001         |
| material_type    | string | Stainless Steel / Aluminum | Stainless Steel |
| thickness        | float  | mm                         | 1–5             |
| batch_id         | string | Batch using this material  | BATCH_001       |
| quantity_used    | float  | kg / m²                    | 10–500          |
| inventory_before | float  | kg / m²                    | 1000            |
| inventory_after  | float  | kg / m²                    | 990             |

---

## **10. Packaging & Shipment Table**

Track finished products, packaging, and shipping info.

| Column          | Type     | Description            | Example / Range  |
| --------------- | -------- | ---------------------- | ---------------- |
| batch_id        | string   | Batch ID               | BATCH_001        |
| packed_units    | int      | Units packed           | 50               |
| packaging_type  | string   | Box / Foam / Tray      | Box + Foam       |
| shipper         | string   | Name                   | FedEx / DHL      |
| shipping_date   | datetime | Date shipped           | 2025-10-08 16:00 |
| logistics_no    | string   | Tracking number        | TRK_1001         |
| shipment_status | string   | In-transit / Delivered | In-transit       |

---

## **Key Notes**

1. **All tables are linked via `machine_id` and `batch_id`** to allow end-to-end tracking.
2. **Sensor data generation** should simulate realistic noise, trends, and degradation over time.
3. **Batch flow table** allows visualization of **material movement** across all processes.
4. **Maintenance and KPIs** feed predictive ML models (RUL, anomaly detection, flow optimization).
5. **Single data generation**: generate all above tables once, save in `.pkl` or database, then run ML and dashboards on same data.

---

✅ **Next Steps:**

* Decide **machines to simulate** (CNC Punch, Laser Cutter, Bender, Welder, Polisher, Injection Moulding).
* Define **sensor list and ranges per machine**.
* Generate **batch orders** and assign them to machines.
* Simulate **time-series sensor readings** with realistic process durations, downtime, defects, and maintenance.
* Save **all tables once** for dashboard & ML modeling.

---




---

# **Flow Diagram Plan for Streamlit Dashboard**

## 🎯 **Goal**

To visualize the **path of materials, parts, and batches** as they move from one machine/process to another (e.g., *Blanking → Punching → Bending → Welding → Polishing → Surface Treatment → Assembly → QA → Packaging*).

This visualization helps:

* Non-technical users understand **production flow** at a glance
* Engineers identify **bottlenecks** or delays
* Managers monitor **real-time status** of machines and batches

---

## 🧩 **Approach Overview**

We’ll build a **dynamic, interactive process flow diagram** using **Streamlit** and **graph visualization libraries** like **Plotly**, **NetworkX**, or **Graphviz (via pygraphviz or pydot)**.

---

## 🏗️ **Architecture Plan**

### **1. Data Source**

Use the **Process Flow / Material Tracking Table** from your data schema:

* `batch_id`, `process_step`, `machine_id`, `start_time`, `end_time`, `quality_flag`, etc.

From this, construct edges:

```
(Blanking → Punching → Bending → Welding → Assembly → QA → Packaging)
```

Each edge represents a **flow step**; each node represents a **machine/process**.

---

### **2. Preprocessing Layer (Backend Logic)**

* Create a **graph structure** from process flow data (directed graph `G`).

* Compute metrics for each node (machine):

  * Current status (Running / Idle / Fault)
  * Throughput / Efficiency
  * Average cycle time
  * Defect rate

* Color-code machines based on status.

  * 🟢 Normal
  * 🟡 Warning
  * 🔴 Fault

* Edge thickness or color intensity can represent **material volume** or **flow delay**.

---

### **3. Visualization Layer (Streamlit Frontend)**

#### **Option A – Plotly Sankey Diagram**

* Best for showing **quantitative material flow** between processes.
* Each node = process step
* Each link = number of parts/material moving
* Link thickness = quantity of items
* Ideal for showing *“where most material/time goes”*

#### **Option B – Network Graph (NetworkX + Plotly)**

* Best for **process relationships and machine states**.
* You can:

  * Display machine nodes as circles with color-coded health.
  * Use arrows to indicate flow direction.
  * Hover tooltips to show live machine metrics (OEE, temperature, RUL, etc.).
  * Update graph periodically if you simulate real-time behavior.

#### **Option C – Graphviz (Process Flow Diagram)**

* Clean, flowchart-style visualization.
* Machines connected top-down or left-right by arrows.
* Use custom icons or labels (e.g., machine name, current status).

---

### **4. Dashboard Integration**

Add a **“Material Flow” page** to your Streamlit sidebar navigation:

#### **Page Layout**

**Title:** “Factory Flow & Process Visualization”

**Sections:**

1. **Live Production Map**

   * Interactive process flow (Plotly Sankey or NetworkX)
   * Dropdown to select `batch_id` or `date`
2. **Machine Status Summary**

   * KPI boxes below diagram (e.g., active machines, avg. downtime, OEE)
3. **Flow Efficiency Metrics**

   * Graph of *cycle time vs. process step*
   * *Material yield* (input vs. output ratio per process)
4. **Bottleneck Detection**

   * Highlight process with longest avg. duration
   * Tooltip or color flag on that node

---

### **5. User Interactions**

* **Filter by Batch / Order / Shift**
  → Show only relevant flow
* **Click on Machine Node**
  → Expand details: sensor graphs, downtime history, maintenance logs
* **Hover Over Link**
  → Show material quantity, delay time, and scrap count between processes
* **Export Button**
  → Download current flow report as PDF or Excel

---

### **6. Tech Stack Recommendation**

| Layer         | Tool                                 | Purpose                     |
| ------------- | ------------------------------------ | --------------------------- |
| Visualization | Plotly / Graphviz / NetworkX         | Interactive flow diagrams   |
| Dashboard     | Streamlit                            | UI + control panels         |
| Data Storage  | Pandas DataFrames / SQLite / Parquet | Load pre-generated data     |
| Styling       | CSS via Streamlit Theme Config       | Corporate branding look     |
| Caching       | `st.cache_data`                      | To load generated data once |

---

### **7. Extension Ideas**

* **Add real-time simulation mode** → Animate flow as if material moves every few seconds.
* **Integrate machine health** → Overlay sensor anomaly color on machine nodes.
* **Add maintenance alerts** → Flashing node border when downtime event occurs.
* **Flow bottleneck prediction** → ML model predicts which node will delay next batch.

---

### **8. Deliverable in Project Plan**

In your project plan document, you can add this section as:

> **Component: Process Flow Visualization (Streamlit Dashboard)**
>
> * Purpose: To visualize material movement and machine interaction in production.
> * Input: Process Flow Table (machine_id, process_step, start_time, end_time, etc.)
> * Output: Interactive flow diagram showing machine states, material quantities, and delays.
> * Visualization Type: Plotly Sankey + NetworkX Hybrid
> * Status Indicators: Color-coded machine nodes (green/yellow/red)
> * Interactions: Batch filter, machine drill-down, data export.
> * Update Frequency: Static (prototype mode, loaded once from pre-generated data).


