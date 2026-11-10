In MNE-Python, you can use `epochs.events` to get the original sample indices of the remaining epochs, then add annotations to `raw` using `raw.set_annotations()`.

```
import mne# Get the onset times of the remaining epochs relative to rawonsets = (epochs.events[:, 0] - raw.first_samp) / raw.info['sfreq']# Create annotationsannotations = mne.Annotations(    onset=onsets,    duration=[0] * len(onsets),    description=['kept'] * len(onsets))# Add annotations to raw in placeraw.set_annotations(raw.annotations + annotations)
```

Now:

```
raw.plot()
```

will display a `'kept'` annotation at the start of every remaining epoch.

Why subtract `raw.first_samp`? MNE event sample indices are absolute sample numbers, whereas annotation onsets are relative to the beginning of the `Raw` data. This ensures the annotations are correctly positioned, even if `raw` has a nonzero `first_samp`.
