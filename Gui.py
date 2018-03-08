__author__ = 'AlexLlamas'
from Tkinter import *
from samples import Samples
from CorrelationMesures import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def set_scrollbar(listbox, scrollbar):
    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=Y)


def set_list_box(in_list, listbox):
    ind, largo = (0, len(in_list))
    while ind < largo:
        listbox.insert(END, in_list[ind])
        ind += 1


def case_function(samples, obj):
    sam = Samples()  # object required to plot
    num_bin_x, num_bin_y = (Bin_x.get(), Bin_y.get())
    mi_text.set('Calculating...')
    not_selected = True
    if plot_sample.get():
        sam.plot_sample(samples, num_bin_x, num_bin_y)
        not_selected = False
    if plot_compare.get():
        obj.plot_compare2(num_bin_x, num_bin_y, noise.get(), step.get(), significance.get())
        not_selected = False
    if plot_proposal.get():
        sam.plot_propose(samples, num_bin_x, step.get())
        not_selected = False
    if plot_partition.get():
        sam.plot_partition(samples, num_bin_x, num_bin_y)
        not_selected = False
    if plot_converge_in_samples.get():
        converge_in_samples(num_bin_x, num_bin_y, obj)
        not_selected = False
    if samples_check.get():
        samples_grid(num_bin_x, num_bin_y)
        not_selected = False
    if bin_selection.get():
        bin_selection_validation(sigma=significance.get(), obj=obj)
        not_selected = False
    if cal_measures.get():
        calculate_measures(samples, num_bin_x, num_bin_y)
        not_selected = False
    if not_selected:
        mi_text.set('Select a plot or calculation')


def calculate_measures(samples, num_bin_x, num_bin_y):
    x, y = samples[:, 0], samples[:, 1]
    mi = mutual_info(x, y, num_bin_x, num_bin_y)
    ex = entropy(x, num_bin_x)
    ey = entropy(y, num_bin_y)
    r = norm_mi(x, y, num_bin_x, num_bin_y)
    rxy = pearson_corr(x, y)
    exy = entropy_x_y(x, y, num_bin_x, num_bin_y)
    eyx = entropy_x_y(y, x, num_bin_x, num_bin_y)
    mie = mi_entropy(x, y, num_bin_x, num_bin_y)
    ixy_ud = ud_ixy(x, y, num_bin_x, num_bin_y)
    iyx_ud = ud_ixy(y, x, num_bin_x, num_bin_y)
    ixy_cd = cd_ixy(x, y, num_bin_x, num_bin_y)
    iyx_cd = cd_ixy(y, x, num_bin_x, num_bin_y)
    umd_measure = umd(x, y, num_bin_x, num_bin_y)
    cmd_measure = cmd(x, y, num_bin_x, num_bin_y)
    # d_cor = d_corr(x,y)  # to slow
    # Mic = MIC(x,y)  # too slow

    mi_text.set('Entropy of x: ' + str(ex) + '\n' +
                'Entropy of y: ' + str(ey) + '\n' +
                'Mutual information: ' + str(mi) + '\n' +
                'Mutual info with entropy: ' + str(mie) + '\n' + '\n' +

                '(Max=1)Normalized Mutual info: ' + str(r) + '\n' +
                '(Max=1)Pearson Correlation: ' + str(rxy) + '\n' +
                # '(Max=1)Distance Correlation: ' + str(d_cor) + '\n' +
                # '(Max=1)MIC: ' + str(Mic) + '\n' +
                '(Max=1)Uniform Mutual Dependency (UMD): ' + str(umd_measure) + '\n' +
                '(Max=1)Comparative Mutual Dependency (CMD): ' + str(cmd_measure) + '\n' + '\n' +

                'Entropy of X|Y = ' + str(exy) + '\n' +
                'Entropy of Y|X = ' + str(eyx) + '\n' +
                '(Max=1)UD-Information in Y of X: ' + str(ixy_ud) + '\n' +
                '(Max=1)UD-Information in X of Y: ' + str(iyx_ud) + '\n' +
                '(Max=1)CD-Information2 in Y of X: ' + str(ixy_cd) + '\n' +
                '(Max=1)CD-Information2 in X of Y: ' + str(iyx_cd))


def func(x, a, b, c, d):
    return (a/(b*x+c))+d


def inverse_func(y, a, b, c, d):
    return (a/float(b*(y-d))) - (c/float(b))


