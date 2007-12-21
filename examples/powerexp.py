import scipy.linalg.basic

import Advogato

def test(x = None, y = None):
    xdata = x or [5.357, 5.457, 5.797, 5.936, 6.161, 6.697, 6.731, 6.775, 8.442, 9.769,
             9.861]
    ydata = y or [0.376, 0.489, 0.874, 1.049, 1.327, 2.054, 2.077, 2.138, 4.744, 7.068,
             7.104]
    matrix = []

    for x in xdata:
        # matrix.append([1.0, x, x*x]) # for y = a + bx + cx^2
        matrix.append([1.0, x]) # for y = a + bx + cx^2

    coeffs = scipy.linalg.basic.lstsq(matrix, ydata)[0]

    print "scipy.linalg.basic.lstsq curve fitting example"
    print "fitting data to quadratic equation y = a + bx + cx^2"
    
    print "yields:  x data     y data    calc value   error"

    for i in range(len(xdata)):
        ycalc = coeffs[0] + coeffs[1] * xdata[i]  # + coeffs[2] * xdata[i] * xdata[i]
        error = ycalc - ydata[i]
        print "         % .3f    % .3f      % .3f    % .3f" % (xdata[i], ydata[i],
                                                               ycalc, error)
        print
        
    print "coeffs:", coeffs


def test(xdata, ydata):
    matrix = []

    for x in xdata:
        # matrix.append([1.0, x, x*x]) # for y = a + bx + cx^2
        matrix.append([1.0, x]) # for y = a + bx + cx^2

    coeffs = scipy.linalg.basic.lstsq(matrix, ydata)[0]

    print "scipy.linalg.basic.lstsq curve fitting example"
    print "fitting data to quadratic equation y = a + bx + cx^2"
    
    print "yields:  x data     y data    calc value   error"

    for i in range(len(xdata)):
        ycalc = coeffs[0] *  pow(xdata[i], coeffs[1])  # + coeffs[2] * xdata[i] * xdata[i]
        error = ycalc - ydata[i]
        print "         % .3f    % .3f      % .3f    % .3f" % (xdata[i], ydata[i],
                                                               ycalc, error)
        print
        
    print "coeffs:", coeffs

if __name__ == "__main__":
    #     test()
    import Advogato
    G = Advogato.Kaitiaki()
