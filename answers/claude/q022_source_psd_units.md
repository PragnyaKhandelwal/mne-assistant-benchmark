With dSPM there are no physical units. dSPM is noise-normalized (a z-like statistic, estimated source amplitude divided by its expected noise standard deviation), so the source time courses are dimensionless. The PSD is the squared amplitude per unit frequency, so the y-axis is:

**dSPM² / Hz**, or equivalently **1/Hz** (arbitrary units)

A label like `"Power (dSPM² / Hz, a.u.)"` is clear and accurate.

- **It is not a physical power.** Unlike `method="MNE"`, where the result would be (A·m)² / Hz, the values here are in noise-normalized units. They depend on your noise covariance estimate and regularization, so absolute values aren't comparable across subjects or datasets with different noise covariances. Comparing relative differences (conditions, frequency bands, regions) within the same inverse operator is fine.
- **Check the normalization in your MNE version.** The function returns a one-sided density in units²/Hz, but the exact scaling can vary slightly between versions, so skim the docstring and source if you need to be rigorous.
- **If you need physical units**, rerun with `method="MNE"` (or `"sLORETA"`/`"eLORETA"`, which are also unitless, so use plain MNE for this).
- **For plotting**, a log y-axis or 10·log10 (dB) is common. If you convert to dB, the label becomes "dB re 1 dSPM²/Hz" or simply "Power (dB)" with a note that it's relative.