def samples_grid(num_bin_x, num_bin_y):
        sig = significance.get()  # significance
        v = 10  # number of samples per block 5 for square see paper for more information
        sam_per_block = (v*sig)/math.sqrt(1-math.pow(sig, 2))
        num_samples = int(num_bin_x*num_bin_y*sam_per_block)
        mi_text.set('The number of samples needed for a significance of '
                    + str(sig) + '\nwith v= ' + str(v) + ' ,Bin_x= ' + str(num_bin_x)
                    + ' ,Bin_y= ' + str(num_bin_y) + ' ,is...: ' + str(num_samples))

        print 'The number of samples needed for a significance of ' \
              + str(sig) + 'with v = ' + str(v) + 'Bin_x = ' + str(num_bin_x) \
              + 'Bin_y= ' + str(num_bin_y) + 'is...: ' + str(num_samples)


def bin_selection_validation(sigma, obj):
    step_i = step.get()
    ini = step_i  # initial number of samples
    end = number_sam.get()
    size = ((end - ini)/step_i)
    umd_value = np.zeros(size)  # type: list
    cmd_value = np.zeros(size)  # type: list
    r = np.zeros(size)  # type: list
    axis = np.zeros(size)  # type: list
    k = 0
    for n in range(ini, end, step_i):
        samples = obj.get(n, noise.get())
        x, y = samples[:, 0], samples[:, 1]
        # we are assuming that the data are scaled to be in the range [0,1] that is why is 1 minus
        num_bin_x = int(math.floor(1 / float(math.sqrt((2*sigma)/(n*math.sqrt(1-sigma))))))
        num_bin_y = num_bin_x  # this is because the data is scaled
        # print 'The number of bins for ' + str(n) + ' samples is: ' + str(numBinx)

        umd_value[k] = umd(x, y, num_bin_x, num_bin_y)
        cmd_value[k] = cmd(x, y, num_bin_x, num_bin_y)
        r[k] = norm_mi(x, y, num_bin_x, num_bin_y)
        axis[k] = n
        k += 1
    fig7 = plt.figure(7)
    plt.plot(axis, umd_value, 'r-')
    plt.plot(axis, cmd_value, 'g-')
    plt.plot(axis, r, 'b-')

    plt.xlabel('Number of samples')
    plt.ylabel('UMD (red) | CMD) (green) | MI (blue)')
    plt.ylim((0, 1))
    fig7.show()


