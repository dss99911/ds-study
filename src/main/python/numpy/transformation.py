import numpy as np

x = np.linspace(0, 2, 100)

# %%

x_multiply_2 = x ** 2

# %%
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100