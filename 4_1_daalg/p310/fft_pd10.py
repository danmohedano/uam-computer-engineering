"""Module with the implementation of:
    - Mini-Project 3: FFT and Multiplication of Polynomials and Numbers.
    Dynamic Programming.
"""
__author__ = 'Daniel Mohedano & Silvia Sopeña'

import numpy as np
from typing import List, Dict, Tuple, Callable
import random
import time
from itertools import combinations_with_replacement


def _extend_table(t: np.ndarray, length: int = -1) -> np.ndarray:
    """Extends a table to the smallest power of 2 greater than the number of
    elements in t.

    Args:
        t (np.ndarray): Table.
        length (int): Desired length.

    Returns:
        np.ndarray: The extended table.
    """
    if length != -1:
        a = int(np.ceil(np.log2(length)))
    else:
        a = int(np.ceil(np.log2(len(t))))

    if 2 ** a == len(t):
        return t
    else:
        return np.concatenate((t, [0]*((2 ** a) - len(t))))


def _gen_point(j: int, N: int) -> complex:
    """Generates the complex value for the point j out of N points.

    Args:
        j (int): Point's index.
        N (int): Total of points.

    Returns:
        (complex): Point.
    """
    return np.exp(2 * np.pi * 1j * j / N)


def _degree(pol: List[int]) -> int:
    """Degree of a polynomial.

    Args:
        pol (list): List of coefficients of the polynomial.

    Returns:
        int: Degree.
    """
    deg = 0
    for i in range(len(pol)):
        if pol[i] != 0:
            deg = i

    return deg


