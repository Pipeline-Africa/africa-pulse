\# Open-Meteo Test Fixtures



This directory contains captured Open-Meteo API responses for use in connector tests.



The fixtures provide reproducible examples of successful responses, historical data, multi-location data, API errors, and edge-case inputs.



\## Fixtures



\### `forecast\_lagos\_hourly.json`



Normal hourly forecast response for Lagos, Nigeria.



Request:



`https://api.open-meteo.com/v1/forecast?latitude=6.5244\&longitude=3.3792\&hourly=temperature\_2m,relative\_humidity\_2m,precipitation\&forecast\_days=2`



Captured: 2026-10-04



\### `historical\_lagos\_hourly.json`



Historical hourly weather response for Lagos, Nigeria, covering 1–2 September 2026.



Request:



`https://archive-api.open-meteo.com/v1/archive?latitude=6.5244\&longitude=3.3792\&start\_date=2026-09-01\&end\_date=2026-09-02\&hourly=temperature\_2m,relative\_humidity\_2m,precipitation`



Captured: 2026-10-04



\### `forecast\_multi\_location.json`



Forecast response containing multiple locations (Lagos and Abuja) to test handling of multi-location API responses.



Request:



`https://api.open-meteo.com/v1/forecast?latitude=6.5244,9.0765\&longitude=3.3792,7.3986\&hourly=temperature\_2m\&forecast\_days=1`



Captured: 2026-10-04



\### `error\_invalid\_latitude.json`



Error response produced by supplying an invalid latitude (`999`). This fixture can be used to test API error handling.



Request:



`https://api.open-meteo.com/v1/forecast?latitude=999\&longitude=3.3792\&hourly=temperature\_2m`



Captured: 2026-10-04



\### `edge\_zero\_coordinates.json`



Successful response for latitude `0` and longitude `0`. This fixture tests handling of zero-valued coordinates, which should not be interpreted as missing values.



Request:



`https://api.open-meteo.com/v1/forecast?latitude=0\&longitude=0\&hourly=temperature\_2m\&forecast\_days=1`



Captured: 2026-10-04



\## Attribution



Weather data provided by Open-Meteo.



These fixtures are captured API responses intended for testing and development purposes.

