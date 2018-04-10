
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

def plot_surface(v,X):

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Make data.
        X = np.asarray(X)
        Y = X
        X, Y = np.meshgrid(X, Y)
        Z = -np.sqrt(X**2 + Y**2)/2
        print Z.shape

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(-3.01, 3.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()



def plot_surface_org(N):

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        # Make data.
        X = np.arange(-3, 4, 1)
        Y = np.arange(-3, 4, 1)
        X, Y = np.meshgrid(X, Y)
        Z = -np.sqrt(X**2 + Y**2)/2
        print Z.shape

        # Plot the surface.
        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                               linewidth=0, antialiased=False)

        # Customize the z axis.
        ax.set_zlim(-3.01, 3.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        # Add a color bar which maps values to colors.
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()



def plot_sample(x,y, numBinx, numBiny, step):
        fig = plt.figure(1)
        gs = gridspec.GridSpec(4,4)
        ax1 = fig.add_subplot(gs[:3, :3])
        ax1.scatter(x, y, color='blue')
        ax1.set_yticklabels([])
        ax1.set_xticklabels([])
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax2 = fig.add_subplot(gs[3,:3])
        ax2.hist(x, numBinx, facecolor='g')
        ax2.set_xticklabels([])
        ax2.yaxis.set_visible(False)
        ax2.set_xlabel('Histogram of X')
        ax3 = fig.add_subplot(gs[:3, 3])
        ax3.hist(y, numBiny, orientation='horizontal', facecolor='g')
        ax3.set_yticklabels([])
        ax3.xaxis.set_visible(False)
        ax3.set_ylabel('Histogram of Y')
        #"""
        ax4 = fig.add_subplot(gs[3, 3])
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        X, Y = np.meshgrid(xedges, yedges)
        #ax4.pcolormesh(X, Y, H)
        ax4.set_aspect('equal')
        ax4.xaxis.set_visible(False)
        ax4.yaxis.set_visible(False)
        #"""
        gs.update(wspace=0.5, hspace=0.5)
        H, xedges, yedges = np.histogram2d(y, x, bins=(numBinx, numBiny))
        print str(H)
        plt.show()
        #fig.show()

def plotCorrelation():
	#if(i == 0 or i == 1):
		#plot_sample(x,y,numBinx, 2, 1)
		#plot_sample(x,y,numBinx, 2, 1)
		#print sum(x) 
		#plt.figure(1)
		#plt.subplot(211)
		#plt.title(str(sum(x)))
		#plt.hist(x,numBinx)
		#plt.subplot(212)
		#plt.title(str(sum(y)))			
		#plt.hist(y,numBinx)
		#plt.show()
        return True