def converge_in_samples(num_bin_x, num_bin_y, obj):

    # this function plot the measures with different number of samples
    # the objective of this function is find converge in the measures
    # this is, adding more samples does not change or change very little the measure.

    converge_value_umd = 0.631995917246
    converge_value_cmd = 0.346874335815
    converge_value_r = 0.0607182686559

    ini = step.get()  # initial number of samples
    end = number_sam.get()
    step_i = ini
    size = ((end - ini)/step_i)
    umd_values = np.zeros(size)  # type: list
    cmd_values = np.zeros(size)  # type: list
    r = np.zeros(size)  # type: list
    axis = np.zeros(size)  # type: list
    k = 0

    for i in range(ini, end, step_i):
        samples = obj.get(i, noise.get())
        x, y = samples[:, 0], samples[:, 1]
        umd_values[k] = umd(x, y, num_bin_x, num_bin_y)
        cmd_values[k] = cmd(x, y, num_bin_x, num_bin_y)
        r[k] = norm_mi(x, y, num_bin_x, num_bin_y)
        axis[k] = i
        k += 1

    fig6 = plt.figure(6)
    plt.plot(axis, umd_values, 'r-')
    plt.plot(axis, cmd_values, 'g-')
    plt.plot(axis, r, 'b-')

    p_opt_umd, p_cov = curve_fit(func, axis, umd_values)
    p_opt_cmd, p_cov = curve_fit(func, axis, cmd_values)
    p_opt_r, p_cov = curve_fit(func, axis, r)

    plt.plot(axis, func(axis, *p_opt_umd), 'r-')
    plt.plot(axis, func(axis, *p_opt_cmd), 'g-')
    plt.plot(axis, func(axis, *p_opt_r), 'b-')

    plt.xlabel('Number of samples')
    plt.ylabel('UMD (red) | CMD (green) | MI (blue)')
    plt.ylim((0, 1))
    fig6.show()

    # --- fin converge values --------------------
    a = p_opt_umd[0]
    b = p_opt_umd[1]
    c = p_opt_umd[2]
    # variation between samples i.e. (X_2 = X_1 + e) longer time to converge for higher e values.
    e = 1
    # the function converge when f(X_2)- f(X_1) = eps. longer time to converge for lower eps values.
    eps = 0.00001

    umd_x = ((-(((pow(b, 2))*e)+(2*b*c)) + pow(((((pow(b, 2))*e)+(2*b*c)) -
                                                ((4*(pow(b, 2)))*((b*c*e) + pow(c, 2) - (a*b*e/eps)))), 0.5)) /
             float(2*pow(b, 2)))

    a = p_opt_cmd[0]
    b = p_opt_cmd[1]
    c = p_opt_cmd[2]

    cmd_x = ((-(((pow(b, 2))*e)+(2*b*c)) + pow(((((pow(b, 2))*e)+(2*b*c)) -
                                                ((4*(pow(b, 2)))*((b*c*e) + pow(c, 2) - (a*b*e/eps)))), 0.5)) /
             float(2*pow(b, 2)))

    a = p_opt_r[0]
    b = p_opt_r[1]
    c = p_opt_r[2]

    r_x = ((-(((pow(b, 2))*e)+(2*b*c)) + pow(((((pow(b, 2))*e)+(2*b*c)) -
                                              ((4*(pow(b, 2)))*((b*c*e) + pow(c, 2) - (a*b*e/eps)))), 0.5)) /
           float(2*pow(b, 2)))
    # ------------------------------------------------------------------------------------------------------------------

    print '----------------------------------------------------------------------'
    print 'Number of samples to converge in UMD (red): ' + str(umd_x)
    print 'value of converge for UMD: ' + str(func(umd_x, *p_opt_umd))

    print 'Number of samples to converge in CMD (green): ' + str(cmd_x)
    print 'value of converge for CMD: ' + str(func(cmd_x, *p_opt_cmd))

    print 'Number of samples to converge in MI (blue): ' + str(r_x)
    print 'value of converge for MI: ' + str(func(umd_x, *p_opt_r))

    print '----------------------------------------------------------------------'

    print 'Number of samples to get a converge value of ' + str(converge_value_umd) + ' in UMD is: ' + \
          str(inverse_func(converge_value_umd, *p_opt_umd)) + 'ASB, ' + str(num_bin_x) + 'x' + str(num_bin_y) + ': ' + \
          str(inverse_func(converge_value_umd, *p_opt_umd)/float(num_bin_x*num_bin_y))

    print 'Number of samples to get a converge value of ' + str(converge_value_cmd) + ' in CMD is: ' + \
          str(inverse_func(converge_value_cmd, *p_opt_cmd)) + 'ASB, ' + str(num_bin_x) + 'x' + str(num_bin_y) + ': ' + \
          str(inverse_func(converge_value_cmd, *p_opt_cmd)/float(num_bin_x*num_bin_y))

    print 'Number of samples to get a converge value of ' + str(converge_value_r) + ' in MI is: ' + \
          str(inverse_func(converge_value_r, *p_opt_r)) + 'ASB, ' + str(num_bin_x) + 'x' + str(num_bin_y) + ': ' + \
          str(inverse_func(converge_value_r, *p_opt_r)/float(num_bin_x*num_bin_y))


