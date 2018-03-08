__author__ = 'AlexLlamas'

from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from CorrelationMesures import *
from pandas import *


class Samples:

    def __init__(self, type_var=-1):
        self.type_var = type_var
        return

    def get(self, number_sam, noise):
        if self.type_var == 0:
            return self.get_sin(number_sam, noise)

        elif self.type_var == 1:
            return self.get_square(number_sam)

        elif self.type_var == 2:
            return self.get_blur(number_sam, noise)

        elif self.type_var == 3:
            return self.get_quadratic(number_sam, noise)

        elif self.type_var == 4:
            return self.get_diagonal_line(number_sam, noise)

        elif self.type_var == 5:
            return self.get_horizontal_line(number_sam, noise)

        elif self.type_var == 6:
            return self.get_vertical_line(number_sam, noise)

        elif self.type_var == 7:
            return self.get_x(number_sam, noise)

        elif self.type_var == 8:
            return self.get_circle(number_sam, noise)

        elif self.type_var == 9:
            return self.get_curve_x(number_sam, noise)

        elif self.type_var == 10:
            return self.get_diagonal_line2(number_sam, noise)

        elif self.type_var == 11:
            return self.get_dependent(number_sam)

        elif self.type_var == 12:
            return self.get_independent()

        elif self.type_var == 13:
            return self.get_corr(number_sam, noise)

        elif self.type_var == 14:
            return self.get_file()

        else:
            print 'Error'

    @staticmethod
    def scale(x_input):
        x_scale = (x_input - np.min(x_input))/(np.max(x_input)-np.min(x_input))
        return x_scale

    @staticmethod
    def get_file():
        data = read_csv('Data\X-Y-Independent.txt', header=None, skiprows=[0])
        z = np.zeros((data.shape[0], 2))
        # order X,W,Y,Z,T
        z[:, 0] = np.array(data.ix[:, 0])
        z[:, 1] = np.array(data.ix[:, 1])
        return z

    def get_sin(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples))
        y = np.random.normal(np.sin(x), noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_square(self, num_samples):
        x = np.random.uniform(-10, 10, num_samples)
        y = np.random.uniform(-10, 10, num_samples)
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_blur(self, num_samples, noise):
        mean = [0, 0]
        cov = [[noise, 0], [0, noise]]
        x, y = np.random.multivariate_normal(mean, cov, num_samples).T
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_quadratic(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples))
        y = np.random.normal(np.power(x, np.full(x.shape, 2)), noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_diagonal_line(self, num_samples, noise):
        x = np.array(np.linspace(-1, 1, num_samples))
        y = np.random.normal(x, noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_horizontal_line(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples))
        y = np.random.normal((x-x), noise)
        z = np.array(np.zeros((num_samples, 2)))  # type: Dict[Tuple[int, int]]
        z[:, 0] = x
        z[:, 1] = y
        z[0, 0], z[0, 1] = -10, -10
        z[1, 0], z[1, 1] = 10, 10
        z[:, 0] = self.scale(np.array(z[:, 0]))
        z[:, 1] = self.scale(np.array(z[:, 1]))
        return z

    def get_vertical_line(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples))
        y = np.random.normal((x-x), noise)
        z = np.array(np.zeros((num_samples, 2)))  # type: Dict[Tuple[int, int]]
        z[:, 0] = y
        z[:, 1] = x
        z[0, 0], z[0, 1] = -10, -10
        z[1, 0], z[1, 1] = 10, 10
        z[:, 0] = self.scale(np.array(z[:, 0]))
        z[:, 1] = self.scale(np.array(z[:, 1]))
        return z

    def get_x(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples/2))
        y1 = np.random.normal(x, noise)
        y2 = np.random.normal((np.full(x.shape, 1) - x), noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = np.concatenate((x, x), axis=0)
        z[:, 1] = np.concatenate((y1, y2), axis=0)
        z[:, 0] = self.scale(z[:, 0])
        z[:, 1] = self.scale(z[:, 1])
        return z

    def get_circle(self, num_samples, noise):
        x = np.array(np.linspace(-4, 4, num_samples/2))
        y1 = np.random.normal(np.sqrt(16-np.power(x, np.full(x.shape, 2))), noise)
        y2 = -np.random.normal(np.sqrt(16-np.power(x, np.full(x.shape, 2))), noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = np.concatenate((x, x), axis=0)
        z[:, 1] = np.concatenate((y1, y2), axis=0)
        z[:, 0] = self.scale(z[:, 0])
        z[:, 1] = self.scale(z[:, 1])
        return z

    def get_curve_x(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples/2))
        y1 = np.random.normal(np.power(x, np.full(x.shape, 2)), noise)
        y2 = -np.random.normal(np.power(x, np.full(x.shape, 2)), noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = np.concatenate((x, x), axis=0)
        z[:, 1] = np.concatenate((y1, y2), axis=0)
        z[:, 0] = self.scale(z[:, 0])
        z[:, 1] = self.scale(z[:, 1])
        return z

    def get_diagonal_line2(self, num_samples, noise):
        x = np.array(np.linspace(-10, 10, num_samples))
        y = np.random.normal((np.full(x.shape, 1)-x), noise)
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_dependent(self, num_samples):
        x = np.array(np.linspace(-10, 10, num_samples))
        y = np.array(np.linspace(-10, 10, num_samples))
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    def get_independent(self):
        z = np.zeros((10*10, 2))  # type: Dict[Tuple[int, int]]
        for i in range(0, 10):
            for j in range(0, 10):
                z[i*10 + j, 0] = i
                z[i*10 + j, 1] = j
        z[:, 0] = self.scale(np.array(z[:, 0]))
        z[:, 1] = self.scale(np.array(z[:, 1]))
        return z

    def get_corr(self, num_samples, p):
        u = np.random.uniform(-10, 10, num_samples)
        v_value = np.random.uniform(-10, 10, num_samples)
        x = u
        y = p*u + math.sqrt(1-math.pow(p, 2))*v_value
        z = np.zeros((num_samples, 2))
        z[:, 0] = self.scale(x)
        z[:, 1] = self.scale(y)
        return z

    @staticmethod
    def plot_partition(samples, num_bin_x, num_bin_y):
        """
        Plot the histogram of the samples structure
        :param samples:
        :param num_bin_x:
        :param num_bin_y:
        :return:
        """
        x, y = samples[:, 0], samples[:, 1]
        h, x_edges, y_edges = np.histogram2d(x, y, bins=(num_bin_x, num_bin_y))
        x_mesh, y_mesh = np.meshgrid(y_edges, x_edges)
        fig5 = plt.figure(5)
        # h = np.matrix(h)[0:num_bin_x, 0:num_bin_y]
        plt.pcolormesh(y_mesh, x_mesh, h)
        fig5.show()

    @staticmethod
    def plot_propose(samples, num_bin_x, step):
        """
        calculates de value of UMD, CMD, and MI for different grids ixi
        this calculations keeps the same significance for different grids
        use num_bin_x to define the max i in the for loop

        samples :type : numpy array
        num_bin_x :type : int
        step :type : int
        """
        x, y = samples[:, 0], samples[:, 1]
        umd_values = list()
        cmd_values = list()
        mi_values = list()
        for i in range(2, num_bin_x, step):
            umd_values.append(umd(x, y, i, i))
            cmd_values.append(cmd(x, y, i, i))
            mi_values.append(norm_mi(x, y, i, i))

        fig4 = plt.figure(4)
        plt.plot(range(2, num_bin_x, step), np.asarray(mi_values), 'b-')
        plt.plot(range(2, num_bin_x, step), np.asarray(umd_values), 'r-')
        plt.plot(range(2, num_bin_x, step), np.asarray(cmd_values), 'g-')

        plt.xlabel('Grid size ixi')
        plt.ylabel('Uniform Mutual Dependency(red)|Conditional Mutual Dependency(green)|Mutual information(blue)')
        plt.ylim(0, 1)
        fig4.show()

    def plot_compare2(self, max_bin_x, max_bin_y, noise, step, significance):
        """
        3d plot compare different types of grids while keeping the significance
        """
        sig = significance
        v_value = 10  # number of samples per block 5 for square
        sam_per_block = (v_value*sig)/math.sqrt(1-math.pow(sig, 2))

        size = max_bin_x*max_bin_y
        xp = np.zeros(size)  # type: list
        yp = np.zeros(size)  # type: list

        nmi = np.zeros(size)  # type: list
        md = np.zeros(size)  # type: list
        md2 = np.zeros(size)  # type: list

        max_md2 = 0.0
        max_md = 0.0
        for i in range(2, max_bin_x, step):
            for j in range(2, max_bin_y, step):
                num_samples = int(i*j*sam_per_block)
                samples = self.get(num_samples, noise)
                x, y = samples[:, 0], samples[:, 1]
                pos = i*max_bin_y + j

                xp[pos] = i
                yp[pos] = j

                nmi[pos] = norm_mi(x, y, i, j)
                md[pos] = umd(x, y, i, j)
                if md[pos] > max_md:
                    max_md = md[i*max_bin_y + j]
                md2[pos] = cmd(x, y, i, j)
                if md2[pos] > max_md2:
                    max_md2 = md[pos]

        print 'Maximal Mutual dependency: ' + str(max_md)
        print 'Maximal Mutual dependency: ' + str(max_md)

        fig2 = plt.figure(2)
        axi1 = fig2.gca(projection='3d')
        axi1.plot_trisurf(xp, yp, md, cmap=cm.jet, linewidth=0.2)
        plt.title('Uniform Mutual Dependency (UMD)')
        plt.xlabel('Number of bins in X')
        plt.ylabel('Number of bins in Y')
        fig2.show()

        fig6 = plt.figure(6)
        axi2 = fig6.gca(projection='3d')
        axi2.plot_trisurf(xp, yp, md2, cmap=cm.jet, linewidth=0.2)
        plt.title('Comparative Mutual Dependency (CMD)')
        fig6.show()

        fig3 = plt.figure(3)
        axi2 = fig3.gca(projection='3d')
        axi2.plot_trisurf(xp, yp, nmi, cmap=cm.jet, linewidth=0.2)
        plt.title('Mutual Information (MI)')
        fig3.show()

    @staticmethod
    def plot_sample(samples, num_bin_x, num_bin_y):
        x, y = samples[:, 0], samples[:, 1]

        fig = plt.figure(1)
        gs = gridspec.GridSpec(4,4)
        ax1 = fig.add_subplot(gs[:3, :3])
        ax1.scatter(x, y, color='blue')
        ax1.set_xlabel('X axis')
        ax1.set_ylabel('Y axis')
        ax2 = fig.add_subplot(gs[3,:3])
        ax2.hist(x, bins=np.linspace(np.amin(x), np.amax(x), num_bin_x), facecolor='g')
        ax2.set_xticklabels([])
        ax2.yaxis.set_visible(False)
        ax2.set_xlabel('Histogram of X')
        ax3 = fig.add_subplot(gs[:3, 3])
        ax3.hist(y, num_bin_y, orientation='horizontal', facecolor='g')
        ax3.set_yticklabels([])
        ax3.xaxis.set_visible(False)
        ax3.set_ylabel('Histogram of Y')
        gs.update(wspace=0.5, hspace=0.5)
        fig.show()
        np.histogram2d(y, x, bins=(num_bin_x, num_bin_y))
