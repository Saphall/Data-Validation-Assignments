solution: 


## employee

1. Managers are given a role other than manager.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM 
(
SELECT e.client_employee_id FROM
employee e JOIN employee mgr ON 
	e.client_employee_id = mgr.manager_employee_id
WHERE e."role" != 'manager'
) test_result	
```
> test passed.
<p>



2. Employees hired before age of 16.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM employee e 
WHERE CAST(e.hire_date AS DATE) - CAST(e.dob AS DATE) < 16;
```
> test passed.
<p>


3. Terminated employees has working_hour and fte.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM 
(
SELECT * FROM employee e 
except
SELECT * FROM employee e 
WHERE term_reason = '' AND term_date = ''
) terminated_employee 
WHERE CAST(fte AS FLOAT) > 0  OR CAST(weekly_hours AS FLOAT ) > 0
```
> test failed.
<p>


4. An employee manager of himself.

```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM employee e 
WHERE e.client_employee_id  = e.manager_employee_id ;
```
> test passed.
<p>


## timesheet

1. Number of teammates absent is greater than number of teammates.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status FROM 
(
WITH cte_teammate AS
	( SELECT department_id,shift_date, COUNT(*) AS num_of_teammates
	FROM timesheet t 
	GROUP BY department_id, shift_date 
	) 
		SELECT CAST(ct.num_of_teammates AS INT) - CAST(t.num_teammates_absent AS INT) AS working_teammates
		FROM timesheet t
		INNER JOIN cte_teammate ct ON 
		ct.department_id = t.department_id 
		WHERE CAST(ct.num_of_teammates AS INT) - CAST(t.num_teammates_absent AS INT) < 0
) test_result
```
> test failed.
<p>


2. Multiple timesheet detail of employee on same date.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM ( 
SELECT employee_id, COUNT(employee_id), shift_date
  FROM timesheet
  GROUP BY employee_id, shift_date
  HAVING COUNT(employee_id) > 1
) test_result
```
> test passed.
<p>


3. Check if absent employee has shift types.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
 FROM timesheet t 
WHERE attendance = 'false' AND shift_type = ''
```
> test passed.
<p>

4. Check if employee has both 'present' and 'absent' attendance on same date.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM (
SELECT employee_id , shift_date
FROM timesheet 
WHERE attendance = 'true'
intersect 
SELECT employee_id , shift_date 
FROM timesheet 
WHERE attendance = 'false'
) test_result
```
> test passed.
<p>





## product

1. Products have different prices in sales and product detail .
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status 
FROM (
SELECT product_id, price FROM sales
except
SELECT product_id, price FROM product
) test_result
```
> test passed.
<p>

2. Check if mrp of product is less than cost price 
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status 
FROM product p 
WHERE CAST (mrp AS FLOAT ) < CAST(price  AS FLOAT)
```
> test failed.
<p>

3 . Not active product being sold.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status 
FROM sales 
WHERE product_id IN (	
	SELECT product_id FROM product p
	WHERE CAST(active AS boolean) = false
)
```
> test passed.
<p>

4. Check if there is no information about whether product is active or not. 
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM product p 
WHERE active = ''
```
> test passed.
<p>

## sales 

1. Product is sold before created date of product i.e duration is sale is negative.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM product p JOIN sales s ON 
	s.product_id = p.product_id 
WHERE (CAST(s.bill_date AS DATE) - CAST(p.created_date AS DATE)) < 0
```
> test failed.
<p>


2. Same product different quantity at same TIME.
```
SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        else 'passed'
    END AS test_status
FROM 
(
SELECT bill_date, customer_id ,product_id,qty ,COUNT(*) FROM sales s 
GROUP BY bill_date, customer_id ,product_id ,qty 
HAVING COUNT(*) !=1
) test_result
```
> test failed.
<p>

3. Check if same bill number is assigned to different customers in same date. 
```
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    else 'passed'
  END AS test_result
FROM (
  SELECT COUNT(*)
  FROM sales
  GROUP BY bill_no, customer_id,bill_date
  HAVING COUNT(DISTINCT customer_id) > 1
) test_result;
```
> test passed.
<p>

4. Check if net_bill_amount less than gross_price
```
SELECT
  COUNT(*) AS impacted_record_count,
  CASE
    WHEN COUNT(*) > 0 THEN 'failed'
    else 'passed'
  END AS test_result
  FROM sales s 
 WHERE 
 	CAST(net_bill_amt AS FLOAT) < CAST(gross_price AS FLOAT)
```
> test passed.
<p>
