import scipy.optimize as optimize


# Define the mathematical function whose root we want to find
def f(x):
    return x**3 - x**2 + 2

# 값의 lower bound, upper bound 가 있을 때, 가장 빠르다고 함. safety, fast
root = optimize.brentq(f, -10, 10)

# Print the result
print(f"The root is {root}")

#%%
import scipy.optimize as optimize

# Define the mathematical function whose root we want to find
def f(x):
    return x**3 - x**2 + 2

# Define the derivative of the function (required by the newton method)
def f_prime(x):
    return 3*x**2 - 2*x


# unsafe, very fast, relatively exact if we provide f’ , f’’
root = optimize.newton(f, x0=-0.1, fprime=f_prime)

# Print the result
print(f"The root is {root}")
