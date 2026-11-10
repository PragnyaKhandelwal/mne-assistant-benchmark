Yes. If your scientific question concerns only the −0.2 to 0.8 s interval, rejecting trials based on artifacts within that interval is generally a reasonable approach. In MNE-Python, you can use `reject_tmin` and `reject_tmax` to restrict the time interval used for peak-to-peak amplitude rejection while retaining the longer epochs for time-frequency analysis.

For your example:

- Epoch duration: −1 to 2 s
- Rejection interval: −0.2 to 0.8 s
- Time-frequency analysis: Use the full −1 to 2 s epoch.

This separates the interval used for artifact rejection from the interval retained for analysis.

### MNE-Python implementation

```
reject_criteria = dict(    eeg=100e-6,  # Example: 100 µV    eog=200e-6)epochs = mne.Epochs(    raw,    events,    event_id=event_id,    tmin=-1.0,    tmax=2.0,    baseline=None,    reject=reject_criteria,    reject_tmin=-0.2,    reject_tmax=0.8,    preload=True)
```

This means:

- Epoch data are retained from −1 to 2 s.
- Peak-to-peak rejection is evaluated only between −0.2 and 0.8 s.
- The same rejection interval applies to both `reject` and `flat` criteria.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

  MNE 1.13.2 documentation+1



### Important caveats

There are three things worth considering:

1\. Edge artifacts can still affect your time-frequency results.

Even if an artifact occurs outside your rejection interval, it can contaminate nearby time-frequency estimates because wavelet or sliding-window estimates use data beyond the time point being plotted.

2\. Annotation-based rejection is a separate consideration.

MNE's `reject_by_annotation=True` is enabled by default. Bad annotations can cause epochs to be dropped independently of the peak-to-peak thresholds. `reject_tmin` and `reject_tmax` also constrain annotation-based rejection in current MNE versions, but check the behavior of your installed version.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



3\. Consider the wavelet temporal support.

For example, if you use low-frequency Morlet wavelets, the effective temporal support can be quite long. An artifact at −0.8 s could influence estimates closer to your analysis window.

### My recommendation

Use `reject_tmin=-0.2` and `reject_tmax=0.8` as your primary rejection criterion, but additionally:

- Inspect the retained epochs for artifacts outside the rejection window.
- Check whether those artifacts overlap the temporal support of your wavelets.
- Consider excluding contaminated time-frequency estimates near the edges.
- Report the rejection interval explicitly in your methods.

One important distinction: `reject_tmin` and `reject_tmax` control peak-to-peak rejection; they do not guarantee that the retained epochs are artifact-free throughout their entire duration.

Documentation: [MNE-Python Epochs API](https://mne.tools/stable/generated/mne.Epochs.html?utm_source=chatgpt.com).
