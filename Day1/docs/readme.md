SOLUTION: 

```
1. Check if a single employee is listed twice with multiple ids.

select count(*) as impacted_record_count,
	case when count(*) > 0 then 'failed' else 'passed' end as test_status
from (
select count(client_employee_id)
from employee 
group by client_employee_id 
having count(*) > 1 
) test_result;

```
> Test Passed.
<p>
<p>


```
2.  Check if part time employees are assigned other fte_status.

SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM employee e
INNER JOIN employee_raw er 
    ON e.client_employee_id = er.employee_id 
    AND cast(er.fte  as float ) < 0.7
    AND e.fte_status <> 'Part Time';
```
> Test Passed.
<p>
<p>


```
3. Check if termed employees are marked as active.

SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM employee
WHERE term_date IS NOT NULL AND is_active='TRUE';
```
> Test Failed.
<p>
<p>


```
4. Check if the same product is listed more than once in a single bill.

SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM (
	SELECT COUNT(product_id)
    FROM sales
    GROUP BY bill_no, product_id
    HAVING COUNT(product_id) > 1
    ) test_result;
```
> Test Passed.
<p>
<p>


```
 5. Check if the customer_id in the sales table does not exist in the customer table.
  
  SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM (
    SELECT DISTINCT customer_id FROM sales
    EXCEPT
    SELECT customer_id FROM customer
) test_result;
```
> Test Passed.
<p>
<p>


```
6. Check if there are any records where updated_by is not empty but updated_date is empty.

SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM sales
WHERE updated_by IS NOT NULL AND updated_date IS NULL;
```
> Test Passed.
<p>
<p>


```
7.Check if there are any hours worked that are greater than 24 hours in a day.


SELECT COUNT(*) AS impacted_record_count,
       CASE
           WHEN COUNT(*) > 0 THEN 'failed'
           ELSE 'passed'
       END  AS test_status
FROM timesheet
WHERE CAST(hours_worked AS FLOAT) > 24;
```
> Test Passed.
<p>
<p>


```
8. Check if non on-call employees are set as on-call.

SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM timesheet t
INNER JOIN timesheet_raw tr
    ON t.employee_id = tr.employee_id
     AND t.shift_date = tr.punch_apply_date
    AND tr.paycode <> 'ON_CALL'
    AND t.was_on_call = 'TRUE';
```
> Test Failed.
<p>
<p>


```
9. Check if the break is true for employees who have not taken a break at all.

SELECT
    COUNT(*) AS impacted_record_count,
    CASE
        WHEN COUNT(*) > 0 THEN 'failed'
        ELSE 'passed'
    END AS test_status
FROM timesheet t
INNER JOIN timesheet_raw tr
    ON t.employee_id = tr.employee_id
     AND t.shift_date = tr.punch_apply_date
    AND tr.paycode <> 'BREAK'
    AND t.has_taken_break = 'TRUE';
```
> Test Failed.
<p>
<p>


```
10. Check if the night shift is not assigned to the employees working on the night shift.

			-- consider day_shift: 5:00 - 14:00 
			-- evening_shift: 14:00 - 22:00
			-- night_shift: 22:00 - 5:00
			
			
SELECT COUNT(*) AS impacted_record_count,
       CASE
           WHEN COUNT(*) > 0 THEN 'failed'
           ELSE 'passed'
       END  AS test_status
FROM timesheet
WHERE shift_type <> 'Day' 
	AND shift_start_time between '22:00' and '5:00';
```
> Test Passed.
<p>
<p>




