```
variances = np.var(raw.get_data(reject_by_annotation='omit'), axis=1)
```

This excludes spans annotated with `BAD_` (and MNE's `EDGE` annotations) and computes the variance independently for each channel, producing an array of shape `(n_channels,)`.
