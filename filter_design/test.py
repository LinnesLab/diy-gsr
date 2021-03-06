# from https://developer.mbed.org/handbook/SciPy-FIR-Filter

from numpy import sin, arange, pi
from scipy.signal import lfilter, firwin
from pylab import figure, plot, grid, show

# Create a signal for demonstration
# 320 samples of (1000Hz + 150000 Hz) at 48 kHz
sample_rate = 48000.
nsamples = 320

F_1KHz = 1000.
A_1KHz = 1.0

F_15KHz = 15000.
A_15KHz = 0.5

t = arange(nsamples) / sample_rate
signal = A_1KHz * sin(2*pi*F_1KHz*t) + A_15KHz*sin(2*pi*F_15KHz*t)

# Create FIR filter and apply it to signal

# Nyquist rate
nyq_rate = sample_rate / 2

# cutoff freq of filter
cutoff_hz = 6000.0

# length of filter (number of coefficients, i.e. filter order + 1)
numtaps = 33

# Use firwin to create a lowpass FIR filter (use firwin FTW)
fir_coeff = firwin(numtaps, cutoff_hz/nyq_rate)

#fir_coeff = firwin(numtaps, cutoff = 0.4, window='hamming')

# http://mpastell.com/2010/01/18/fir-with-scipy/
# lowpass filters look like this
# a = firwin(n, cutoff=0.3, window='blackmanharris')
# highpass filters look like this
# b = - firwin(n, cutoff=0.5, window='blackmanharris')
# b[n/2] = b[n/2] + 1
# combine them to make a bandpass filter
# d = - (a + b)
# d[n/2] = d[n/2] + 1

# Use lfilter to filter the signal with the FIR filter
filtered_signal = lfilter(fir_coeff, 1.0, signal)


#------------------------------------------------
# Plot the original and filtered signals.
#------------------------------------------------

# The first N-1 samples are "corrupted" by the initial conditions
warmup = numtaps - 1

# The phase delay of the filtered signal
delay = (warmup / 2) / sample_rate

figure(1)
# Plot the original signal
plot(t, signal)

# Plot the filtered signal, shifted to compensate for the phase delay
#plot(t-delay, filtered_signal, 'r-')

# Plot just the "good" part of the filtered signal.  The first N-1
# samples are "corrupted" by the initial conditions.
plot(t[warmup:]-delay, filtered_signal[warmup:], 'g', linewidth=2)

grid(True)

show()

#------------------------------------------------
# Print values
#------------------------------------------------
def print_values(label, values):
    var = "float32_t %s[%d]" % (label, len(values))
    print "%-30s = {%s}" % (var, ', '.join(["%+.10f" % x for x in values]))

#print_values('signal', signal)
#print_values('fir_coeff', fir_coeff)
#print_values('filtered_signal', filtered_signal)
