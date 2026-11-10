If you computed the PSD using `method='dSPM'`, the y-axis should generally be labelled:

dSPM²/Hz (or (noise-normalized units)²/Hz).

It should not be labelled `A²/Hz`, `(nAm)²/Hz`, or `(V/m)²/Hz`, because dSPM estimates are noise-normalized rather than expressed in physical source-current units.

A small but important distinction: dSPM is a noise-normalized, dimensionless estimate. Therefore, its PSD has units of dimensionless²/Hz, conventionally written as `1/Hz`.

For a publication, I would use:

- Y-axis: `dSPM²/Hz`
- X-axis: `Frequency (Hz)`

The MNE discussion explicitly confirms that dSPM source estimates are unitless, and that their derived power quantities do not inherit physical units.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.discourse.group\&sz=32)

MNE Forum+1



Also, `compute_source_psd_epochs()` does not automatically convert the output to dB. You are working with linear PSD values, not log power.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1



My recommendation: Label it `dSPM²/Hz` for clarity, rather than simply `Power (a.u.)`.
