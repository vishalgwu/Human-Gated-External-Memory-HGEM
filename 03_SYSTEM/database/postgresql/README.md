# PostgreSQL Setup

PostgreSQL stores T1 immutable constants, experiment events, and conflict logs.

Expected database:

```powershell
createdb hgem_research
psql -d hgem_research -f 03_SYSTEM/database/postgresql/schema.sql
```

The application role should have insert/select permissions for experiment logs. T1 constants should be treated as append-only after session setup.

