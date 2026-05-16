-- Month-over-month cohort retention.
-- Incremental: on each run only re-processes the last two cohort months,
-- then merges into the table so historical rows are not re-scanned.
-- Partitioned by cohort_month → each cohort month is its own partition.
-- Clustered by month_index → retention queries always filter on month_index.
{{
    config(
        materialized='incremental',
        unique_key=['cohort_month', 'month_index'],
        incremental_strategy='merge',
        partition_by={
            'field': 'cohort_month',
            'data_type': 'date',
            'granularity': 'month'
        },
        cluster_by=['month_index']
    )
}}

WITH customer_first_purchase AS (
    SELECT
        customer_unique_id,
        DATE_TRUNC(DATE(MIN(purchased_at)), MONTH) AS cohort_month
    FROM {{ ref('int_orders_enriched') }}
    GROUP BY customer_unique_id
),

customer_purchases AS (
    SELECT DISTINCT
        customer_unique_id,
        DATE_TRUNC(DATE(purchased_at), MONTH) AS purchase_month
    FROM {{ ref('int_orders_enriched') }}

    {% if is_incremental() %}
    -- Only pull purchases from the last two months to catch late-arriving data
    WHERE DATE(purchased_at) >= (
        SELECT DATE_SUB(MAX(cohort_month), INTERVAL 2 MONTH)
        FROM {{ this }}
    )
    {% endif %}
),

cohort_analysis AS (
    SELECT
        cfp.customer_unique_id,
        cfp.cohort_month,
        cp.purchase_month,
        DATE_DIFF(cp.purchase_month, cfp.cohort_month, MONTH) AS month_index
    FROM customer_first_purchase cfp
    JOIN customer_purchases cp
        ON cfp.customer_unique_id = cp.customer_unique_id
)

SELECT
    cohort_month,
    month_index,
    COUNT(DISTINCT customer_unique_id) AS total_users
FROM cohort_analysis
GROUP BY cohort_month, month_index
