The key distinction is that the 16th-order Butterworth shown by `raw.plot()` may not represent the actual filter order used in your filtering operation. You should report the parameters of the filter that was actually applied using `raw.filter(0.1, 40)`.

Assuming you are using MNE-Python, here's what you should report and where to find it.

## 1. Parameters to report in your paper

For your command:

```
raw.filter(0.1, 40)
```

You should report:

| Parameter             | What to report                                                          |
| --------------------- | ----------------------------------------------------------------------- |
| Filter type           | Butterworth (if configured as such; otherwise report the actual design) |
| Filter range          | 0.1–40 Hz                                                               |
| Filter direction      | Zero-phase (default in MNE for the usual IIR filtering configuration)   |
| Filter order          | Actual order used by the filter                                         |
| Filter implementation | IIR or FIR                                                              |
| Sampling frequency    | Your recording's sampling frequency                                     |
| Phase characteristics | Zero-phase, if applicable                                               |

Important: MNE-Python's default filtering method is FIR, not Butterworth. Therefore, `raw.filter(0.1, 40)` does not automatically mean that a Butterworth filter was applied.

## 2. Where to find the actual filter parameters

First, inspect your filtering command and the MNE output in your Python console.

For example:

```
raw.filter(0.1, 40)
```

MNE usually prints information about the filter design, including:

- Filter length
- Lower and upper passband edges
- Transition bandwidths
- Filter type (FIR/IIR)
- Window and design method

If you explicitly used an IIR Butterworth filter, you might have something like:

```
raw.filter(    0.1,    40,    method='iir',    iir_params=dict(order=4, ftype='butter'))
```

You can inspect the IIR filter settings using:

```
raw.filter(    0.1,    40,    method='iir',    iir_params=dict(order=4, ftype='butter'))
```

The actual filter order is then specified explicitly.

## 3. Why does `raw.plot()` show a 16th-order Butterworth?

This is an important detail.

The filter displayed in `raw.plot()` may be a visualization setting used for displaying the data rather than the filter previously applied to your actual recording.

In other words:

- `raw.filter()` applies a filter to the data.
- `raw.plot()` can display data using a separate visualization filter.

These should not be confused when reporting methods in a paper.

## 4. Example of how to write it in your paper

If you used MNE's default FIR filtering:

> The continuous EEG data were band-pass filtered between 0.1 and 40 Hz using a finite impulse response (FIR) filter implemented in MNE-Python.

If you actually used a Butterworth IIR filter:

> The continuous EEG data were band-pass filtered between 0.1 and 40 Hz using a Butterworth infinite impulse response (IIR) filter. The filter order and phase characteristics were [specify actual values].

## One thing I'd like to clarify

Could you share the output of:

```
raw.filter(0.1, 40)
```

Specifically, the messages printed in your Python console when filtering.

I can then help you identify the exact filter type, order, phase, and other parameters to report in your research paper, without accidentally reporting the 16th-order visualization filter as your actual preprocessing filter.
