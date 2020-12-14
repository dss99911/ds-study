#temporary relation
#https://www.geeksforgeeks.org/sql-with-clause/

#get single column
WITH temporaryTable(averageValue) as
    (SELECT avg(Salary)
    from Employee),
        SELECT EmployeeID,Name, Salary
        FROM Employee, temporaryTable
        WHERE Employee.Salary > temporaryTable.averageValue;

# get two column
WITH totalSalary(Airline, total) as
    (SELECT Airline, sum(Salary)
    FROM Pilot
    GROUP BY Airline),
    airlineAverage(avgSalary) as
    (SELECT avg(Salary)
    FROM Pilot )
    SELECT Airline
    FROM totalSalary, airlineAverage
    WHERE totalSalary.total > airlineAverage.avgSalary;

with a as (
    select * from log.parsed_message
    limit 1
), b as (
    select * from log.message
    limit 2
);

select * from a