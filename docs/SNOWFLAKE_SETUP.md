# Snowflake setup

DuckDB is the dev target; Snowflake is a **second dbt target on the same models**
— no rewrite. Develop fast locally, then build to Snowflake for the cloud story.

## 1. Bootstrap the account (once)

Run [`warehouse/snowflake_setup.sql`](../warehouse/snowflake_setup.sql) as a role
that can create databases/warehouses. It creates the `ENERGY_FLEXIBILITY_OS`
database, the schemas (`RAW`, `STAGING`, `MARTS`, `OPTIMISATION`, `MONITORING`,
`APP`, `REPORTING`), an XSMALL auto-suspending warehouse, and the `MONITORING.*`
tables that mirror the local CSV monitoring records.

## 2. Set credentials

```bash
export SNOWFLAKE_ACCOUNT=xy12345.eu-west-1
export SNOWFLAKE_USER=...
export SNOWFLAKE_PASSWORD=...
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH        # optional (has a default)
export SNOWFLAKE_ROLE=TRANSFORMER            # optional
```

## 3. Build

```bash
pip install -e ".[snowflake]"
cd dbt_energy
dbt build --target snowflake                 # vs. the default duckdb 'dev'
dbt source freshness --target snowflake       # warn >6h / error >12h on carbon RAW
```

Source freshness is configured on `raw.seed_carbon_intensity` via its
`data_fetched_at` load stamp (warn after 6h, error after 12h). It is meaningful
against the Snowflake RAW table that Dagster stamps on each load; against the
static dev seed it ages as expected. `dbt build` is unaffected — freshness only
runs on the explicit `dbt source freshness` command.

## Cost note

Data volume is tiny (~670 rows/day for GB regional half-hourly). The XSMALL
warehouse with `AUTO_SUSPEND = 60` keeps spend near zero — this is deliberately
not a big-data workload; Snowflake is here for the warehouse/governance story,
not because the data needs it.
