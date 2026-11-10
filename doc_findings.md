# Documentation findings

MNE documentation pages that the pilot failures point to. These are candidates for
discussion, not changes anyone has agreed to.

| Failure | Assistants | Page | What seems unclear or missing |
|---|---|---|---|
| Annotation onsets shifted when the recording has a measurement date (q009, earlier runs) | Gemini, ChatGPT | `mne.Annotations` (`orig_time`), `Raw.set_annotations` | How onsets relate to `first_samp` and `meas_date`, and when `first_samp` must be subtracted, is easy to get wrong; a short worked example could help. |
| `mean_flip` used on all-positive dSPM estimates (q016) | all three | `mne.extract_label_time_course` (`mode`) | The modes are described, but not when *not* to use `mean_flip` (magnitude estimates such as free-orientation dSPM). |
| Removed montage names `standard_1020` / `standard_1005` (q010, q019, q024) | all three | 1.13 changelog, `make_standard_montage`, no-MRI tutorial | Assistants still default to the old names, even when told the version. Open question for maintainers: would temporary deprecated aliases, or a "did you mean colin27_1020?" hint in the error, help users with older scripts? |
| `adjacency=None` described as fully connected or harmless (q021) | Claude, ChatGPT | `spatio_temporal_cluster_1samp_test` (`adjacency`) | The docstring is accurate, but a warning that `None` is rarely appropriate for sensor data might prevent misuse. |
| Original events reused after `raw.resample` (q007) | Gemini, ChatGPT | `Raw.resample` | The warning against resampling before epoching exists, but assistants still miss it. |
| Status channel assumed to become annotations (q005) | (criterion not met by Gemini, Claude) | `read_raw_bdf` notes | The notes explain that only TAL channels are parsed; the distinction could be stated earlier. |
