"""
Calculate power law exponent of the cumulative degree histogram.
"""


def powerlaw_exp(xdata = None, ydata = None, yerr = None):
    """Calculate power law coefficients."""

    from scipy import randn, optimize
    from numpy import array, sqrt, linspace, log10

    # Define function for calculating a power law
    powerlaw = lambda x, amp, index: amp * (x**index)

    if xdata == None:
        # Generate data points with noise
        num_points = 20
        # Note: all positive, non-zero data
        xdata = linspace(1.1, 10.1, num_points)
        ydata = powerlaw(xdata, 10.0, -3.0)     # simulated perfect data
        yerr = 0.2 * ydata                      # simulated errors (10%)

        ydata += randn(num_points) * yerr       # simulated noisy data

    if yerr == None:
        yerr = .1 * array(ydata)

    # Fitting the data -- Least Squares Method
    
    # Power-law fitting is best done by first coverting
    # to a linear equation and then fitting to a straight line.
    #
    #  y = a * x^b
    #  log(y) = log(a) + b*log(x)
    
    logx = log10(xdata)
    logy = log10(ydata)
    logyerr = yerr / ydata

    
    # define our (line) fitting function
    fitfunc = lambda p, x: p[0] + p[1] * x
    errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

    pinit = [1.0, -1.0]
    out = optimize.leastsq(errfunc, pinit,
                           args=(logx, logy, logyerr), full_output=1)
    
    pfinal = out[0]
    covar = out[1]
    # print pfinal
    # print covar
    
    index = pfinal[1]
    amp = 10.0**pfinal[0]
    
    indexErr = sqrt( covar[0][0] )
    ampErr = sqrt( covar[1][1] ) * amp


    # from pylab import *
    if False:
    ##########
        # Plotting data
        
        clf()
        subplot(2, 1, 1)
        plot(xdata, powerlaw(xdata, amp, index))     # Fit
        errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
        text(5, 6.5, 'Ampli = %5.2f +/- %5.2f' % (amp, ampErr))
        text(5, 5.5, 'Index = %5.2f +/- %5.2f' % (index, indexErr))
        title('Best Fit Power Law')
        xlabel('X')
        ylabel('Y')
        xlim(1, 11)
    
        subplot(2, 1, 2)
        loglog(xdata, powerlaw(xdata, amp, index))
        errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
        xlabel('X (log scale)')
        ylabel('Y (log scale)')
        xlim(1.0, 11)

        savefig('power_law_fit.png')

    return pfinal

def cum_deg_histogram(G):
    """Cumulative degree histogram."""
    from numpy import cumsum
    from networkx import degree_histogram
    deg_hist = degree_histogram(G)
    deg_hist.reverse()
    cum_deg_hist = list(cumsum(deg_hist))
    cum_deg_hist.reverse()
    return cum_deg_hist


def power_exp_cum_deg_hist(G):
    """Calculate power law exponent of the cumulative degree histogram."""
    from scipy import arange
    cum_deg_hist = cum_deg_histogram(G)
    deg = arange(len(cum_deg_hist)) + 1
    return powerlaw_exp(deg, cum_deg_hist)[1]
    

if __name__ == "__main__":
    from Dataset.Advogato import *
    from Dataset.Dummy import DummyNetwork

    S = SqueakFoundationNetwork(date = '2007-12-25')
    # S.info()
    print power_exp_cum_deg_hist(S)


"""
Calculate power law exponent of the cumulative degree histogram.
"""


def powerlaw_exp(xdata = None, ydata = None, yerr = None):
    """Calculate power law coefficients."""

    from scipy import randn, optimize
    from numpy import array, sqrt, linspace, log10

    # Define function for calculating a power law
    powerlaw = lambda x, amp, index: amp * (x**index)

    if xdata == None:
        # Generate data points with noise
        num_points = 20
        # Note: all positive, non-zero data
        xdata = linspace(1.1, 10.1, num_points)
        ydata = powerlaw(xdata, 10.0, -3.0)     # simulated perfect data
        yerr = 0.2 * ydata                      # simulated errors (10%)

        ydata += randn(num_points) * yerr       # simulated noisy data

    if yerr == None:
        yerr = .1 * array(ydata)

    # Fitting the data -- Least Squares Method
    
    # Power-law fitting is best done by first coverting
    # to a linear equation and then fitting to a straight line.
    #
    #  y = a * x^b
    #  log(y) = log(a) + b*log(x)
    
    logx = log10(xdata)
    logy = log10(ydata)
    logyerr = yerr / ydata

    
    # define our (line) fitting function
    fitfunc = lambda p, x: p[0] + p[1] * x
    errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

    pinit = [1.0, -1.0]
    out = optimize.leastsq(errfunc, pinit,
                           args=(logx, logy, logyerr), full_output=1)
    
    pfinal = out[0]
    covar = out[1]
    # print pfinal
    # print covar
    
    index = pfinal[1]
    amp = 10.0**pfinal[0]
    
    indexErr = sqrt( covar[0][0] )
    ampErr = sqrt( covar[1][1] ) * amp


    # from pylab import *
    if False:
    ##########
        # Plotting data
        
        clf()
        subplot(2, 1, 1)
        plot(xdata, powerlaw(xdata, amp, index))     # Fit
        errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
        text(5, 6.5, 'Ampli = %5.2f +/- %5.2f' % (amp, ampErr))
        text(5, 5.5, 'Index = %5.2f +/- %5.2f' % (index, indexErr))
        title('Best Fit Power Law')
        xlabel('X')
        ylabel('Y')
        xlim(1, 11)
    
        subplot(2, 1, 2)
        loglog(xdata, powerlaw(xdata, amp, index))
        errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
        xlabel('X (log scale)')
        ylabel('Y (log scale)')
        xlim(1.0, 11)

        savefig('power_law_fit.png')

    return pfinal

