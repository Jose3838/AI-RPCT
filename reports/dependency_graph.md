# AI-RPCT Dependency Graph

Historical Source Registry
        |
        v
Historical Entity Registry
        |
        v
Provider Entity Registry
        |
        v
Provider Relationship Registry
        |
        +-------------------+
        |                   |
        v                   v
Unified Accelerator     Historical Capacity
        |                   |
        +---------+---------+
                  |
                  v
           Feature Store
                  |
                  v
         Forecast Dataset
                  |
                  v
      Forecast Engine v1
                  |
                  v
   Forecast Explanations
                  |
                  +------------------------+
                  |                        |
                  v                        v
      Data Quality Metrics      Pipeline Health
                  |                        |
                  +------------+-----------+
                               |
                               v
                     Pipeline Dashboard
