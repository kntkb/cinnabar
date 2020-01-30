import numpy as np
import matplotlib.pylab as plt
from freeenergyframework import stats


def _master_plot(x, y, title='',
                 xerr=None, yerr=None,
                 method_name='', target_name='',
                 guidelines=True, origins=True,
                 statistics=['RMSE', 'MUE']):
    nsamples = len(x)
    # aesthetics
    plt.figure(figsize=(10, 10))
    plt.xlabel(f'Experimental / kcal mol$^{-1}$')
    plt.ylabel(f'Calculated {method_name} / kcal mol$^{-1}$')

    ax_min = min(min(x), min(y)) - 0.5
    ax_max = max(max(x), max(y)) + 0.5
    scale = [ax_min, ax_max]

    plt.xlim(scale)
    plt.ylim(scale)
    if origins:
        plt.plot([0, 0], scale, 'gray')
        plt.plot(scale, [0, 0], 'gray')
    plt.plot(scale, scale, 'k:')
    if guidelines:
        small_dist = 0.5
        plt.fill_between(scale, [ax_min-small_dist, ax_max-small_dist],
                         [ax_min+small_dist, ax_max+small_dist],
                         color='grey', alpha=0.2)
        plt.fill_between(scale, [ax_min-small_dist*2, ax_max-small_dist*2],
                         [ax_min+small_dist*2, ax_max+small_dist*2],
                         color='grey', alpha=0.2)
    # actual plotting
    plt.scatter(x, y,color='hotpink')
    plt.errorbar(x, y, xerr=xerr, yerr=yerr, color='hotpink', linewidth=0., elinewidth=2.)

    # stats and title
    statistics_string = ''
    for statistic in statistics:
        s = stats.bootstrap_statistic(x, y, statistic=statistic)
        string = f"{statistic}:   {s['mle']:.2f} [95%: {s['low']:.2f}, {s['high']:.2f}] kcal mol$^-$$^1$ \n"
        statistics_string += string

    long_title = f'{title} \n {target_name} (N = {nsamples}) \n {statistics_string}'

    plt.title(long_title, fontsize=11, loc='right', horizontalalignment='right', family='monospace')
    plt.show()

def plot_DDGs(results,method_name='',target_name='',title='',map_positive=False):
    # data
    if not map_positive:
        x_data = np.asarray([x.exp_DDG for x in results])
        y_data = np.asarray([x.calc_DDG for x in results])
    else:
        x_data = []
        y_data = []
        for i,j in zip([x.exp_DDG for x in results],[x.calc_DDG for x in results]):
            if i < 0:
                x_data.append(-i)
                y_data.append(-j)
            else:
                x_data.append(i)
                y_data.append(j)
        x_data = np.asarray(x_data)
        y_data = np.asarray(y_data)
    xerr = np.asarray([x.dexp_DDG for x in results])
    yerr = np.asarray([x.dcalc_DDG for x in results])

    _master_plot(x_data, y_data,
                 xerr=xerr, yerr=yerr,
                 title=title, method_name=method_name, target_name=target_name)


def plot_DGs(results, method_name='', target_name='', title=''):
    from freeenergyframework import absolute
    # data
    x_data, y_data, xerr, yerr = absolute.generate_absolute_values(results)

    _master_plot(x_data, y_data,
                 xerr=xerr, yerr=yerr,
                 origins=False,statistics=['RMSE','MUE','R2','rho'],
                 title=title, method_name=method_name, target_name=target_name)


def plot_all_DDGs(results,method_name='',target_name='',title=''):
    from freeenergyframework import absolute
    import itertools
    # data
    x_abs, y_abs, xabserr, yabserr = absolute.generate_absolute_values(results)

    # do all to plot_all
    x_data = []
    y_data = []
    xerr = []
    yerr = []
    for a, b in itertools.combinations(range(len(x_abs)),2):
        x = x_abs[a] - x_abs[b]
        x_data.append(x)
        x_data.append(-x)
        err = (xabserr[a]**2 + xabserr[b]**2)**0.5
        xerr.append(err)
        xerr.append(err)
        y = y_abs[a] - y_abs[b]
        y_data.append(y)
        y_data.append(-y)
        err = (yabserr[a]**2 + yabserr[b]**2)**0.5
        yerr.append(err)
        yerr.append(err)
    x_data = np.asarray(x_data)
    y_data = np.asarray(y_data)

    _master_plot(x_data, y_data,
                 xerr=xerr, yerr=yerr,
                 title=title, method_name=method_name, target_name=target_name)
