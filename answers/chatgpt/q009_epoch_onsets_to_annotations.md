You can use `epochs.events` to retrieve the original sample indices of the remaining epochs, then create zero-duration annotations at those positions in `raw`.

```
import mneimport numpy as np# Get the original sample indices of the remaining epochsonsets = (epochs.events[:, 0] - raw.first_samp) / raw.info['sfreq']# Create annotations marking kept epochsannotations = mne.Annotations(    onset=onsets,    duration=np.zeros(len(onsets)),    description=['kept'] * len(onsets),    orig_time=raw.annotations.orig_time)# Add annotations to raw in placeraw.set_annotations(raw.annotations + annotations)
```

### Visualize the annotations

```
raw.plot()
```

You should see a `'kept'` annotation at the beginning of each remaining epoch.

Important: This assumes your epochs have not been resampled or otherwise altered in a way that changes their event sample indices relative to the original `raw`.

Also, if you want to mark the entire epoch duration rather than just its start, replace:

```
duration=np.zeros(len(onsets))
```

with:

```
duration=np.full(len(onsets), epochs.tmax - epochs.tmin)
```

In that case, the annotation onset should also be adjusted to the actual epoch start:

```
onsets = (    epochs.events[:, 0] - raw.first_samp) / raw.info['sfreq'] + epochs.tmin
```
