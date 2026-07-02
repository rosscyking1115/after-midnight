-- Date dimension for the Power BI star. Integer surrogate key (yyyymmdd).
--
-- Built from a contiguous full-year date spine (seed_dates), NOT from the dates
-- that happen to appear in the fact: DAX time intelligence (DATEADD, month-over-
-- month, etc.) silently misbehaves on a date table with gaps or partial years.
-- day_of_week (1 = Monday) exists as the sort-by column for day_name.
with dates as (
    select cast(full_date as date) as full_date from {{ ref('seed_dates') }}
)
select
    extract(year from full_date) * 10000
        + extract(month from full_date) * 100
        + extract(day from full_date)        as date_key,
    full_date,
    extract(year from full_date)             as year,
    extract(month from full_date)            as month,
    date_trunc('month', full_date)           as month_start,
    dayname(full_date)                       as day_name,
    extract(isodow from full_date)           as day_of_week,
    case when extract(isodow from full_date) in (6, 7) then true else false end
        as is_weekend
from dates
