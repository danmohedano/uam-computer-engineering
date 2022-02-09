import pytest
import fft_pd10
import random
import numpy as np

@pytest.fixture
def n_tries():
    return random.randint(5, 10)


def test_fft(n_tries):
    N = n_tries
    for i in range(N):
        num_table = np.random.random(2**10) + np.random.random(2**10) * 1j

        result_own = fft_pd10.fft(num_table.copy())
        result_np = np.fft.fft(num_table.copy())
        result_np[1:] = np.flip(result_np[1:])

        assert np.allclose(result_own, result_np), f'It[{i}]: Different results'


@pytest.fixture
def n_tries_base():
    return random.randint(5, 10), random.randint(2, 10)


def test_polynomial_multiplication(n_tries_base):
    N, base = n_tries_base

    for i in range(N):
        num1 = fft_pd10.rand_polynomial(base=base)
        num2 = fft_pd10.rand_polynomial(base=base)

        result_own = fft_pd10.mult_polynomials_fft(num1, num2)
        result_np_aux = np.flip(np.polymul(np.flip(num1), np.flip(num2)))

        result_np = np.zeros(len(result_own))
        result_np[:len(result_np_aux)] = result_np_aux

        assert np.allclose(result_own, result_np), f'It[{i}]: Different results'


def test_number_multiplication(n_tries_base):
    N, base = n_tries_base

    for i in range(N):
        num1 = fft_pd10.rand_number(2**10, base)
        num2 = fft_pd10.rand_number(2**10, base)

        result_own = fft_pd10.mult_numbers_fft(num1, num2)
        result_py = num1 * num2

        assert result_own == result_py, f'It[{i}]: Different results'


@pytest.mark.parametrize('c, l_coins, d_opt', 
    [[7, [1, 3, 4, 5], [{1:0, 3:1, 4:1, 5:0}]],
     [11, [1, 3, 5, 7], [{1: 1, 3: 1, 5: 0, 7: 1}, 
                        {1: 0, 3: 2, 5: 1, 7: 0},
                        {1: 1, 3: 0, 5: 2, 7: 0}]]])

def test_optimal_change(c, l_coins, d_opt):
    result = fft_pd10.optimal_change(c, l_coins)

    flag = False

    for sol in d_opt:
        if sol == result:
            flag = True

    assert flag, f'Incorrect result: {result}'


@pytest.mark.parametrize('mg, node_ini, dist', 
    [[np.array([[0, 2, np.inf, np.inf, 3], 
                [np.inf, 0, 2, np.inf, np.inf], 
                [np.inf, np.inf, 0, np.inf, np.inf], 
                [np.inf, np.inf, 3, 0, np.inf], 
                [np.inf, np.inf, np.inf, -3, 0]]), 0, {0: 0, 1: 2, 2: 3, 3: 0, 4: 3}]])

def test_bellman_ford(mg, node_ini, dist):
    result, _ = fft_pd10.bellman_ford(node_ini, mg)

    assert result == dist, f'Incorrect result: {result}'

@pytest.mark.parametrize('probs, opt_order', 
    [[[0.22, 0.18, 0.25, 0.35], [2, 0, 1, 3]],
     [[0.22, 0.18, 0.20, 0.05, 0.25, 0.02, 0.08], [2, 0, 1, 4, 3, 6, 5]]])

def test_optimal_bst(probs, opt_order):
    _, roots = fft_pd10.optimal_order(probs)
    result = fft_pd10.list_opt_ordering_search_tree(roots, 0, len(roots) - 1)

    assert result == opt_order, f'Incorrect result: {result}'



