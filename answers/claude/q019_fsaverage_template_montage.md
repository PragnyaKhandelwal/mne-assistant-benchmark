For template-based EEG source localization without MRIs, the standard MNE approach is:

- **Montage:** a standard template montage (e.g. `standard_1005`, `standard_1020`, or a manufacturer-specific one like `biosemi64`) that matches your cap's channel names.
- **Transformation:** the built-in `trans='fsaverage'`. MNE ships a head-to-MRI transform for fsaverage that is meant to be paired with these standard montages. You don't need to compute one.

```python
import mne
from mne.datasets import fetch_fsaverage

fs_dir = fetch_fsaverage()          # downloads/locates fsaverage
subjects_dir = fs_dir.parent
subject = "fsaverage"

# raw = your mne.io.Raw / Epochs / Evoked
montage = mne.channels.make_standard_montage("standard_1005")
raw.set_montage(montage, match_case=False, on_missing="raise")

mne.viz.plot_alignment(
    raw.info,
    trans="fsaverage",              # built-in transform
    subject=subject,
    subjects_dir=subjects_dir,
    surfaces=["head-dense", "brain"],
    eeg=["original", "projected"],
    show_axes=True,
    dig=True,
)

src = mne.read_source_spaces(fs_dir / "bem" / "fsaverage-ico-5-src.fif")
bem = fs_dir / "bem" / "fsaverage-5120-5120-5120-bem-sol.fif"
fwd = mne.make_forward_solution(
    raw.info, trans="fsaverage", src=src, bem=bem, eeg=True, mindist=5.0
)
```

**If the alignment still looks off, check these common culprits:**

1. **Wrong montage for your cap.** If you applied a 10-20 montage to a cap with different electrode positions (e.g., an equidistant or 10-10 cap with custom names), the positions will be wrong. Use the montage that matches your hardware, or your actual digitized positions.

2. **Digitized or custom positions in the wrong frame or units.** If you loaded positions from a file (e.g., `read_custom_montage`), make sure they're in meters and that the coordinate frame is correct (`head`, or `unknown` with fiducials so MNE can convert it). Template coordinates in a different frame (e.g., raw MNI) won't work with `trans='fsaverage'`. If you have real digitization, don't use the fsaverage trans. Coregister it instead with `mne.gui.coregistration(subject="fsaverage", ...)` and scale the MRI to the head shape.

3. **Missing fiducials.** For custom montages, include nasion/LPA/RPA and set `coord_frame="head"`, since the head frame is defined by them.

4. **Channel name mismatches.** Case or naming differences (`FP1` vs `Fp1`, or old `T3/T4/T5/T6` vs `T7/T8/P7/P8`) can cause channels to be dropped or mis-assigned. Use `match_case=False`, or rename via `raw.rename_channels`. Also check `raw.info["dig"]` to confirm all EEG channels actually got positions.

5. **Interpreting the plot.** With `eeg="projected"`, electrodes are snapped to the scalp surface, whereas `"original"` shows raw montage positions. Small offsets are normal. Large systematic shifts (e.g., whole cap rotated or floating far from the head) point to a frame or montage problem.

If you tell me what the plot looks like (cap floating above, rotated, shifted forward) and where your electrode positions come from (cap model, custom file, or a standard montage name), I can narrow down the cause. I'd also confirm details against the 1.13 docs for the tutorial "Source localization with no MRI", since I can't verify anything specific to that release.
