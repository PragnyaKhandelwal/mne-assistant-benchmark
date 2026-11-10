When using `fsaverage` as a template MRI for EEG source localization without individual participant MRIs, electrode misalignment usually happens due to coordinate frame mismatches or unaligned transformation parameters (`trans`).

### Recommended Montage and Transformation

1. **Montage:** Use **`standard_1005`** (or **`standard_1020`**). These standard montages are provided in MNI/MRI coordinate space, which natively aligns with the `fsaverage` template brain.
2. **Transformation (`trans`):** Use the built-in shortcut **`trans = 'fsaverage'`**. MNE-Python provides this pre-computed transformation string to map standard MNI-space electrode coordinates directly to the `fsaverage` head/MRI coordinate system.

---

### Step-by-Step Code Example

To ensure your electrodes line up correctly on the scalp, follow this workflow in MNE-Python 1.13:

```python
import mne
from mne.datasets import fetch_fsaverage

# 1. Ensure your subjects_dir contains 'fsaverage'
subjects_dir = mne.datasets.fetch_fsaverage(verbose=True)

# 2. Clean channel names to match standard 10-05/10-20 naming conventions
# (e.g., uppercase, removing trailing dots like 'Fp1.' -> 'Fp1')
new_names = {
    ch_name: ch_name.rstrip(".").upper().replace("Z", "z").replace("FP", "Fp")
    for ch_name in raw.ch_names
}
raw.rename_channels(new_names)

# 3. Set the standard montage (in MNI space)
montage = mne.channels.make_standard_montage("standard_1005")
raw.set_montage(montage)

# 4. Define paths and the built-in fsaverage transform
subject = "fsaverage"
trans = "fsaverage"  # Built-in MNE shortcut for fsaverage coregistration

fs_dir = subjects_dir / subject
src_path = fs_dir / "bem" / f"{subject}-ico-5-src.fif"
bem_path = fs_dir / "bem" / f"{subject}-5120-5120-5120-bem-sol.fif"

src = mne.read_source_spaces(src_path)
bem = mne.read_bem_solution(bem_path)

# 5. Verify the alignment visually
fig = mne.viz.plot_alignment(
    raw.info,
    src=src,
    eeg=["original", "projected"],
    trans=trans,
    subject=subject,
    subjects_dir=subjects_dir,
    show_axes=True,
    mri_fiducials=True,
    dig="fiducials",
)

```

---

### Common Pitfalls to Check

* **Channel Name Mismatches:** If even a few channel names (like `T7` vs `T3`, or trailing periods) do not match the template montage dictionary, MNE will drop or misplace them, throwing off the layout.
* **Passing Identity Instead of `fsaverage`:** If you pass `trans=None` or an identity matrix, MNE won't apply the required rotation/translation to match the FreeSurfer template space, causing electrodes to float away from the head or sink deep into the cortex.

---

For a visual walkthrough of setting up coregistration and alignment workflows, you can check out this [MNE-Python Coregistration Tutorial](https://www.youtube.com/watch?v=ALV5qqMHLlQ).
