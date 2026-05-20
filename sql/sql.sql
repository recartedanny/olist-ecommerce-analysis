-- Query 1: Average price, review score and order volume by product category
SELECT 
    p.product_category_name AS category,
    AVG(i.price) AS avg_price,
    AVG(r.review_score) AS avg_review,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM products p
INNER JOIN items i ON p.product_id = i.product_id
INNER JOIN orders o ON o.order_id = i.order_id
INNER JOIN reviews r ON r.order_id = o.order_id
GROUP BY p.product_category_name
ORDER BY total_orders DESC;

-- Query 2: Monthly sales evolution by year
SELECT 
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
    COUNT(DISTINCT order_id) AS total_orders
FROM orders
GROUP BY year, month
ORDER BY year, month;

-- Query 3: Impact of delivery timing on customer satisfaction
WITH delivery AS (
    SELECT 
        o.order_id,
        COALESCE(EXTRACT(EPOCH FROM (order_delivered_customer_date - order_estimated_delivery_date))/86400, 0) AS days_diff,
        CASE 
            WHEN DATE(order_delivered_customer_date) < DATE(order_estimated_delivery_date) THEN 'Early'
            WHEN DATE(order_delivered_customer_date) = DATE(order_estimated_delivery_date) THEN 'On Time'
            WHEN DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date) THEN 'Late'
        END AS delivered_status,
        r.review_score
    FROM orders o 
    INNER JOIN reviews r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL 
    AND o.order_estimated_delivery_date IS NOT NULL
)
SELECT 
    delivered_status,
    AVG(CASE WHEN review_score <= 2 THEN 1.0 ELSE 0 END) * 100 AS pct_negative_reviews,
    AVG(review_score) AS avg_review,
    COUNT(order_id) AS total_orders
FROM delivery
GROUP BY delivered_status;
