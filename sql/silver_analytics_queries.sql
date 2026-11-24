-- Query Silver Delta table via Microsoft Fabric SQL Analytics Endpoint
SELECT 
    store_city,
    payment_method,
    COUNT(transaction_id) AS valid_transactions,
    SUM(quantity) AS total_items_sold,
    SUM(total_revenue_zar) AS net_revenue_zar
FROM silver_retail_sales
WHERE status = 'Completed'
GROUP BY store_city, payment_method
ORDER BY net_revenue_zar DESC;
