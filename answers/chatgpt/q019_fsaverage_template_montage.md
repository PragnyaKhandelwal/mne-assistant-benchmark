If you don't have individual MRIs, using `fsaverage` with a standard EEG montage is a reasonable approach for EEG source localization in MNE-Python. However, the important distinction is that the electrode montage and the head-to-MRI transformation are two separate things.

The most common reason electrodes appear displaced from the template head is that the electrode coordinates are being plotted in the wrong coordinate frame, or that the head-to-MRI transformation has not been properly established.

You should use:

1. A standard montage that matches your EEG cap.
2. The `fsaverage` template as your anatomical subject.
3. A head-to-MRI transformation that aligns the electrode coordinate system with the `fsaverage` anatomy.

## 1. Recommended montage and transformation

For a conventional 10–20 or 10–10 EEG system, I recommend:

| Setting            | Recommendation                                     |
| ------------------ | -------------------------------------------------- |
| Anatomical subject | `fsaverage`                                        |
| Montage            | `standard_1005` (or the montage matching your cap) |
| Transformation     | `trans='fsaverage'`                                |
| Source space       | `fsaverage-ico-5-src.fif`                          |
| BEM                | `fsaverage-5120-5120-5120-bem-sol.fif`             |

Why `standard_1005`? It provides a denser set of standard electrode positions, so it is useful even if your actual cap has fewer electrodes. You should only use positions corresponding to electrodes actually present in your recording.

Important: MNE's built-in `fsaverage` transformation is specifically intended for this template-MRI workflow. You generally do not need to manually calculate a transformation or run individual MRI coregistration when using the corresponding standard montage.

This is the approach demonstrated in MNE's official EEG-without-MRI tutorial.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.3.1 documentation+1



## 2. Working example for MNE-Python 1.13

Try the following workflow:

```
import os.path as opimport mnefrom mne.datasets import fetch_fsaverage# Download fsaveragefs_dir = fetch_fsaverage(verbose=True)subjects_dir = op.dirname(fs_dir)subject = "fsaverage"# Template transformationtrans = "fsaverage"# Source spacesrc = op.join(    fs_dir, "bem", "fsaverage-ico-5-src.fif")# BEM solutionbem = op.join(    fs_dir, "bem",    "fsaverage-5120-5120-5120-bem-sol.fif")# Load your EEG dataraw = mne.io.read_raw_fif("your_data_raw.fif", preload=True)# Standardize channel names if necessary# Make sure they match the montage names.# Set the standard montagemontage = mne.channels.make_standard_montage(    "standard_1005")
```

The key line is:

```
trans = "fsaverage"
```

Do not replace it with `trans=None` or an arbitrary identity transformation.

## 3. Understanding the electrode alignment plot

Pay attention to these two options:

```
eeg=["original", "projected"]
```

- `original`: shows the original standard electrode coordinates.
- `projected`: shows the electrode positions projected onto the scalp surface.

[EEG forward operator with a template MRI — MNE 1.13.0.dev240+gf60019e31 documentation](https://images.openai.com/static-rsc-4/jmI3BzC5ufMuwnHmgrRaq7kZIc8TYP3t1qSMwx1ZOLv6P04K7IUUmSDwgAw0vJguRLo5wweNOCXLshvedzzwU97AR2I9YQ_LXIFWdGrf2voEJKAURgLs3d64axUxl9uOkvi9zA0cRkMHc5ojhVP07p_gMawueUZ_dx3BqezkgWg?purpose=inline)

[mne.tools](https://mne.tools/dev/auto_tutorials/forward/35_eeg_no_mri.html?utm_source=chatgpt.com)

The projected positions should lie on the scalp surface. Small differences between original and projected positions are normal.

If the electrodes are substantially displaced, check the following:

1. Channel names: `Fp1`, `Fp2`, `Fz`, `Cz`, etc., must match the montage labels.
2. Montage selection: Make sure the montage corresponds to your actual electrode system.
3. Coordinate frame: Do not mix digitized head-coordinate positions with standard montage positions in MNI coordinates.
4. Transformation: Use `trans="fsaverage"` when using the standard MNE template workflow.

## 4. Compute the forward solution

Once the alignment looks reasonable, you can calculate the forward model:

```
fwd = mne.make_forward_solution(    raw.info,    trans=trans,    src=src,    bem=bem,    eeg=True,    mindist=5.0,    n_jobs=None)print(fwd)
```

You should see something similar to:

```
MRI -> head transform : ... fsaverage-trans.fif
Measurement data      : instance of Info
Conductor model       : ... fsaverage-5120-5120-5120-bem-sol.fif
```

## 5. One important scientific limitation

Using `fsaverage` does not mean that you have accurately coregistered each participant's electrodes to their individual anatomy.

Without individual MRIs or digitized electrode positions, you are assuming that:

- Participants have approximately average head anatomy.
- Their electrode positions correspond to the standard montage.
- The template transformation is a reasonable approximation.

MNE explicitly cautions that source estimates without individual MRIs can have localization errors of several centimeters. This matters particularly when interpreting individual participants' source locations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.3.1 documentation+1



## One question that would help me diagnose your alignment problem

Which EEG electrode system are you using?

- 10–20 (19–21 electrodes)
- 10–10 (32–64 electrodes)
- 10–5 (128–256 electrodes)
- BioSemi
- Brain Products actiCAP
- Other

Also, are you using only the standard electrode positions, or do you have digitized electrode coordinates?

With those details, I can recommend the correct montage and transformation for your setup and help identify why your electrodes are not aligning with the `fsaverage` head.
