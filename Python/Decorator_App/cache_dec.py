from functools import lru_cache
from functools import cache
from tools import measure


#@lru_cache
def count_vowels(statement: str) -> int:
    return sum(statement.count(vowels) for vowels in "aeiouAEIOU")


@lru_cache(maxsize=None)
def fib_with_cache(n):
    if(n<2):
        return n
    return fib_with_cache(n-1) + fib_with_cache(n-2)


def fib_without_cache(n):
    if(n<2):
        return n
    return fib_without_cache(n-1) + fib_without_cache(n-2)

@measure
def main(n: int):
    statements: [str] = ["Hello World!",
                         "How are you",
                         "How long have you been here"]

    return fib_with_cache(n)
"""
    for sentance in statements:
        for i in range(1_000_000):
             count_vowels(sentance)
"""

if __name__ == '__main__':
    print(main(300))