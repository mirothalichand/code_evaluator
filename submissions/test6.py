def is_armstrong(n: int) -> bool:
    digits = str(n)
    return sum(int(d) for d in digits) == n