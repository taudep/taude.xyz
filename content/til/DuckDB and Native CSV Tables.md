---
title: DuckDB and Native CSV Tables
date: 2025-01-01
draft: false
tags:
  - duckdb
  - til
original_date: 2025-01-01
slug: "duckdb-and-native-csv-tables"
---
Not new, but I'm light on content. I told my team about this trick the other day, and it's one of my favorites: using duckdb to ingest various CSV exports from various sources and then using SQL to poke at that data.

Details from the docs over at: [DuckDB CSV Import](https://duckdb.org/docs/current/guides/file_formats/csv_import)

But in short, I export various datasets from Snowflake pretty regularly, from different databases and datasets that aren't naturally joined; I download various JSON reports from APIs and convert the Results to CSV.  Then I bring them both into duckdb:
```sql
CREATE TABLE tenantInformation 
   AS SELECT * FROM read_csv('global_tenan_list.csv');
   
CREAT TABLE regionalErrors 
   AS SELECT * from read_csv('regionMapping.csv');
   

Select * from ...
```

Well, you can take it from here.