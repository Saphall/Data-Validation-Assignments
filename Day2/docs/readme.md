SOLUTION: 


## Employee

1. Managers are given a role other than manager.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from 
(
select e.client_employee_id from
employee e join employee mgr on 
	e.client_employee_id = mgr.manager_employee_id
where e."role" != 'Manager'
) test_result	
```
> Test Passed.
<p>



2. Employees hired before age of 16.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from employee e 
where cast(e.hire_date as date) - cast(e.dob as date) < 16;
```
> Test Passed.
<p>


3. Terminated Employees has working_hour and fte.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from 
(
select * from employee e 
except
select * from employee e 
where term_reason = '' and term_date = ''
) terminated_employee 
where cast(fte as float) > 0  or cast(weekly_hours as float ) > 0
```
> Test Failed.
<p>


4. An employee manager of himself.

```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from employee e 
where e.client_employee_id  = e.manager_employee_id ;
```
> Test Passed.
<p>


## Timesheet

1. Number of teammates absent is greater than number of teammates.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status from 
(
with cte_teammate as
	( select department_id,shift_date, count(*) as num_of_teammates
	from timesheet t 
	group by department_id, shift_date 
	) 
		select cast(ct.num_of_teammates as int) - cast(t.num_teammates_absent as int) as working_teammates
		from timesheet t
		inner join cte_teammate ct on 
		ct.department_id = t.department_id 
		where cast(ct.num_of_teammates as int) - cast(t.num_teammates_absent as int) < 0
) test_result
```
> Test Failed.
<p>


2. Multiple timesheet detail of employee on same date.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from ( 
SELECT employee_id, COUNT(employee_id), shift_date
  FROM timesheet
  GROUP BY employee_id, shift_date
  HAVING COUNT(employee_id) > 1
) test_result
```
> Test Passed.
<p>


3. check if absent employee has shift types.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
 from timesheet t 
where attendance = 'FALSE' and shift_type = ''
```
> Test Passed.
<p>

4. check if employee has both 'present' and 'absent' attendance on same date.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from (
select employee_id , shift_date
from timesheet 
where attendance = 'TRUE'
intersect 
select employee_id , shift_date 
from timesheet 
where attendance = 'false'
) test_result
```
> Test Passed.
<p>





## Product

1. Products have different prices in sales and product detail .
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status 
from (
SELECT product_id, price FROM sales
EXCEPT
SELECT product_id, price FROM product
) test_result
```
> Test Passed.
<p>

2. check if mrp of product is less than cost price 
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status 
from product p 
where cast (mrp as float ) < cast(price  as float)
```
> Test Failed.
<p>

3 . Not Active product being sold.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status 
from sales 
where product_id in (	
	select product_id from product p
	where cast(active as boolean) = false
)
```
> Test Passed.
<p>

4. check if there is no information about whether product is active or not. 
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from product p 
where active = ''
```
> Test Passed.
<p>

## Sales 

1. Product is sold before created date of product i.e duration is sale is negative.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from product p join sales s on 
	s.product_id = p.product_id 
where (cast(s.bill_date as date) - cast(p.created_date as date)) < 0
```
> Test Failed.
<p>


2. Same product different quantity at same time.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
from 
(
select bill_date, customer_id ,product_id,qty ,count(*) from sales s 
group by bill_date, customer_id ,product_id ,qty 
having count(*) !=1
) test_result
```
> Test Failed.
<p>

3. check if same bill number is assigned to different customers in same date. 
```
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
FROM (
  SELECT COUNT(*)
  FROM sales
  GROUP BY bill_no, customer_id,bill_date
  HAVING COUNT(DISTINCT customer_id) > 1
) test_result;
```
> Test Passed.
<p>

4. check if net_bill_amount less than gross_price
```
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    ELSE 'passed'
  END AS test_result
  from sales s 
 where 
 	cast(net_bill_amt as float) < cast(gross_price as float)
```
> Test Passed.
<p>
