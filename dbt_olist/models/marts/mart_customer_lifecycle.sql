-- One row per unique customer with acquisition, repeat, CLV, and churn metrics.
-- Covers notebook queries: new customers per month, repeat rate, purchase frequency, CLV, churn.
-- Partitioned by acquisition_month → filters by date skip entire partitions.
-- Clustered by state + is_churned → Tableau geo and churn filters hit less data.
{{
    config(
        materialized='table',
        partition_by={
            'field': 'acquisition_month',
            'data_type': 'date',
            'granularity': 'month'
        },
        cluster_by=['is_churned', 'is_repeat_customer']
    )
}}

WITH order_sequences AS (
    SELECT
        customer_unique_id,
        order_id,
        purchased_at,
        total_payment_value,
        ROW_NUMBER() OVER (
            PARTITION BY customer_unique_id ORDER BY purchased_at
        ) AS order_rank,
        LAG(purchased_at) OVER (
            PARTITION BY customer_unique_id ORDER BY purchased_at
        ) AS prev_purchased_at
    FROM {{ ref('int_orders_enriched') }}
),

customer_summary AS (
    SELECT
        customer_unique_id,
        MIN(purchased_at)                                                        AS first_purchase_at,
        MAX(purchased_at)                                                        AS last_purchase_at,
        COUNT(DISTINCT order_id)                                                 AS total_orders,
        SUM(total_payment_value)                                                 AS lifetime_value,
        AVG(DATE_DIFF(DATE(purchased_at), DATE(prev_purchased_at), DAY))         AS avg_days_between_orders
    FROM order_sequences
    GROUP BY customer_unique_id
),

dataset_max AS (
    SELECT DATE(MAX(purchased_at)) AS max_date FROM {{ ref('stg_orders') }}
)

SELECT
    cs.customer_unique_id,
    DATE_TRUNC(DATE(cs.first_purchase_at), MONTH)     AS acquisition_month,
    cs.first_purchase_at,
    cs.last_purchase_at,
    cs.total_orders,
    ROUND(cs.lifetime_value, 2)                        AS lifetime_value,
    ROUND(cs.lifetime_value / cs.total_orders, 2)      AS avg_order_value,
    ROUND(cs.avg_days_between_orders, 1)               AS avg_days_between_orders,
    cs.total_orders > 1                                AS is_repeat_customer,
    DATE_DIFF(DATE(cs.last_purchase_at), DATE(cs.first_purchase_at), DAY) AS customer_lifespan_days,
    -- Churned = no purchase in last 120 days (2x the ~60-day avg repeat gap)
    DATE_DIFF(dm.max_date, DATE(cs.last_purchase_at), DAY) > 120          AS is_churned
FROM customer_summary cs
CROSS JOIN dataset_max dm
