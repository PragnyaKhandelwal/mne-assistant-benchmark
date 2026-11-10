Use `Raw.set_montage()` with a standard montage. It modifies `raw` in place and attaches the positions to `raw.info`.

```python
import mne

montage = mne.channels.make_standard_montage("standard_1020")
raw.set_montage(montage)
```

That's all you need. Topomap plotting (`raw.plot_sensors()`, `evoked.plot_topomap()`, `raw.compute_psd().plot_topomap()`, etc.) will now work.

**Things to watch for**

- **Case sensitivity.** Standard montages use names like `Fp1`, `Fz`, `FCz`, `POz`. If your channels are uppercase (`FP1`, `FZ`) or otherwise differ in case, pass `match_case=False`:

  ```python
  raw.set_montage(montage, match_case=False)
  ```

- **Channels not in the montage.** By default, if your data has channels (other than non-EEG types like EOG, ECG, stim, etc.) that the montage doesn't know about, `set_montage` raises an error. Options:
  - Mark them with the right type first: `raw.set_channel_types({"EOG1": "eog"})`
  - Or let them through without positions: `raw.set_montage(montage, on_missing="ignore")` (or `"warn"`)

- **Old 10-20 names.** If you have legacy names (`T3`, `T4`, `T5`, `T6`), rename them to the modern equivalents (`T7`, `T8`, `P7`, `P8`) first:

  ```python
  raw.rename_channels({"T3": "T7", "T4": "T8", "T5": "P7", "T6": "P8"})
  ```

- **Choosing a different template.** `standard_1020` is a good default. If you have extra sites, `standard_1005` is a superset, and `biosemi32`, `easycap-M1`, etc. exist for specific caps. You can list them all with `mne.channels.get_builtin_montages()`.

**Quick check**

```python
raw.plot_sensors(show_names=True)
```
