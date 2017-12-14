__author__ = 'AlexLlamas'
import numpy as np
import math
# from minepy import MINE


# -------------------------------------- Mutual information -----------------------------------------------------------
def mutual_info(x, y, numBinx, numBiny):
    N = x.size
    H, xedges, yedges = np.histogram2d(x, y ,bins=[numBinx, numBiny])
    H = np.array(H)
    sumx = np.sum(H, axis=0)
    sumy = np.sum(H, axis=1)
    MI = 0.0
    for i in range(0,numBinx):
        for j in range(0, numBiny):
            if H[i,j] != 0:
                MI += (H[i,j]/float(N)) * \
                      math.log10((H[i,j]/float(N))/((sumy[i]/float(N))*(sumx[j]/float(N))))
    return MI
# ---------------------------------------------------------------------------------------------------------------------


# --------------------------------------------- Entropy -------------------------------------------------------------
def entropy(x, numBinx):
    N = x.size
    H, edges = np.histogram(x, numBinx)
    e = 0.0
    for i in range(0,numBinx):
        if H[i] != 0:
            e -= (H[i]/float(N))*math.log10(H[i]/float(N))
    return e
# ---------------------------------------------------------------------------------------------------------------------


# --------------------------------------- Normalized mutual information -----------------------------------------------
def norm_MI(x, y, numBinx, numBiny):
    MI = mutual_info(x, y, numBinx, numBiny)
    ex = entropy(x, numBinx)
    ey = entropy(y, numBiny)
    R = MI/float(ex+ey)
    Rmax = min(ex, ey)/float(ex+ey)
    return R / Rmax
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------- Pearson correlation --------------------------------------------------
def pearson_corr(x, y):
    N = x.size
    xm = np.mean(x)
    ym = np.mean(y)
    numerator = 0.0
    for i in range(0, N):
        numerator += (x[i] - xm)*(y[i]-ym)
    sx = 0.0
    for i in range(0, N):
        sx += math.pow((x[i]-xm), 2)
    sy = 0.0
    for i in range(0,N):
        sy += math.pow((y[i]-ym), 2)
    rxy = numerator / math.sqrt(sx*sy)
    return rxy
# ---------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------ Entropy X|Y --------------------------------------------------------
def entropyx_y(x, y, numBinx, numBiny):
    N = x.size
    H, xedges, yedges = np.histogram2d(x, y ,bins=[numBinx, numBiny])
    H = np.array(H)
    sumx = np.sum(H, axis=0)
    exy = 0.0
    for i in range(0,numBinx):
        for j in range(0, numBiny):
            if H[i,j] != 0:
                exy += (H[i,j]/float(N))*math.log10((sumx[j]/float(N))/(H[i,j]/float(N)))
    return exy
# ---------------------------------------------------------------------------------------------------------------------


# -------------------------------- Mutual information based on Entropy ------------------------------------------------
def MI_Entropy(x, y, numBinx, numBiny):
    MIE = entropy(x, numBinx) - entropyx_y(x, y, numBinx, numBiny)
    return MIE
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------- Propose dependency of Y over X ---------------------------------------------------
def propuesta_Ixy(x, y, numBinx, numBiny):
    H, xedges, yedges = np.histogram2d(x, y ,bins=[numBinx, numBiny])
    H = np.array(H)
    sumx = np.sum(H, axis=0)
    norm = float(numBinx)/((numBinx-1)*2*numBiny)
    Ixy = 0.0
    for i in range(0,numBinx):
        for j in range(0, numBiny):
            if sumx[j] != 0:
                Ixy += math.fabs((1/float(numBinx))-(H[i,j]/float(sumx[j])))
    return norm*Ixy
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------- Propose dependency of X over Y ---------------------------------------------------
def propuesta_Iyx(x, y, numBinx, numBiny):
    H, xedges, yedges = np.histogram2d(x, y ,bins=[numBinx, numBiny])
    H = np.array(H)
    sumy = np.sum(H, axis=1)
    norm = float(numBiny)/((numBiny-1)*2*numBinx)
    Iyx = 0.0
    for i in range(0,numBinx):
        for j in range(0, numBiny):
            if sumy[i] != 0:
                Iyx += math.fabs((1/float(numBiny))-(H[i,j]/float(sumy[i])))
    return norm*Iyx
# ---------------------------------------------------------------------------------------------------------------------




