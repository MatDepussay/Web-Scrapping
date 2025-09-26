import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def inconue(x):
    return np.cos(10. * x)* np.exp(-x/2)



nb_points = 201
xl, xr = 0,2
esp = 0.1

XS = np.linspace(xl, xr, nb_points)
YS = inconue(XS) + esp * np.random.randn(nb_points)

plt.plot(XS, YS, 'b.')
