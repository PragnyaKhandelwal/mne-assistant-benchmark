For source localization in MNE-Python, the recommended approach is to add the average reference as a **projector** rather than applying it immediately. MNE's inverse operators require it, and a projector keeps the reference consistent through epoching, evoking, and inverse computation.

```python
# Modifies `raw` in place. Adds the average-reference projector (not yet applied).
raw.set_eeg_reference("average", projection=True)

# Apply the projector so the data is actually re-referenced
raw.apply_proj()
```

**Why a projector?**
- `make_inverse_operator` checks that an average-reference projector is present for EEG and raises an error if it isn't. Adding it as a projector (`projection=True`) satisfies this and ensures the forward/inverse computations use the same reference.
- Projectors are carried along to `Epochs` and `Evoked` objects, so the reference stays consistent through your pipeline.

**Notes**

1. **Bad channels first.** Mark bad channels (`raw.info["bads"]`) or interpolate them *before* setting the reference. Otherwise they contaminate the average. For example:
   ```python
   raw.interpolate_bads()          # needs a montage/channel positions set
   raw.set_eeg_reference("average", projection=True)
   raw.apply_proj()
   ```
   If you interpolate, the bads are reset, so all channels contribute to the average.

2. **Montage required.** Source localization needs channel locations, so make sure you've set one (e.g. `raw.set_montage("standard_1020")`).

3. **Direct (non-projector) alternative.** If you want to re-reference immediately without a projector:
   ```python
   raw.set_eeg_reference("average", projection=False)
   ```
   This works for plain analysis, but for dSPM you'll still need an average-reference projector when computing the inverse, so the projection approach above is simpler and safer.

4. **Order with other preprocessing.** Do filtering and ICA/artifact removal as appropriate, and keep the reference step consistent with what you'll use for the forward model (MNE's forward solution for EEG assumes an average reference).

If you later build the inverse operator, you can verify the projector is there with:
```python
print(raw.info["projs"])
```
It should list an entry like `Average EEG reference`.