# ------------------------------------------ Distance Covariance -----------------------------------------------------
def d_cov(x,y):
    N = x.size

    a_kp = np.zeros(N)
    for k in range(0,N):
        for l in range(0,N):
            a_kp[k] = a_kp[k] + math.fabs(x[k]-x[l])
        a_kp[k] = (1/float(N))*a_kp[k]

    a_pl = np.zeros(N)
    for l in range(0,N):
        for k in range(0,N):
            a_pl[l]= a_pl[l] + math.fabs(x[k]-x[l])
        a_pl[l]=a_pl[l]*(1/float(N))

    a_pp = 0.0
    for k in range(0,N):
        for l in range(0,N):
            a_pp += math.fabs(x[k]- x[l])
    a_pp = a_pp * (1/math.pow(N,2))

    A = np.zeros((N,N))
    for k in range(0,N):
        for l in range(0,N):
            A[k, l] = math.fabs(x[k]-x[l]) - a_kp[k] - a_pl[l] + a_pp

    # ------------------------------- now with b

    b_kp = np.zeros(N)
    for k in range(0,N):
        for l in range(0,N):
            b_kp[k] = b_kp[k] + math.fabs(y[k]-y[l])
        b_kp[k] = (1/float(N))*b_kp[k]

    b_pl = np.zeros(N)
    for l in range(0,N):
        for k in range(0,N):
            b_pl[l]= b_pl[l] + math.fabs(y[k]-y[l])
        b_pl[l]=b_pl[l]*(1/float(N))

    b_pp = 0.0
    for k in range(0,N):
        for l in range(0,N):
            b_pp += math.fabs(y[k]- y[l])
    b_pp = b_pp * (1/math.pow(N,2))

    B = np.zeros((N,N))
    for k in range(0,N):
        for l in range(0,N):
            B[k, l] = math.fabs(y[k]-y[l]) - b_kp[k] - b_pl[l] + b_pp

    # Distance
    V_xy = 0.0
    for k in range(0,N):
        for l in range(0,N):
            V_xy += A[k,l]*B[k,l]
    V_xy = V_xy*(1/math.pow(N,2))

    return V_xy
# ---------------------------------------------------------------------------------------------------------------------


# ----------------------------------------- Distance correlation ------------------------------------------------------
def d_corr(x,y):
    var_x = d_cov(x,x)
    var_y = d_cov(y,y)
    cond = var_x * var_y
    R_xy = 0.0
    if cond != 0:
        R_xy = d_cov(x,y)/math.sqrt(cond)
    return R_xy
# ---------------------------------------------------------------------------------------------------------------------

"""
# ----------------------------------------------------- MIC -----------------------------------------------------------
def MIC(x, y):
    mine = MINE(alpha =0.6, c=15)
    mine.compute_score(x, y)
    return mine.mic()
# ---------------------------------------------------------------------------------------------------------------------
"""

# ---------------------------- Propose 2 distance between p(X) and P(X|Y) ---------------------------------------------
def propuesta2_Ixy(x, y, numBinx, numBiny):
    N = x.size
    H, xedges, yedges = np.histogram2d(x, y ,bins=[numBinx, numBiny])
    H = np.array(H)
    sumx = np.sum(H, axis=0)
    sumy = np.sum(H, axis=1)
    norm = float(numBinx)/((numBinx-1)*2*numBiny)
    Ixy = 0.0
    for i in range(0,numBinx):
        for j in range(0, numBiny):
            if sumx[j] != 0:
                Ixy += math.fabs((sumy[i]/float(N))-(H[i,j]/float(sumx[j])))
    return norm*Ixy
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------- Propose 2 distance between p(Y) and P(Y|X) ---------------------------------------------
def propuesta2_Iyx(x, y, numBinx, numBiny):
    N = x.size
    H, xedges, yedges = np.histogram2d(x, y ,bins=[numBinx, numBiny])
    H = np.array(H)
    sumx = np.sum(H, axis=0)
    sumy = np.sum(H, axis=1)
    norm = float(numBiny)/((numBiny-1)*2*numBinx)
    Iyx = 0.0
    for i in range(0,numBinx):
        for j in range(0, numBiny):
            if sumy[i] != 0:
                Iyx += math.fabs((sumx[j]/float(N))-(H[i,j]/float(sumy[i])))
    return norm*Iyx
# ---------------------------------------------------------------------------------------------------------------------

# --------------------------------------- Propose mutual dependency ---------------------------------------------------
def propuesta_mutual_dependency(x, y, numBinx, numBiny):
    Ixy = propuesta_Ixy(x, y, numBinx, numBiny)
    Iyx = propuesta_Iyx(x, y, numBinx, numBiny)
    #return Ixy
    return Iyx
    #return max(Ixy, Iyx)
    #return (Ixy + Iyx)/2
# ---------------------------------------------------------------------------------------------------------------------

# ----------------------------------------- Propose mutual distance ---------------------------------------------------
def propuesta2_mutual_dependency(x, y, numBinx, numBiny):
    Ixy = propuesta2_Ixy(x, y, numBinx, numBiny)
    Iyx = propuesta2_Iyx(x, y, numBinx, numBiny)
    return Iyx
    #return max(Ixy,Iyx)
    #return (Ixy + Iyx)/2
# ---------------------------------------------------------------------------------------------------------------------


