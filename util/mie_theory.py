#/usr/bin/python


# PACKAGES AND SETTINGS

import numpy as np
pi = np.pi

from scipy.interpolate import interp1d
from matplotlib.ticker import FuncFormatter


# FUNCTION DEFINITIONS

from scipy.special import jv, yv, lpmv
from scipy.misc import derivative

def j(x, n): 
    return np.sqrt(pi/(2*x))*jv(n+1/2, x)
    
def y(x, n):
    return np.sqrt(pi/(2*x))*yv(n+1/2, x)

def h1(x, n): 
    return j(x, n) + 1j*y(x, n)

def psi(x, n):
    return x*j(x, n)

def xi(x, n):
    return x*h1(x, n)

def d_psi(x, n):
    #return derivative(psi, x, dx=1e-6, args=(n, ))
    return (1 + n)*j(x, n) - x*j(x, n + 1)

def d_xi(x, n):
    #return derivative(xi, x, dx=1e-6, args=(n, ))
    return (1 + n)*h1(x, n) - x*h1(x, n + 1)

def a(x, n, m):
    return (m*psi(m*x, n)*d_psi(x, n) - psi(x, n)*d_psi(m*x, n))/(m*psi(m*x, n)*d_xi(x, n) - xi(x, n)*d_psi(m*x, n))

def b(x, n, m):
    return (psi(m*x, n)*d_psi(x, n) - m*psi(x, n)*d_psi(m*x, n))/(psi(m*x, n)*d_xi(x, n) - m*xi(x, n)*d_psi(m*x, n))

def x(lda, r, n1):
    return 2*pi*r*n1/lda

def m(lda, n1, n2):
    return n2(lda)/n1
    
def sigma_sca(lda, r, n1, n2, N):
    return np.array([(2*pi*r**2)/x(lda, r, n1)**2*(2*n + 1)*(np.abs(a(x(lda, r, n1), n, m(lda, n1, n2)))**2 + np.abs(b(x(lda, r, n1), n, m(lda, n1, n2)))**2) for n in range(1, N+1)]).sum(axis=0)

def sigma_ext(lda, r, n1, n2, N):
    return np.array([(2*pi*r**2)/x(lda, r, n1)**2*(2*n + 1)*(np.real(a(x(lda, r, n1), n, m(lda, n1, n2)) + b(x(lda, r, n1), n, m(lda, n1, n2)))) for n in range(1, N+1)]).sum(axis=0)

def sigma_abs(lda, r, n1, n2, N):
    return sigma_ext(lda, r, n1, n2, N) - sigma_sca(lda, r, n1, n2, N)

def g(lda, r, n1, n2, N):
    return (4*pi*r**2)/(x(lda, r, n1)**2*sigma_sca(lda, r, n1, n2, N))*np.array([n*(n+2)/(n+1)*np.real(a(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(a(x(lda,r, n1), n+1, m(lda, n1, n2))) + b(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(b(x(lda, r, n1), n+1, m(lda, n1, n2)))) + (2*n+1)/(n*(n+1))*np.real(a(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(b(x(lda, r, n1), n, m(lda, n1, n2)))) for n in range(1, N+1)]).sum(axis=0)

def sigma_pr(lda, r, n1, n2, N):
    return (2*pi*r**2)/x(lda, r, n1)**2*np.array([(2*n+1)/(n*(n+1))*np.real(a(x(lda, r, n1), n, m(lda, n1, n2)) + np.conj(b(x(lda, r, n1), n, m(lda, n1, n2))) - 2*a(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(b(x(lda, r, n1), n, m(lda, n1, n2)))) + n*(n+2)/(n+1)*np.real(a(x(lda, r, n1), n, m(lda, n1, n2)) + b(x(lda, r, n1), n, m(lda, n1, n2)) + np.conj(a(x(lda, r, n1), n+1, m(lda, n1, n2))) + np.conj(b(x(lda, r, n1), n+1, m(lda, n1, n2))) - 2*a(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(a(x(lda, r, n1), n+1, m(lda, n1, n2))) - 2*b(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(b(x(lda, r, n1), n+1, m(lda, n1, n2)))) for n in range(1, N+1)]).sum(axis=0)

def sigma_pr_(lda, r, n1, n2, N):
    return sigma_ext(lda, r, n1, n2, N) - (4*pi*r**2)/x(lda, r, n1)**2*np.array([n*(n+2)/(n+1)*np.real(a(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(a(x(lda,r, n1), n+1, m(lda, n1, n2))) + b(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(b(x(lda, r, n1), n+1, m(lda, n1, n2)))) + (2*n+1)/(n*(n+1))*np.real(a(x(lda, r, n1), n, m(lda, n1, n2))*np.conj(b(x(lda, r, n1), n, m(lda, n1, n2)))) for n in range(1, N+1)]).sum(axis=0)

def P_mn(x, m, n):
    return lpmv(m, n, np.cos(x))

def pi_mn(x, m, n):
    return P_mn(x, m, n)/np.sin(x)

def tau_mn(x, m, n):
    #return derivative(P_mn, x, dx=1e-6, args=(m, n, ))
    return -(1 + n)*1/np.tan(x)*P_mn(x, m, n) + (1 - m + n)*1/np.sin(x)*P_mn(x, m, n + 1)

def S1(theta, lda, r, n1, n2, N):
    return np.array([(2*n+1)/(n*(n+1))*(a(x(lda, r, n1), n, m(lda, n1, n2))*pi_mn(theta, 1, n) + b(x(lda, r, n1), n, m(lda, n1, n2))*tau_mn(theta, 1, n)) for n in range(1, N+1)]).sum(axis=0)

def S2(theta, lda, r, n1, n2, N):
    return np.array([(2*n+1)/(n*(n+1))*(a(x(lda, r, n1), n, m(lda, n1, n2))*tau_mn(theta, 1, n) + b(x(lda, r, n1), n, m(lda, n1, n2))*pi_mn(theta, 1, n)) for n in range(1, N+1)]).sum(axis=0)


def THEORY_CURVE( LDA, d=100e-6, n1=1.33 ):
    # DIELECTRIC FUNCTION OF SPHERE MATERIAL

    lda, n, k = np.transpose(np.loadtxt('data/refractive-indices/Au_nk.txt', skiprows=1)) # load experimental data for refractive index and extinction coefficient vs wavelength
    n2 = interp1d(lda*1e-6, n + 1j*k, kind=2) # interpolate data

    #lda = np.linspace(400, 800, 100)*1e-9
    return sigma_sca( LDA, 0.5*d, n1, n2, 100 )*1e12 #µm²
    
    




