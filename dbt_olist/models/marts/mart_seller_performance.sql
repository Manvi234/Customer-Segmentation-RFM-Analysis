-- Seller leaderboard: units sold, revenue, unique customers, 5-star reviews, fulfillment speed.
-- Covers notebook Query 6 and Query 12.
-- Clustered by total_revenue → leaderboard queries (ORDER BY revenue DESC) hit less data.
-- Note: COUNTIF is BigQuery-specific; on Snowflake use COUNT(CASE WHEN review_score = 5 THEN 1 END).
{{
    config(
        materialized='table',
        cluster_by=['seller_id', 'total_items_sold']
    )
}}

SELECT
    oi.seller_id,
    COUNT(oi.order_id)                                                          AS total_items_sold,
    ROUND(SUM(oi.price), 2)                                                     AS total_revenue,
    COUNT(DISTINCT o.customer_id)                                               AS unique_customers,
    COUNTIF(r.review_score = 5)                                                 AS five_star_reviews,
    ROUND(
        SAFE_DIVIDE(COUNTIF(r.review_score = 5), COUNT(oi.order_id)) * 100, 1
    )                                                                           AS five_star_rate_pct,
    ROUND(
        AVG(DATE_DIFF(DATE(oi.shipping_limit_at), DATE(o.approved_at), DAY)), 2
    )                                                                           AS avg_fulfillment_days
FROM {{ ref('int_order_items_enriched') }} oi
JOIN {{ ref('stg_orders') }} o
    ON oi.order_id = o.order_id
LEFT JOIN {{ ref('stg_order_reviews') }} r
    ON o.order_id = r.order_id
GROUP BY oi.seller_id
