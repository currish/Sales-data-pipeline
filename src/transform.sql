-- Daily Sales
Drop table if exists daily_sales;

create table daily_sales as 
select 
    billing_date as date,
    sum(gross_revenue) as total_revenue,
    sum(total_amount_corrected) AS total_corrected_amount
from sales_raw
group by billing_date;    

-- Monthly Sales
drop table if exists monthly_sales;

create table monthly_sales as 
select date_trunc('month', billing_date) as month,
sum(gross_revenue) as total_revenue,
sum(total_amount_corrected) AS total_corrected_amount
from sales_raw
group by date_trunc('month', billing_date);

-- Top Items by Revenue
drop table if exists top_items;

create table top_items as 
select item_name,
sum(gross_revenue) as total_revenue,
sum(total_amount_corrected) AS total_corrected_amount
from sales_raw
group by item_name
order by sum(gross_revenue) desc;