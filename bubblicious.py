import time


# I want a timing decorator to measure the efficiency of a few different approaches.
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} took {elapsed_time:.6f} seconds to run.")
        return result
    return wrapper

####################################
# Naive Code
####################################
# O(sqrt(num))
def is_prime_simple(num):
    if num < 2:
        return False
    # Iterate to the sqrt of the number to find all potential factors of our number.
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


@timing_decorator
# O(n*sqrt(m))
def find_primes_in_range(start, end):
    primes = []
    for num in range(max(2, start), end + 1):
        if is_prime_simple(num):
            primes.append(num)
    return primes


@timing_decorator
def find_bub_numbers_hex_conversion(prime_numbers):
    b_results = []
    for num in prime_numbers:
        if hex(num)[-1] == 'b':
            b_results.append(num)
    return b_results


####################################
# Optimized Code
####################################
@timing_decorator
# O(n*log(log(n)))
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


@timing_decorator
def find_bub_numbers_mod(prime_numbers):
    b_results = []
    for num in prime_numbers:
        if (num-11) % 16 == 0:
            b_results.append(num)
    return b_results


def main():  
    end_range = 100000
    prime_numbers = sieve_of_eratosthenes(end_range)
    results = find_bub_numbers_mod(prime_numbers)
    print(len(results))


if __name__ == "__main__":
    main()
