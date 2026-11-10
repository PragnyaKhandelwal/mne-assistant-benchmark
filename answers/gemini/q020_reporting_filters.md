The filter description you see in raw.plot() (e.g., a 16th-order Butterworth) is used strictly for real-time visualization inside the interactive plotting window to ensure smooth scrolling. It does not alter your underlying data array.

For your paper, you must report the parameters of the actual filter you applied to your data via raw.filter(0.1, 40), which uses an FIR (Finite Impulse Response) filter by default in MNE-Python, rather than the IIR Butterworth filter used by the plotter.

1. Which Parameters Should You Report?
Standard electrophysiology reporting guidelines (like COBIDAS for EEG/MEG) require the following details for your data filter:

Filter Type: Finite Impulse Response (FIR) filter.

Design Method: Windowed-sinc filter (MNE default: fir_design='firwin').

Window Type: Hamming window (fir_window='hamming', the MNE default).

Cutoff Frequencies: Pass-band edges at 0.1 Hz (high-pass) and 40 Hz (low-pass).

Transition Bandwidth: The lower and upper transition widths (automatically calculated by MNE based on your sampling rate and cutoff frequencies).

Filter Length: The total filter length (number of coefficients/taps).

Phase: Zero-phase (non-causal, symmetric, delay-compensated via phase='zero').

2. Where Do You Find These Parameters?
You can easily extract these exact values from two places:

The Python Console Logs: When you ran raw.filter(0.1, 40), MNE automatically printed a detailed breakdown to your console (logging output), including the exact filter length, transition bandwidths, and design parameters.

Programmatically: If you need to inspect or verify them without re-running the full script, you can generate the filter parameters using mne.filter.create_filter():

Python
import mne

# Pass your sampling rate (sfreq) and parameters
info = raw.info
filter_params = mne.filter.create_filter(
    data=None,
    sfreq=info['sfreq'],
    l_freq=0.1,
    h_freq=40
)
Example Methods Text for Your Paper
You can adapt a concise summary like this for your manuscript:

"Continuous data were band-pass filtered between 0.1 and 40 Hz using a finite impulse response (FIR) filter implemented in MNE-Python. The filter was designed using a windowed-sinc approach with a Hamming window (zero-phase, non-causal). [Optional: Insert transition bandwidths and filter length printed from your console log here]."
