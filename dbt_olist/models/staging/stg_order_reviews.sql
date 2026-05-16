-- Deduplicate to one review per order_id (keep latest).
-- The Olist source has orders with multiple review_ids plus extra duplicate
-- rows from the --allow_quoted_newlines reload. Partitioning by order_id
-- ensures the LEFT JOIN in int_orders_enriched produces no fan-out.
SELECT
    review_id,
    order_id,
    review_score,
    review_comment_title,
    review_comment_message,
    review_creation_date    AS review_created_at,
    review_answer_timestamp AS review_answered_at
FROM {{ source('olist', 'order_reviews') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY order_id
    ORDER BY review_creation_date DESC
) = 1