def fft(t: np.ndarray) -> np.ndarray:
    """Calculates the FFT of table t.

    Args:
        t (np.ndarray): Table.

    Returns:
        np.ndarray: Result of FFT.
    """
    if len(t) == 1:
        return t

    t = _extend_table(t)
    N = len(t)

    t_even = np.array([t[2 * i] for i in range(N // 2)])
    t_odd = np.array([t[2 * i + 1] for i in range(N // 2)])

    f_even = fft(t_even)
    f_odd = fft(t_odd)

    result = [None] * N

    for j in range(N):
        result[j] = f_even[j % (N // 2)] + _gen_point(j, N)*f_odd[j % (N // 2)]

    return np.array(result)


def invert_fft(
        t: np.ndarray,
        fft_func: Callable[[np.ndarray], np.ndarray] = fft) -> np.ndarray:
    """Calculates the inverse FFT with the provided function.

    Args:
        t (np.ndarray): Table.
        fft_func (func): Implementation of FFT.

    Returns:
        np.ndarray: Result of the inverse FFT.
    """
    t = _extend_table(t)
    N = len(t)

    # 1. Conjugate
    t = np.array([np.conj(x) for x in t])

    # 2. Apply FFT
    result = fft_func(t)

    # 3&4. Conjugate again and divide by 2 ** k = N
    result = np.array([np.conj(x) / N for x in result])

    return result


def rand_polynomial(long: int = 2**10, base: int = 10) -> List[int]:
    """Generates a list with the coefficients of the polynomial with degree
    length - 1.

    Args:
        long (int): Length of the list. long - 1 identifies the degree of the
        polynomial.
        base (int): Base of the coefficients.

    Returns:
        list: List with the coefficients of the polynomial.
    """
    return [random.randint(0, base - 1) for i in range(long - 1)] + \
        [random.randint(1, base - 1)]


def poli_2_num(l_pol: List[int], base: int = 10) -> int:
    """Evaluates the polynomial with a certain base using Horner's rule.

    Args:
        l_pol (list): List of polynomial's coefficients.
        base (int): Base of the polynomial.

    Returns:
        int: Evaluation on the base.
    """
    x = l_pol[-1]

    for i in range(len(l_pol) - 2, -1, -1):
        x = x * base + l_pol[i]

    return x


def rand_number(num_digits: int, base: int = 10) -> int:
    """Generates a random int with num_digits figures in the base provided.

    Args:
        num_digits (int): Number of digits.
        base (int): Base of the number.

    Returns:
        int: The random number.
    """
    return poli_2_num(rand_polynomial(num_digits, base), base)


def num_2_poli(num: int, base: int = 10) -> List[int]:
    """Converts a number into its polynomial representation in the base given.

    Args:
        num (int): Number to convert.
        base (int): Base of the polynomial.

    Returns:
        list: The polynomial.
    """
    pol = []

    while num != 0:
        pol.append(num % base)
        num = num // base

    return pol


def mult_polynomials_fft(
        l_pol_1: List[int], l_pol_2: List[int],
        fft_func: Callable[[np.ndarray], np.ndarray] = fft) -> List[int]:
    """Multiplies two polynomials applying the FFT algorithm.

    Args:
        l_pol_1 (list): List of coefficients of polynomial 1.
        l_pol_2 (list): List of coefficients of polynomial 2.
        fft_func (function): Function of FFT.

    Returns:
        list: Coefficients resulting of the multiplication.
    """
    length1 = _degree(l_pol_1)
    length2 = _degree(l_pol_2)

    pol_1 = _extend_table(np.array(l_pol_1), length1 + length2 + 1)
    pol_2 = _extend_table(np.array(l_pol_2), length1 + length2 + 1)

    # 1. Compute values of polynomials in special points (FFT)
    fft1 = fft_func(pol_1)
    fft2 = fft_func(pol_2)

    # 2. PQ(Xi) = P(Xi)Q(Xi)
    mult_points = np.array([fft1[i] * fft2[i] for i in range(len(pol_1))])

    # 3. Inverse FFT
    mult_coeff = invert_fft(np.array(mult_points), fft_func)

    return [round(x) for x in mult_coeff.real]


def mult_numbers_fft(
        num1: int, num2: int,
        fft_func: Callable[[np.ndarray], np.ndarray] = fft) -> int:
    """Multiplies integers using the FFT.

    Args:
        num1 (int): The first integer.
        num2 (int): The second integer.
        fft_func (function): The FFT function.

    Returns:
        int: The result of the multiplication.
    """
    pol1 = num_2_poli(num1)
    pol2 = num_2_poli(num2)

    result = mult_polynomials_fft(pol1, pol2, fft_func)

    return poli_2_num(result)


def time_fft(
        n_tables: int, num_coefs_ini: int, num_coefs_fin: int, step: int,
        fft_func: Callable[[np.ndarray], np.ndarray] = fft) -> List[float]:
    """Times the execution of the FFT implementation provided.

    Args:
        n_tables (int): Number of tables to generate.
        num_coefs_ini (int): Initial number of coefficients.
        num_coefs_fin (int): Final number of coefficients.
        step (int): Step for the number of coefficients.
        fft_func (function): FFT implementation.

    Returns:
        list: List with the average times of the FFT.
    """
    results = []
    n_coeffs = num_coefs_ini
    while n_coeffs <= num_coefs_fin:
        total_time = 0.0

        for i in range(n_tables):
            pol = rand_polynomial(n_coeffs)

            t = time.time()
            fft_func(np.array(pol))
            t = time.time() - t

            total_time += t

        results.append(total_time / n_tables)
        n_coeffs += step

    return results


def time_mult_polynomials_fft(
        n_pairs: int, num_coefs_ini: int, num_coefs_fin: int, step: int,
        fft_func: Callable[[np.ndarray], np.ndarray] = fft) -> List[float]:
    """Times the execution of multiplication of polynomials.

    Args:
        n_pairs (int): Number of pairs generated.
        num_coefs_ini (int): Initial number of coefficients.
        num_coefs_fin (int): Final number of coefficients.
        step (int): Step for the number of coefficients.
        fft_func (function): FFT implementation.

    Returns:
        list: List with the average times of the multiplication.
    """
    results = []
    n_coeffs = num_coefs_ini
    while n_coeffs <= num_coefs_fin:
        total_time = 0.0

        for i in range(n_pairs):
            pol1 = rand_polynomial(n_coeffs)
            pol2 = rand_polynomial(n_coeffs)

            t = time.time()
            mult_polynomials_fft(pol1, pol2, fft_func)
            t = time.time() - t

            total_time += t

        results.append(total_time / n_pairs)
        n_coeffs += step

    return results


def time_mult_numbers_fft(
        n_integers: int, num_digits_ini: int,
        num_digits_fin: int, step: int,
        fft_func: Callable[[np.ndarray], np.ndarray] = fft) -> List[float]:
    """Times the execution of multiplication of numbers.

    Args:
        n_integers (int): Number of integers generated.
        num_digits_ini (int): Initial number of digits.
        num_digits_fin (int): Final number of digits.
        step (int): Step for the number of digits.
        fft_func (function): FFT implementation.

    Returns:
        list: List with the average times of the multiplication.
    """
    results = []
    n_digits = num_digits_ini
    while n_digits <= num_digits_fin:
        total_time = 0.0

        for i in range(n_integers):
            num1 = rand_number(n_digits)
            num2 = rand_number(n_digits)

            t = time.time()
            mult_numbers_fft(num1, num2, fft_func)
            t = time.time() - t

            total_time += t

        results.append(total_time / n_integers)
        n_digits += step

    return results


def min_coin_number(c: int, l_coins: List[int]) -> int:
    """Calculates the minimum number of l_coins coins needed to give c change.

    Args:
        c (int): Desired change.
        l_coins (list): Type of coins (values).

    Returns:
        int: Minimum number of coins needed.
    """
    coins = sorted(l_coins)
    ci = {i: coins[i] for i in range(len(coins))}
    dp_matrix = np.zeros([len(coins), c + 1])

    # TODO: ask if 1 always a coin
    # Initilize first row of matrix: n(1,c) = c
    for i in range(dp_matrix.shape[1]):
        dp_matrix[0][i] = i

    # Dynamic loop: n(i,c) = min{n(i-1,c), 1+n(i,c-vi)}
    for i in range(1, dp_matrix.shape[0]):
        for j in range(1, dp_matrix.shape[1]):
            no_i = dp_matrix[i-1][j]
            yes_i = np.inf

            if j >= ci[i]:
                yes_i = 1 + dp_matrix[i][j - ci[i]]

            dp_matrix[i][j] = min(no_i, yes_i)

    return int(dp_matrix[-1][-1])


def optimal_change(c: int, l_coins: List[int]) -> Dict[int, int]:
    """Returns a dict with the coins needed to give change c.

    Args:
        c (int): Desired change.
        l_coins (list): Coin values.

    Returns:
        dict: Amount of coins needed of each type to return change c.
    """
    n_coins = min_coin_number(c, l_coins)

    for x in combinations_with_replacement(l_coins, n_coins):
        if sum(x) == c:
            return {coin: x.count(coin) for coin in l_coins}

    return {}


def bellman_ford(u: int, mg: np.ndarray) -> Tuple[Dict[int, float],
                                                  Dict[int, int]]:
    """Applies Bellman-Ford's algorithm to graph mg starting at node u.

    Args:
        u (int): Starting node.
        mg (np.ndarray): Adjacency matrix of the graph.

    Returns:
        dict: Minimum distances between u and every other node.
        dict: Previous node dictionary.
    """
    d = {k: mg[u, k] for k in range(mg.shape[0])}
    p = {node: -1 for node in range(mg.shape[0])}
    p[u] = u

    for k in range(1, mg.shape[0]):
        for i in range(mg.shape[0]):
            if i == u:
                continue
            for j in range(mg.shape[0]):
                new_cost = d[j] + mg[j, i]
                if d[i] > new_cost:
                    d[i] = new_cost
                    p[i] = j

    return d, p


def max_length_common_subsequence(str_1: str, str_2: str) -> np.ndarray:
    """Calculates the array of partial common subsequence lengths.

    Args:
        str_1 (str): String 1.
        str_2 (str): String 2.

    Returns:
        np.ndarray: Array of partial common subsequence lengths.
    """
    dp_matrix = np.zeros([len(str_2) + 1, len(str_1) + 1])

    for i in range(1, dp_matrix.shape[0]):
        for j in range(1, dp_matrix.shape[1]):
            if str_2[i - 1] == str_1[j - 1]:
                dp_matrix[i][j] = 1 + dp_matrix[i - 1][j - 1]
            else:
                dp_matrix[i][j] = max(dp_matrix[i][j - 1], dp_matrix[i - 1][j])

    return dp_matrix


def find_max_common_subsequence(str_1: str, str_2: str) -> str:
    """Calculates a possible common subsequence of maximum length.

    Args:
        str_1 (str): String 1.
        str_2 (str): String 2.

    Returns:
        str: Possible common subsequence of maximum length.
    """
    matrix = max_length_common_subsequence(str_1, str_2)
    string = ''

    i, j = matrix.shape[0] - 1, matrix.shape[1] - 1

    while matrix[i][j] != 0:
        if matrix[i][j] == matrix[i - 1][j]:
            i -= 1
        elif matrix[i][j] == matrix[i][j - 1]:
            j -= 1
        else:
            string = str_1[j - 1] + string
            i -= 1
            j -= 1

    return string


def optimal_order(l_probs: List[float]) -> Tuple[np.ndarray, np.ndarray]:
    """Calculates the optimal search binary tree.

    Args:
        l_probs (list): List of probabilities of each key.

    Returns:
        np.ndarray: Matrix with optimal search costs.
        np.ndarray: Subtree roots.
    """
    N = len(l_probs)
    dp_matrix = np.zeros([N, N])
    roots = np.ones([N, N], dtype=int)*-1

    for L in range(N-1, -1, -1):
        for R in range(L, N):
            sum_pi = sum(l_probs[L:R+1])

            if L != R:
                min_cj = np.inf
                for j in range(L, R + 1):
                    c_L, c_R = 0, 0
                    if j - 1 >= L:
                        c_L = dp_matrix[L][j-1]
                    if j + 1 <= R:
                        c_R = dp_matrix[j+1][R]

                    if c_L + c_R < min_cj:
                        min_cj = c_L + c_R
                        roots[L][R] = j
            else:
                min_cj = 0

            dp_matrix[L][R] = sum_pi + min_cj

    return dp_matrix, roots


def _recursive_ordering(m_roots: np.ndarray, left: int, right: int,
                        ordering: List[int]):
    """ Recursive function for the ordering of the roots

    Args:
        m_roots (np.ndarray): Matrix of roots.
        l (int): Left index.
        r (int): Right index.
        ordering (list): Ordering of the roots
    """
    # Base case
    if left == right:
        ordering.append(left)
        return

    # Find root of tree lr
    root = m_roots[left][right]
    ordering.append(root)
    if left <= root - 1:
        _recursive_ordering(m_roots, left, root - 1, ordering)
    if root + 1 <= right:
        _recursive_ordering(m_roots, root + 1, right, ordering)

    return


def list_opt_ordering_search_tree(m_roots: np.ndarray,
                                  l: int, r: int) -> List[int]:
    """Calculates the insertion order of the keys corresponding to the optimal
    binary search tree.

    Args:
        m_roots (np.ndarray): Matrix of roots.
        l (int): Left index.
        r (int): Right index.

    Returns:
        list: Insertion order of the keys.
    """
    ordering: List[int] = []

    _recursive_ordering(m_roots, l, r, ordering)

    return ordering


if __name__ == '__main__':
    original = np.array([1, 2, 1])
    result = fft(original)
    inv_result = invert_fft(result, fft)

    print("Original: ", original)
    print("FFT: ", result)
    print("Inverse FFT: ", inv_result)

    x1 = 123456789
    x2 = 123456789

    print(mult_numbers_fft(x1, x2))
    print(x1 * x2)

    c = 7
    l_coins = [1, 3, 4, 5]
    print(min_coin_number(c, l_coins))
    print(optimal_change(c, l_coins))

    str_1 = 'forraje'
    str_2 = 'zarzajo'

    print(max_length_common_subsequence(str_1, str_2))
    print(find_max_common_subsequence(str_1, str_2))

    l_probs = [0.22, 0.18, 0.20, 0.05, 0.25, 0.02, 0.08]
    optimal_bst, roots = optimal_order(l_probs)
    print(optimal_bst)
    print(roots)
    print(list_opt_ordering_search_tree(roots, 0, 6))
