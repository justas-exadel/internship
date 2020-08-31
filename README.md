# internship
## First task

Write a script that calculates n-th fibonnaci number. The script has to contain two functions
  1. One function calculates Fibonnaci number using iterative algorithm
  1. Another function calculates Fibonnaci number using recursive algorithm

Requirements
1. Functions have to handle erros if we pass bad arguments DONE
2. A function call result has to be printed as "Function name (argument value) = function value, duration xx.xxx seconds" DONE
4. Add cache, check recursion depth DONE
6. save cache for the next run - serialize/deserialize DONE

3. Unit tests
5. Add arguments parsing - fib 1 2 3 4 5 fib_recursive 4 5 6 7 8


Creat solution pull request.

## Second task

Splits long message to multiple messages in order to fit within an arbitrary message length limit (useful for SMS, Twitter, etc.).

```
import msgsplitter
result = msgsplitter.split("Hello, this is a really long message.", length_limit=30)
print(result)
['Hello, this is a really (1/2)', 'long message. (2/2)']
```

## Third task
#### Task 1 ####
Implement the class 'Car' that meets the requirements defined below.
Requirements for the car number:
 * must have format: 3 capital letters minus 3 digits (e.g. ABC-001)
 * must be unique (not registered before)
 * once a valid number is assigned to the car, it can't be modified

Create unit tests in order to make sure that the code conforms already mentioned scenarios.
```
a = Car('AAA-002')
print(a.car_number)
AAA-002
print(a.registered_cars)
Registered cars: AAA-002
print(a.car_count)
1
print(a.status)
Successfully registered

b = Car()
b.car_number = "AAA-001"
print(b.car_number)
AAA-001
print(b.registered_cars)
Registered cars: AAA-001, AAA-002
print(b.car_count)
2
print(b.status)
Successfully registered

b.car_number = "AAA-003"
print(b.car_number)
AAA-001
print(b.registered_cars)
Registered cars: AAA-001, AAA-002
print(b.car_count)
2
print(b.status)
The car has already number assigned

c = Car('AA1-001')
print(c.car_number)
None
print(c.registered_cars)
Registered cars: AAA-001, AAA-002
print(c.car_count)
2
print(c.status)
Not valid number

c.car_number = "AA1-001"
print(c.car_number)
None
print(c.registered_cars)
Registered cars: AAA-001, AAA-002
print(c.car_count)
2
print(c.status)
Not valid number

d = Car()
d.car_number = 'AAA-002'
print(d.car_number)
None
print(d.registered_cars)
Registered cars: AAA-001, AAA-002
print(d.car_count)
2
print(d.status)
Already registered number

del d
print(c.registered_cars)
Registered cars: AAA-001, AAA-002
print(c.car_count)
2

del b
print(c.registered_cars)
Registered cars: AAA-002
print(c.car_count)
1

del a
print(c.registered_cars)
There are no registered cars at this moment
print(c.car_count)
0
```
#### Task 2 ####
Create a microservice that uses previously implemented 'Car' class.
It should be able to execute HTTP requests defined below.
You can choose a web microframework whatever you are comfortable with.
Think of how you will ensure data persistence, when the server is restarted.
```
Request:
curl -X POST \
  http://localhost:5000/add_car \
  -H 'Content-Type: application/json' \
  -d '{"number": "AAA-001"}'
Response:
{"info": "Successfully registered"}

Request:
curl -X POST \
  http://localhost:5000/add_car \
  -H 'Content-Type: application/json' \
  -d '{"number": "AAA-002"}'
Response:
{"info": "Successfully registered"}

Request:
curl -X GET \
  http://localhost:5000/registered_cars
Response:
{"info": "Registered cars: AAA-001, AAA-002"}

Request:
curl -X DELETE \
  http://localhost:5000/delete_car?number=AAA-002
Response:
{"info": "Deleted successfully"}

Request:
curl -X GET \
  http://localhost:5000/registered_cars
Response:
{"info": "Registered cars: AAA-001"}
```
#### Task 3 ####
Using docker containers deploy locally already existing microservice solution.

