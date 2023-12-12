# Bubblicious

## The Question
A "Bubblicious Number" is an integer that is prime and whose hexadecimal representation has a last digit of B. The first three are 11, 43 and 59. How many Bubblicious Numbers are there between one and 100,000?

## The approach

### Our Naive Approach
Let's tackle this problem in pieces. To start, we can think of the most naive way to solve this. Let's loop through all numbers in the given range, check if it's prime, convert the prime number into hexadecimal, and see if it ends in 'B'.

To determine if a number is prime, we first take the number and find its square root. A simple example would be 100. `sqrt(100) = 10`. We can loop from 2 to 10 to find any potential factors of 100, not 1 and the number itself. If any number in this range divides evenly into our number, then we know our number is not prime!

``` python
def is_prime_simple(num):
    if num < 2:
        return False
    # Iterate to the sqrt of the number to find all potential factors of our number.
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
```

We then use this function to find all prime numbers in a given range.
``` python
def find_primes_in_range(start, end):
    primes = []
    for num in range(max(2, start), end + 1):
        if is_prime_simple(num):
            primes.append(num)
    return primes
```

``` python
def main():  
    start_range = 0
    end_range = 1000000
    result = find_primes_in_range(start_range, end_range)
    print(len(result))
    # > 9592
```

Great! now, how can we determine if the hexadecimal representation of any of these numbers has a last digit of B? Well, we can convert the number to hex, then check the final index of the hex string, and see if it ends in B.

``` python
def find_b_ending_prime_numbers(start, end):
    b_results = []
    results = find_primes_in_range(start, end)
    for num in results:
        if hex(num)[-1] == 'b' or hex(num)[-1] == 'B':
            print(num, hex(num))
            b_results.append(num)
    return b_results
```

Our final result would look like this
```python
def main():  
    start_range = 0
    end_range = 100000
    b_results = find_b_ending_prime_numbers(start_range, end_range)
    print(len(b_results))
    # > 1201
```

This seems _fine_ but how long does it take to run?

Here's a quick function timing wrapper
```python
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.6f} seconds to run.")
        return result
    return wrapper
```

Re-running our code, we get `find_b_ending_prime_numbers took 0.074330 seconds to run.`
Seems.. ok? Well, doing a quick check of our time complexity, we get `O(n*sqrt(m))`.
So fairly linear. I'm not a prime number calculation expert, but my first instinct was that we could do something a little quicker. 

After a few Google searches, I found another algorithm that should be faster than what I originally implemented and learned while in middle school.

### Finding a better approach
[Wikipedia](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes) defines the Sieve of Eratosthenes as, "an ancient algorithm for finding all prime numbers up to any given limit." This felt fairly promising.

Here's my implementation of it
```python
def sieve_of_eratosthenes(limit):
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False  # 0 and 1 are not prime

    for num in range(2, int(limit**0.5) + 1):
        if is_prime[num]:
            primes.append(num)
            for multiple in range(num**2, limit + 1, num):
                is_prime[multiple] = False

    for num in range(int(limit**0.5) + 1, limit + 1):
        if is_prime[num]:
            primes.append(num)
    return primes
```

But how does it work? Well, it uses a similar factorization trick as what is used to determine if a single number is prime. It creates a boolean array and initially marks each number (except 0 and 1) as prime through the defined limit. It takes the defined upper limit (100,000 in this example) and only iterates through the square root of that limit. Starting at 2, it checks if the current number is prime. If that number is prime, it takes all multiples of that number and marks those as not prime (2 is prime, but 4, 6, 8, 10, 12, .., 99998, 100000 are all not prime). At the end of the loop, we have an array of prime numbers. We can define the time complexity of this function as `O(n*log(log(n)))`. Much better!

Let's find the time difference between these two approaches:
```
find_primes_in_range took 0.077833 seconds to run.
sieve_of_eratosthenes took 0.004868 seconds to run.
```

Wowza! That's roughly 94% faster than the naive approach. But what else can we optimize? Well, I don't really like my current "Last digit of 'B'" logic.


### What does it mean for a hexadecimal number to end in B?
B in hexadecimal equates to a decimal 11. 
Let's go through the first few hexadecimal numbers ending in B
1. 0B -> 11
2. 1B -> 27
3. 2B -> 43 (also our first Bubblicious number)

This can be converted into a formula `(16n + 11) = m`

So to quickly tell if a number is Bubblicious, we can reduce this to `(m-11) % 16 == 0 `

Let's add this new logic to our code and calculate the difference again.
``` python
def main():  
    end_range = 100000
    prime_numbers = sieve_of_eratosthenes(end_range)
    find_bub_numbers_hex_conversion(prime_numbers)
    find_bub_numbers_mod(prime_numbers)
```

```
find_bub_numbers_hex_conversion took 0.000614 seconds to run.
find_bub_numbers_mod took 0.000316 seconds to run.
```
Amazing! Roughly half the time needed.

I'm sure there are plenty of other optimizations that could be done, but I'm a big believer in getting something to about 80% of as good as I can make it and sharing the results quickly. My version of 100% perfect is not the same as others, so pouring all my effort into that final 20% has significantly diminishing returns. I would rather share my results and get instant feedback from others. 

I hope you find this insightful. Cheers!