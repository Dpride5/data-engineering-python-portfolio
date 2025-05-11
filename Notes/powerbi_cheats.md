|---------------------------------------------------------------------------------------------------------------------------------- |
| Running total | `Running Total = CALCULATE([Total Hours], FILTER(ALLSELECTED(employee_hours), employee_hours[Date] <= MAX(employee_hours[Date])))` |
| YoY Growth    | `YoY Hours = [Total Hours] - CALCULATE([Total Hours], SAMEPERIODLASTYEAR(employee_hours[Date]))`                                   |
| Pct of total  | `Pct of Total = DIVIDE([Total Hours], CALCULATE([Total Hours], ALL(employee_hours)))`                                              |
