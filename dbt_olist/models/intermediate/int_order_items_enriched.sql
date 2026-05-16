-- Order items joined with product details and English category names.
-- Consumed by: mart_seller_performance, mart_category_performance
SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.shipping_limit_at,
    oi.price,
    oi.freight_value,
    p.category_name_pt,
    COALESCE(ct.category_name_en, p.category_name_pt) AS category_name_en,
    p.weight_g,
    p.length_cm,
    p.height_cm,
    p.width_cm
FROM {{ ref('stg_order_items') }} oi
LEFT JOIN {{ ref('stg_products') }} p
    ON oi.product_id = p.product_id
LEFT JOIN {{ ref('stg_category_translation') }} ct
    ON p.category_name_pt = ct.category_name_pt
