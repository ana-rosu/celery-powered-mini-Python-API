from decimal import Decimal, getcontext
from math import factorial
from typing import Generator, Tuple, Optional

CHUDNOVSKY_C = 426880 * Decimal(10005).sqrt()
CHUDNOVSKY_K = 545140134
CHUDNOVSKY_M = 13591409
CHUDNOVSKY_X_BASE = -262537412640768000  # (-640320^3)

def calculate_pi(
    n_digits: int
) -> Generator[Tuple[float, Optional[str]], None, None]:
    """
    Compute Pi using the Chudnovsky series with per-term progress reporting.

    Args:
        n_digits: Number of decimal digits of Pi to compute (must be > 0)

    Yields:
        Tuple[float, Optional[str]]:
            - progress (0.0 to 1.0)
            - computed Pi (None until finished)
    """
    if n_digits <= 0:
        raise ValueError("Number of digits must be greater than 0.")

    getcontext().prec = n_digits + 10  # extra digits for intermediate precision

    pi_series_sum = Decimal(CHUDNOVSKY_M)
    term_index = 1
    total_terms_estimate = n_digits // 14 + 1  # ~14 digits per term

    while True:
        numerator = factorial(6 * term_index) * (CHUDNOVSKY_K * term_index + CHUDNOVSKY_M)
        denominator = factorial(3 * term_index) * factorial(term_index) ** 3 * (CHUDNOVSKY_X_BASE ** term_index)

        current_term = Decimal(numerator) / Decimal(denominator)
        pi_series_sum += current_term

        
        progress = min(term_index / total_terms_estimate, 1.0)
        yield progress, None

        term_index += 1

        # Stop when the term is smaller than desired precision
        if abs(current_term) < Decimal(10) ** (-n_digits):
            break
    pi_estimate = CHUDNOVSKY_C / pi_series_sum
    yield 1.0, str(+pi_estimate)[: n_digits + 2]
