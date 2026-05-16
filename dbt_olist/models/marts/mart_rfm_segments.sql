-- RFM segmentation across all ~96k customers.
-- Replaces the copy-pasted 20-line CTE that appeared twice in notebook cells 69 and 80.
-- Clustered by customer_segment + r_score → Tableau segment filters read far less data.
{{
    config(
        materialized='table',
        cluster_by=['customer_segment', 'r_score']
    )
}}

WITH customer_metrics AS (
    SELECT
        customer_unique_id,
        DATE_DIFF(
            (SELECT DATE(MAX(purchased_at)) FROM {{ ref('stg_orders') }}),
            DATE(MAX(purchased_at)),
            DAY
        )                          AS recency_days,
        COUNT(DISTINCT order_id)   AS frequency,
        SUM(total_payment_value)   AS monetary
    FROM {{ ref('int_orders_enriched') }}
    GROUP BY customer_unique_id
),

rfm_scores AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(5) OVER (ORDER BY frequency ASC)     AS f_score,
        NTILE(5) OVER (ORDER BY monetary ASC)      AS m_score
    FROM customer_metrics
)

SELECT
    customer_unique_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    CONCAT(CAST(r_score AS STRING), CAST(f_score AS STRING), CAST(m_score AS STRING)) AS rfm_combined_score,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Hibernating'
        ELSE 'Others'
    END AS customer_segment
FROM rfm_scores
