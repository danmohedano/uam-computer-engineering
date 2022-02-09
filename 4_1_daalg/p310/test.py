from fft_pd10 import *
import numpy as np

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
l_coins = [1,3,4,5]
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