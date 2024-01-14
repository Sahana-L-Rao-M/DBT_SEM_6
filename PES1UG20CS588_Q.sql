 --Join - airp,flights,ticket
--Name : Sahana Rao
--SRN: PES1UG20CS588

 --ORDER OF JOIN 1:
SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM flights F JOIN airp A JOIN ticket T ON T.flight_id = F.flight_id and A.city=F.source
where city like 'M%';

EXPLAIN SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM flights F JOIN airp A JOIN ticket T ON T.flight_id = F.flight_id and A.city=F.source
where city like 'M%';


CREATE INDEX city_index ON airp (city);

create index source_index on flights(source);

SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM flights F JOIN airp A JOIN ticket T ON T.flight_id = F.flight_id and A.city=F.source
where city like 'M%';

EXPLAIN SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM flights F JOIN airp A JOIN ticket T ON T.flight_id = F.flight_id and A.city=F.source
where city like 'M%';

DROP INDEX city_index ON airp;

DROP INDEX source_index ON flights;

--ORDER 2
SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM airp A JOIN flights F JOIN ticket T ON A.city=F.source AND T.flight_id = F.flight_id 
where city like 'M%';

EXPLAIN SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM airp A JOIN flights F JOIN ticket T ON A.city=F.source AND T.flight_id = F.flight_id 
where city like 'M%';

--ORDER3

SELECT A.airport_id,A.airport_name,F.source,F.destination,T.ssn,T.tid,T.seat_no,T.class
FROM airp A JOIN ticket T JOIN flights F  ON A.city=F.source AND T.flight_id = F.flight_id 
where city like 'M%';

--Joining tables flights, passengers and ticket

--order1 

explain SELECT P.first_name,P.SSN,F.flight_id,F.TimeOfFly,T.tid,T.seat_no
FROM passengers P left outer JOIN ticket T ON P.ssn=T.ssn
left outer JOIN flights F ON T.flight_id = F.flight_id
where P.age>20 and P.first_name like 'R%';

create index fname_index on passengers(first_name);
create index age_index on passengers(age);

DROP INDEX fname_index on passengers;

DROP INDEX age_index on passengers;

--order2

explain SELECT P.first_name,P.SSN,F.flight_id,F.TimeOfFly,T.tid,T.seat_no
FROM ticket T JOIN flights F ON T.flight_id = F.flight_id
right outer join passengers P ON P.ssn=T.ssn
where P.age>20 and P.first_name like 'R%';

create index fname_index on passengers(first_name);
create index age_index on passengers(age);

DROP INDEX fname_index on passengers;

DROP INDEX age_index on passengers;

--correlated and subquery
SELECT a.airport_name as Source_Airport,f.flight_id,f.source,f.destination,f.departure_time,f.arrival_time
FROM airp A INNER JOIN flights F ON f.source = A.city
WHERE 
   f.TimeOfFly = (
        SELECT MIN(TimeOfFly) 
        FROM flights F1
        WHERE F1.source=f.source and f1.destination=f.destination
    );

create index airportname_index on airp(airport_name);
create index source_index on flights(source);
create index destination_index on flights(destination);
create index airportid_index on airp(airport_id);
create index time_index on flights(TimeOfFly);

drop index airportname_index on airp;
drop index source_index on flights;
drop index destination_index on flights;
drop index airportid_index on airp;
drop index time_index on flights;


--Materialised view

CREATE VIEW f_p_t AS 
SELECT P.ssn,P.first_name,P.last_name,P.age,P.dob,P.gender,P.phone_number,T.tid,T.flight_id,T.class,T.seat_no,F.company,F.source,F.destination,F.arrival_time,F.departure_time,F.capacity,F.TimeOfFly
FROM passengers P inner JOIN ticket T ON P.ssn=T.ssn
inner JOIN flights F ON T.flight_id = F.flight_id;

SELECT first_name,last_name,phone_number,source,destination
FROM f_p_t
WHERE company like 'A%';

create index company_index on flights(company);
drop index company_index on flights;

--Function in where

CREATE INDEX idx_f_name ON passengers(first_name);

SELECT *
FROM passengers
WHERE LOWER(first_name) LIKE 'r%';

SELECT *
FROM passengers
WHERE first_name LIKE 'r%';


--Dynamic sql

PREPARE statement FROM 'SELECT * FROM passengers WHERE age =?';
SET @pas_age = 23;
EXECUTE statement USING @pas_age;

--Arrays

-- Create the table with an array column
CREATE TABLE new (
  id INT PRIMARY KEY,
  flight_number VARCHAR(50),
  departure_time DATETIME,
  arrival_time DATETIME,
  passenger_counts JSON
);

INSERT INTO new (id, flight_number, departure_time, arrival_time, passenger_counts)
VALUES
  (1, 'ABC123', '2023-03-20 10:00:00', '2023-03-20 12:00:00', '{"economy": 100, "business": 20, "first_class": 10}'),
  (2, 'XYZ456', '2023-03-20 15:00:00', '2023-03-20 18:00:00', '{"economy": 150, "business": 30, "first_class": 15}');


SELECT id, flight_number, JSON_EXTRACT(passenger_counts, '$.economy') as economy_count
FROM new
WHERE JSON_EXTRACT(passenger_counts, '$.economy') > 100;

EXPLAIN SELECT id, flight_number, JSON_EXTRACT(passenger_counts, '$.economy') as economy_count
FROM new
WHERE JSON_EXTRACT(passenger_counts, '$.economy') > 100;

CREATE INDEX idx_passenger_counts ON new(passenger_counts);

EXPLAIN SELECT id, flight_number, JSON_EXTRACT(passenger_counts, '$.economy') as economy_count
FROM new
WHERE JSON_EXTRACT(passenger_counts, '$.economy') > 100;

//large table

CREATE TABLE my_table (
id INT NOT NULL PRIMARY KEY,
data VARCHAR(255)
);

INSERT INTO my_table (id, data)
SELECT
ROW_NUMBER() OVER () AS id,
CONCAT('data_', FLOOR(RAND() * 1000000)) AS data
FROM
information_schema.columns c1,
information_schema.columns c2;

CREATE INDEX hash_idx ON my_table (data) USING HASH;

CREATE INDEX btree_idx ON my_table (data);

SELECT * FROM my_table WHERE data = 'data_123456';

explain SELECT * FROM my_table WHERE data = 'data_123456';

explain SELECT * FROM my_table WHERE data = 'data_123';

