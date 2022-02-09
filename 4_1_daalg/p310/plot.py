import fft_pd10
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def test_function(n_iterations, ini, fin, step, test_fn, fft_implementation=None):
    print('Testing ' + str(test_fn))
    if not fft_implementation:
        return np.array(test_fn(n_iterations, ini, fin, step))
    else:
        return np.array(test_fn(n_iterations, ini, fin, step, fft_func=fft_implementation))


def fit_times(ini, fin, step, data, expression):
    x = np.array([i for i in range(ini, fin + 1, step)])
    x = x.reshape(-1, 1)

    lr_m = LinearRegression()
    lr_m.fit(expression(x), data)
    return lr_m.predict(expression(x)), x

ITERS = 10
INI = 10
FIN = 1000
STEP = 5

times_fft = test_function(ITERS, INI, FIN, STEP, fft_pd10.time_fft, fft_pd10.fft)
times_fft_np = test_function(ITERS, INI, FIN, STEP, fft_pd10.time_fft, np.fft.fft)
predicted_fft, x = fit_times(INI, FIN, STEP, times_fft, lambda x: (2**np.ceil(np.log2(x)))*np.log2(2**np.ceil(np.log2(x))))

plt.title("Timing of FFT")
plt.xlabel("Polynomial Size (N)")
plt.ylabel("t (ms)")
plt.grid(True)
plt.plot(x, times_fft, '.r', x, predicted_fft, '--b')
plt.legend(['Real times', 'Fitted times'])
plt.show()