def cum_deg_histogram(G):
    """Cumulative degree histogram."""
    from numpy import cumsum
    from networkx import degree_histogram
    deg_hist = degree_histogram(G)
    deg_hist.reverse()
    cum_deg_hist = list(cumsum(deg_hist))
    cum_deg_hist.reverse()
    return cum_deg_hist


def power_exp_cum_deg_hist(G):
    """Calculate power law exponent of the cumulative degree histogram."""
    from scipy import arange
    cum_deg_hist = cum_deg_histogram(G)
    deg = arange(len(cum_deg_hist)) + 1
    return powerlaw_exp(deg, cum_deg_hist)[1]
    

if __name__ == "__main__":
    from Dataset.Advogato import *
    from Dataset.Dummy import DummyNetwork

    S = SqueakFoundationNetwork(date = '2007-12-25')
    # S.info()
    print power_exp_cum_deg_hist(S)


"""
Calculate power law exponent of the cumulative degree histogram.
"""


def powerlaw_exp(xdata = None, ydata = None, yerr = None):
    """Calculate power law coefficients."""

    from scipy import randn, optimize
    from numpy import array, sqrt, linspace, log10

    # Define function for calculating a power law
    powerlaw = lambda x, amp, index: amp * (x**index)

    if xdata == None:
        # Generate data points with noise
        num_points = 20
        # Note: all positive, non-zero data
        xdata = linspace(1.1, 10.1, num_points)
        ydata = powerlaw(xdata, 10.0, -3.0)     # simulated perfect data
        yerr = 0.2 * ydata                      # simulated errors (10%)

        ydata += randn(num_points) * yerr       # simulated noisy data

    if yerr == None:
        yerr = .1 * array(ydata)

    # Fitting the data -- Least Squares Method
    
    # Power-law fitting is best done by first coverting
    # to a linear equation and then fitting to a straight line.
    #
    #  y = a * x^b
    #  log(y) = log(a) + b*log(x)
    
    logx = log10(xdata)
    logy = log10(ydata)
    logyerr = yerr / ydata

    
    # define our (line) fitting function
    fitfunc = lambda p, x: p[0] + p[1] * x
    errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

    pinit = [1.0, -1.0]
    out = optimize.leastsq(errfunc, pinit,
                           args=(logx, logy, logyerr), full_output=1)
    
    pfinal = out[0]
    covar = out[1]
    # print pfinal
    # print covar
    
    index = pfinal[1]
    amp = 10.0**pfinal[0]
    
    indexErr = sqrt( covar[0][0] )
    ampErr = sqrt( covar[1][1] ) * amp


    # from pylab import *
    if False:
    ##########
        # Plotting data
        
        clf()
        subplot(2, 1, 1)
        plot(xdata, powerlaw(xdata, amp, index))     # Fit
        errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
        text(5, 6.5, 'Ampli = %5.2f +/- %5.2f' % (amp, ampErr))
        text(5, 5.5, 'Index = %5.2f +/- %5.2f' % (index, indexErr))
        title('Best Fit Power Law')
        xlabel('X')
        ylabel('Y')
        xlim(1, 11)
    
        subplot(2, 1, 2)
        loglog(xdata, powerlaw(xdata, amp, index))
        errorbar(xdata, ydata, yerr=yerr, fmt='k.')  # Data
        xlabel('X (log scale)')
        ylabel('Y (log scale)')
        xlim(1.0, 11)

        savefig('power_law_fit.png')

    return pfinal

def cum_deg_histogram(G):
    """Cumulative degree histogram."""
    from numpy import cumsum
    from networkx import degree_histogram
    deg_hist = degree_histogram(G)
    deg_hist.reverse()
    cum_deg_hist = list(cumsum(deg_hist))
    cum_deg_hist.reverse()
    return cum_deg_hist


def power_exp_cum_deg_hist(G):
    """Calculate power law exponent of the cumulative degree histogram."""
    from scipy import arange
    cum_deg_hist = cum_deg_histogram(G)
    deg = arange(len(cum_deg_hist)) + 1
    return powerlaw_exp(deg, cum_deg_hist)[1]
    

if __name__ == "__main__":
    from Dataset.Advogato import *
    from Dataset.Dummy import DummyNetwork

    S = SqueakFoundationNetwork(date = '2007-12-25')
    # S.info()
    print power_exp_cum_deg_hist(S)


