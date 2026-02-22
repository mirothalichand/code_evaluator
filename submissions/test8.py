def is_prime(n: int) -> bool:
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return True