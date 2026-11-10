When you compute source-space power spectra using `mne.minimum_norm.compute_source_psd_epochs` with **dSPM** (Dynamic Statistical Parametric Mapping), the units on the y-axis are **$(\text{dSPM})^2/\text{Hz}$** (often expressed simply as **dimensionless power per Hz**, **$\text{dSPM}^2 / \text{Hz}$**, or **arbitrary units (a.u.)**).

### Why these units?

1. **Standard MNE (`method='MNE'`):** If you use the standard linear inverse operator, the source estimates represent current dipole moments. For MEG, these are typically in **Ampere-meters ($\text{Am}$)**, meaning the resulting PSD units would be $\text{Am}^2/\text{Hz}$.
2. **dSPM (`method='dSPM'`):** dSPM normalizes the minimum-norm estimate at each vertex by dividing it by the estimated noise standard deviation (derived from the noise covariance matrix). Because you divide an amplitude by its noise standard deviation, the resulting dSPM values are **dimensionless** (similar to a $Z$-score or a noise-normalized statistical map).
3. **Power Spectral Density:** Taking the PSD of a dimensionless, noise-normalized time series squares those values and divides by frequency resolution, yielding **$(\text{dSPM})^2/\text{Hz}$**.

### How to label your plot:

* **Precise label:** $(\text{dSPM})^2/\text{Hz}$
* **General/Publication-friendly label:** **Power ($\text{dSPM}^2/\text{Hz}$)** or **Power (arbitrary units)**.

Because dSPM values are unitless noise-normalized metrics, reviewers and readers do not expect strict physical units (like $\text{Am}^2/\text{Hz}$) on the y-axis, making $(\text{dSPM})^2/\text{Hz}$ or arbitrary units standard practice.
