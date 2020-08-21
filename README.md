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
