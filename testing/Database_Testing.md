# Database Testing


## Objective

Verify database accuracy and data consistency.


## Test Cases


### TC_DB_001

Test:

Insert transaction record


Expected:

Record stored successfully


Result:

PASS



### TC_DB_002

Test:

Retrieve transaction history


Expected:

Correct transaction list displayed


Result:

PASS



## SQL Validation


Check missing risk scores:


SELECT *
FROM transactions
WHERE risk_score IS NULL;


Expected:

No invalid records.