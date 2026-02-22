def is_armstrong(n: int) -> bool:
    # only checks for 3-digit numbers
    total = 0
    temp = n
    while temp > 0:
        digit = temp % 10
        total += digit ** 3
        temp //= 10
    return total == n