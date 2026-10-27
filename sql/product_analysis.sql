
-- E-commerce Product Analytics
-- Source table: public.products

-- 1. Count the total number of products
SELECT
    COUNT(*) AS total_products
FROM products;


-- 2. Analyze product prices
SELECT
    ROUND(MIN(price)::numeric, 2) AS lowest_price,
    ROUND(MAX(price)::numeric, 2) AS highest_price,
    ROUND(AVG(price)::numeric, 2) AS average_price,
    ROUND(SUM(price)::numeric, 2) AS total_catalog_value
FROM products;


-- 3. Analyze products by category
SELECT
    category,
    COUNT(*) AS total_products,
    ROUND(AVG(price)::numeric, 2) AS average_price,
    ROUND(MIN(price)::numeric, 2) AS lowest_price,
    ROUND(MAX(price)::numeric, 2) AS highest_price
FROM products
GROUP BY category
ORDER BY total_products DESC, category ASC;


-- 4. Find the five most expensive products
SELECT
    id,
    title,
    category,
    price
FROM products
ORDER BY price DESC
LIMIT 5;


-- 5. Find products priced above the catalog average
SELECT
    id,
    title,
    category,
    price
FROM products
WHERE price > (
    SELECT AVG(price)
    FROM products
)
ORDER BY price DESC;
