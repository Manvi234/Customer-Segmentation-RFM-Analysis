-- Orders joined with customers, aggregated payments, and review score.
-- Consumed by: mart_rfm_segments, mart_customer_lifecycle, mart_cohort_retention
SELECT
    o.order_id,
    o.customer_id,
    c.customer_unique_id,
    c.city,
    c.state,
    o.order_status,
    o.purchased_at,
    o.approved_at,
    o.shipped_at,
    o.delivered_at,
    o.estimated_delivery_at,
    DATE_DIFF(DATE(o.delivered_at), DATE(o.estimated_delivery_at), DAY) AS delivery_days_vs_estimate,
    p.total_payment_value,
    p.payment_type,
    r.review_score
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_customers') }} c
    ON o.customer_id = c.customer_id
LEFT JOIN (
    -- Collapse multiple payment rows (installments / mixed methods) to one per order
    SELECT
        order_id,
        SUM(payment_value) AS total_payment_value,
        MAX(payment_type)  AS payment_type
    FROM {{ ref('stg_order_payments') }}
    GROUP BY order_id
) p ON o.order_id = p.order_id
LEFT JOIN {{ ref('stg_order_reviews') }} r
    ON o.order_id = r.order_id