def plot_select():
    ind = list1.curselection()
    if list1.curselection() != ():

        if ind[0] == 0:
            sam = Samples(type_var=0)
            samples = sam.get_sin(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 1:
            sam = Samples(type_var=1)
            samples = sam.get_square(number_sam.get())
            case_function(samples, sam)
        elif ind[0] == 2:
            sam = Samples(type_var=2)
            samples = sam.get_blur(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 3:
            sam = Samples(type_var=3)
            samples = sam.get_quadratic(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 4:
            sam = Samples(type_var=4)
            samples = sam.get_diagonal_line(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 5:
            sam = Samples(type_var=5)
            samples = sam.get_horizontal_line(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 6:
            sam = Samples(type_var=6)
            samples = sam.get_vertical_line(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 7:
            sam = Samples(type_var=7)
            samples = sam.get_x(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 8:
            sam = Samples(type_var=8)
            samples = sam.get_circle(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 9:
            sam = Samples(type_var=9)
            samples = sam.get_curve_x(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 10:
            sam = Samples(type_var=10)
            samples = sam.get_diagonal_line2(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 11:
            sam = Samples(type_var=11)
            samples = sam.get_dependent(number_sam.get())
            case_function(samples, sam)
        elif ind[0] == 12:
            sam = Samples(type_var=12)
            samples = sam.get_independent()
            case_function(samples, sam)
        elif ind[0] == 13:
            sam = Samples(type_var=13)
            samples = sam.get_corr(number_sam.get(), noise.get())
            case_function(samples, sam)
        elif ind[0] == 14:
            sam = Samples(type_var=14)
            samples = sam.get_file()
            case_function(samples, sam)
        else:
            mi_text.set('Error')
    else:
        mi_text.set('Select a type')


def frame6_help():
    mi_text.set('Plot sample structure \n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: used to select the size of the sample \n '
                'Num_bins X: used to set the bins in the histogram for X \n'
                'Num_bins Y: used to set the bins in the histogram for Y \n'
                'Step: is not used \n'
                'Significance: is not used.')


def frame7_help():
    mi_text.set('Plot Comparative \n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: is not used, the samples are calculated to maintain the significance\n '
                'Num_bins X: used to set the max number of bins in X for the analysis\n'
                'Num_bins Y: used to set the max number of bins in Y for the analysis \n'
                'Step: sets the number of bins to move from \n'
                'Significance: sets the significance for all calculations.')


def frame8_help():
    mi_text.set('Plot measures for grids ixi \n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: sets the size of the sample, all calculations will have the same \n '
                'Num_bins X: sets the max number of bins in X and Y for the analysis \n'
                'Num_bins Y: is not used \n'
                'Step: sets the number of bins to move from  \n'
                'Significance: is not used.')


def frame9_help():
    mi_text.set('Plot histogram of the structure \n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: used to select the size of the sample \n '
                'Num_bins X: used to set the bins in the histogram for X \n'
                'Num_bins Y: used to set the bins in the histogram for Y \n'
                'Step: is not used \n'
                'Significance: is not used.')


def frame10_help():
    mi_text.set('Plot Converge in samples \n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: sets the max number of samples \n '
                'Num_bins X: sets the bins in X, the same for all calculations \n'
                'Num_bins Y: sets the bins in Y, the same for all calculations \n'
                'Step: set the beginning and the step until the max number of samples \n'
                'Significance: is not used.')


def frame11_help():
    mi_text.set('Calculate samples for the grid \n '
                'Noise: is not used \n '
                'Number of samples: is not used \n '
                'Num_bins X: sets the bins in X \n'
                'Num_bins Y: sets the bins in Y \n'
                'Step: is not used \n'
                'Significance: set the significance to calculate the number of samples needed for the selected bins.')


def frame12_help():
    mi_text.set('Plot bin selection validation\n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: sets the max number of samples  \n '
                'Num_bins X: is not used \n'
                'Num_bins Y: is not used \n'
                'Step: set the beginning and the step until the max number of samples \n'
                'Significance: used to have the same significance for all calculations')


def frame13_help():
    mi_text.set('Calculate measures \n '
                'Noise: used to increase de variance of the variables \n '
                'Number of samples: sets the size of the sample \n '
                'Num_bins X: used to set the bins for X \n'
                'Num_bins Y: used to set the bins for Y \n'
                'Step: is not used \n'
                'Significance: is not used')

# Principal Window -------------------------------------------------------------------------------------------------
v0 = Tk()
v0.minsize(width=300, height=400)
v0.title("Correlation comparison")
title = Label(v0, text='Structures').pack()
# Listbox ---------------------------------
frame0 = Frame(v0)
frame0.pack()
scroll1 = Scrollbar(frame0)
list1 = Listbox(frame0)
list1.pack()
set_scrollbar(list1, scroll1)
name_list = ['Sinusoidal', 'Uniform', 'Blur', 'Quadratic', 'Diagonal line 1', 'Horizontal line', 'Vertical line',
             'X line', 'Circle', 'X curve', 'Diagonal line 2', 'Dependent', 'Independent', 'Correlated', 'File']
set_list_box(name_list, list1)
# ------------------------------------------

# --- Other variables ------------------------------------------------------------------------------------------------
mi_text = StringVar()
label1 = Label(v0, textvariable=mi_text).pack()

b1 = Button(v0, text="Calculate", command=lambda: plot_select()).pack()

# --- input variables ------------------------------------------------------------------------------------------------
# Noise variable -------------------
frame1 = Frame(v0)
frame1.pack(fill=X)
L1 = Label(frame1, text='Noise: ', width=20, anchor=E).pack(side=LEFT)
noise = DoubleVar(value=0.2)
e1 = Entry(frame1, textvar=noise).pack(side=LEFT)

# Number of samples variable --------
frame2 = Frame(v0)
frame2.pack(fill=X)
l2 = Label(frame2, text='Number of samples: ', width=20, anchor=E).pack(side=LEFT)
number_sam = IntVar(value=1000)
e2 = Entry(frame2, textvar=number_sam).pack(side=LEFT)

# Number of bins in X -------------
frame3 = Frame(v0)
frame3.pack(fill=X)
l3 = Label(frame3, text='Num_bins X: ', width=20, anchor=E).pack(side=LEFT)
Bin_x = IntVar(value=40)
e3 = Entry(frame3, textvar=Bin_x).pack(side=LEFT)

# Number of bins in Y -------------
frame4 = Frame(v0)
frame4.pack(fill=X)
l4 = Label(frame4, text='Num_bins Y: ', width=20, anchor=E).pack(side=LEFT)
Bin_y = IntVar(value=40)
e4 = Entry(frame4, textvar=Bin_y).pack(side=LEFT)

# Step variable ----------------
frame5 = Frame(v0)
frame5.pack(fill=X)
l5 = Label(frame5, text='Step: ', width=20, anchor=E).pack(side=LEFT)
step = IntVar(value=100)
e5 = Entry(frame5, textvar=step).pack(side=LEFT)

# Significance variable ----------------
frame6 = Frame(v0)
frame6.pack(fill=X)
l6 = Label(frame6, text='Significance: ', width=20, anchor=E).pack(side=LEFT)
significance = DoubleVar(value=0.95)
e6 = Entry(frame6, textvar=significance).pack(side=LEFT)

# ---- Check buttons --------------------------------------------------------------------------------------------------
frame6 = Frame(v0)
frame6.pack(fill=X, padx=100)
button_6 = Button(frame6, text="?", command=lambda: frame6_help()).pack(side=LEFT)
plot_sample = IntVar(value=0)
c1 = Checkbutton(frame6, text="Plot Sample structure?", variable=plot_sample).pack(side=LEFT)


frame7 = Frame(v0)
frame7.pack(fill=X, padx=100)
button_7 = Button(frame7, text="?", command=lambda: frame7_help()).pack(side=LEFT)
plot_compare = IntVar(value=0)
c2 = Checkbutton(frame7, text="Plot Comparative?", variable=plot_compare).pack(side=LEFT)


frame8 = Frame(v0)
frame8.pack(fill=X, padx=100)
button_8 = Button(frame8, text="?", command=lambda: frame8_help()).pack(side=LEFT)
plot_proposal = IntVar(value=0)
c3 = Checkbutton(frame8, text="Plot measures for Grids ixi?", variable=plot_proposal).pack(side=LEFT)


frame9 = Frame(v0)
frame9.pack(fill=X, padx=100)
button_9 = Button(frame9, text="?", command=lambda: frame9_help()).pack(side=LEFT)
plot_partition = IntVar(value=0)
c4 = Checkbutton(frame9, text="Plot histogram of the structure?", variable=plot_partition).pack(side=LEFT)


frame10 = Frame(v0)
frame10.pack(fill=X, padx=100)
button_10 = Button(frame10, text="?", command=lambda: frame10_help()).pack(side=LEFT)
plot_converge_in_samples = IntVar(value=0)
c5 = Checkbutton(frame10, text="Plot Converge in samples?", variable=plot_converge_in_samples).pack(side=LEFT)


frame11 = Frame(v0)
frame11.pack(fill=X, padx=100)
button_11 = Button(frame11, text="?", command=lambda: frame11_help()).pack(side=LEFT)
samples_check = IntVar(value=0)
c6 = Checkbutton(frame11, text="Calculate samples for the grid?", variable=samples_check).pack(side=LEFT)


frame12 = Frame(v0)
frame12.pack(fill=X, padx=100)
button_12 = Button(frame12, text="?", command=lambda: frame12_help()).pack(side=LEFT)
bin_selection = IntVar(value=0)
c7 = Checkbutton(frame12, text="Plot bin selection validation", variable=bin_selection).pack(side=LEFT)


frame13 = Frame(v0)
frame13.pack(fill=X, padx=100)
button_13 = Button(frame13, text="?", command=lambda: frame13_help()).pack(side=LEFT)
cal_measures = IntVar(value=0)
c8 = Checkbutton(frame13, text="Calculate measures", variable=cal_measures).pack(side=LEFT)

# ---------------------------------------------------------------------------------------------------------------------

v0.mainloop()
