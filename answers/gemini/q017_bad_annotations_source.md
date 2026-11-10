In MNE-Python, how your manually annotated segments (typically designated with descriptions starting with `'bad'`, such as `'bad_artifact'`) are handled depends on the specific step of the pipeline.

Here is how covariance calculation, epoching, and source estimation treat those annotations:

---

### 1. When computing Covariance

* **If you compute covariance from Epochs (`mne.compute_covariance`):**
Any epochs that overlap with a bad annotation segment will be **automatically excluded** (dropped) from the covariance calculation, provided you use an Epochs object that was created with bad-annotation rejection enabled.
* **If you compute covariance from continuous Raw data (`mne.compute_raw_covariance`):**
It features a parameter called `reject_by_annotation` (which defaults to `True`). When active, any continuous data segments overlapping with annotations starting with `'bad'` are **automatically skipped** and excluded from the covariance matrix estimation.

### 2. When creating Epochs (`mne.Epochs`)

* When you segment continuous `Raw` data into epochs using `mne.Epochs` (or `mne.make_fixed_length_epochs`), MNE checks the annotations by default.
* Any epoch that overlaps with a segment annotated as bad is **automatically dropped** and marked as a dropped epoch (you will see a log message like `<i> dropped X epochs because of a bad annotation`).

### 3. When computing Source Estimates

* Source estimation (`mne.minimum_norm.apply_inverse`, beamformers, etc.) is performed on already processed objects like **Evoked** responses, clean **Epochs**, or continuous **Raw** data.
* Because bad segments should already have been dropped or excluded during epoching or covariance computation, source estimates naturally **do not include** those bad data blocks.
* However, if you run inverse operations directly on a continuous `Raw` object that still contains bad annotated spans, MNE will still process those time points (unless they are drop-masked), which can introduce artifacts into your source time courses. Therefore, it is standard practice to drop or crop them out beforehand.

---

### Summary Checklist

* **Epochs & Raw Covariance:** Handled automatically (`reject_by_annotation=True` by default).
* **Best Practice:** Always ensure your bad annotations begin with the string `'bad'` (e.g., `'bad_blink'`, `'bad_movement'`) so MNE's internal functions recognize them automatically without requiring custom exclusion scripts.
