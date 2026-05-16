SELECT
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_date AS shipping_limit_at,
    price,
    freight_value
FROM {{ source('olist', 'order_items') }}
