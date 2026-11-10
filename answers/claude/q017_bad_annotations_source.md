Mostly yes, but it depends on the function, and there are a few places where annotations are silently *not* respected. The key is that MNE only honors annotations whose description starts with `BAD` (e.g. `BAD_artifact`, `BAD_muscle`, `bad_segment` won't work, since the match is case-sensitive on the `BAD` prefix).

## Where BAD annotations are excluded

**Epoching (`mne.Epochs`)**
- Epochs that overlap a `BAD_*` annotation are dropped by default (`reject_by_annotation=True`).
- This is a rejection of the whole epoch, not trimming. Even a small overlap removes it.
- The drop is logged under `epochs.drop_log` with reason `'BAD_xxx'`.
- Note that this applies when you create epochs from raw data. If you use fixed-length epochs (`mne.make_fixed_length_epochs`), it also takes `reject_by_annotation=True` by default.

**Covariance from Raw (`mne.compute_raw_covariance`)**
- Default `reject_by_annotation=True`. Bad segments are excluded, and the data are effectively handled in the good stretches only.
- Within this function, rejection is done on the annotation basis, and the `tstep` windows overlapping bad spans are skipped.

**Covariance from Epochs (`mne.compute_covariance(epochs)`)**
- It uses whatever epochs survived. If the bad segments already caused epochs to be dropped, they are excluded implicitly. It does not look at annotations again.

**Raw data access**
- `raw.get_data(reject_by_annotation='omit')` drops the bad spans (concatenating the rest), or `'NaN'` fills them with NaN. The default is `None`, which **returns everything, including bad segments**.

**Filtering/resampling/ICA**
- `raw.filter()` filters continuously across the bad segments and doesn't skip them. This matters because annotated spans still influence edge behavior. If you want to handle this, filter first, then annotate, or use `skip_by_annotation` (default `('edge', 'bad_acq_skip')`), which only skips annotations of those specific types.
- `ICA.fit(raw, reject_by_annotation=True)` is the default, so it excludes bad segments.

## Where they are NOT automatically excluded

**Source estimates applied to Raw (`apply_inverse_raw`)**
- This applies the inverse to the full raw data, **including annotated bad segments**. There's an argument `reject_by_annotation` in newer versions only for some functions, but `apply_inverse_raw` has `start`/`stop` and `buffer_size` and does not drop annotated spans. You'll get source time courses covering the bad data too.
- The same goes for `mne.minimum_norm.apply_inverse_raw`'s output being a continuous `SourceEstimate`. Annotations are not carried through.

**Beamformers (`make_lcmv`)**
- The data covariance you pass in determines what's excluded. The filter itself is not annotation-aware. If you computed covariance with `compute_raw_covariance` (default `reject_by_annotation=True`), you're fine. But the application step (`apply_lcmv_raw`) again processes everything.

**`raw.copy().crop()`, `raw.plot_psd()`, `raw.compute_psd()`**
- `compute_psd` has `reject_by_annotation=True` by default for Raw and so respects BAD annotations. Plain cropping doesn't care.

## Practical recommendation for resting state

A robust pattern:

1. Annotate with `BAD_` prefixed descriptions.
2. Compute the noise/data covariance with `compute_raw_covariance(raw, reject_by_annotation=True)` or from fixed-length epochs.
3. Make fixed-length epochs (`reject_by_annotation=True`), and verify with `epochs.drop_log` and `len(epochs)` against what you expected.
4. Apply the inverse to the **epochs** (`apply_inverse_epochs`) instead of the raw object. This guarantees bad segments are not reconstructed, since they never made it into epochs.
5. Sanity check: `print(raw.annotations)` and inspect how much total duration is marked bad (`raw.annotations.duration.sum()`), compared to what `epochs` retained.

## Caveats worth verifying in your version

Details like default arguments and exact behavior have shifted a bit across MNE releases (e.g., the handling of annotations in `compute_raw_covariance` and in `apply_inverse_raw`). I'd confirm against the docs for your installed version (`mne.sys_info()` to check), or test empirically: mark an obvious artifact as `BAD_test` and confirm the number of resulting epochs or covariance sample count (`cov['nfree']`) changes as expected.

If you share which steps you use (raw covariance vs. epochs, which inverse method), I can say precisely where bad segments could leak through.
