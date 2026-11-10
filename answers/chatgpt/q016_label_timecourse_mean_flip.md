This is a fairly common issue when extracting cortical source time courses with MNE-Python, and the important point is that you should not simply take the absolute value of the estimates or flip the signs of participants to make them agree. First, you need to determine why the signs differ.

Your use of:

```
mne.extract_label_time_course(    stc, labels, src,    mode="mean_flip")
```

is already doing something important: `mean_flip` attempts to correct for differences in cortical surface orientation within each label. However, it does not necessarily resolve sign differences between participants.

There are a few things to check.

## 1. Understand what `mean_flip` actually does

A cortical source estimate has a sign because the estimated current is oriented relative to the source-space orientation.

Within a label, different vertices can have different surface-normal orientations. Simply averaging their time courses can cause cancellation.

`mean_flip` addresses this by:

- Identifying the vertex with the strongest activity in the label.
- Using its orientation as a reference.
- Flipping the signs of other vertices as needed before averaging.

This helps prevent cancellation within a label.

However, it does not guarantee that the resulting label time course has the same sign across participants.

For example:

| Participant | Label time course |
| ----------- | ----------------- |
| Subject 1   | +2.1              |
| Subject 2   | -1.8              |
| Subject 3   | +2.4              |
| Subject 4   | -2.0              |

This could happen if the anatomical surface orientations or source-space configurations differ between participants.

A small but important correction: MNE's `mean_flip` does not use the strongest-activity vertex as its reference. It estimates the dominant direction of the source-space normal vectors using SVD and flips vertices whose normals point in the opposite direction. This is a geometrical orientation correction, not an alignment of functional responses across participants.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+1



## 2. Check whether your source orientations are consistent across participants

This is where I would start.

In particular, check how you computed your inverse solutions:

- Did you use `loose=0.2` or `loose=0`?
- Did you use `pick_ori="normal"`?
- Did you use the same template source space for all participants?
- Did you morph all source estimates to a common brain, such as `fsaverage`?

For group-level signed cortical time courses, a good approach is to use a consistent cortical orientation convention.

For example, if you want signed estimates along the cortical surface normal, consider:

```
stc = mne.minimum_norm.apply_inverse(    evoked,    inverse_operator,    lambda2=lambda2,    method="dSPM",    pick_ori="normal")
```

Then morph the resulting estimates to a common surface:

```
morph = mne.compute_source_morph(    stc,    subject=subject,    subject_from=subject,    subject_to="fsaverage",    subjects_dir=subjects_dir)stc_fsaverage = morph.apply(stc)
```

Use the same template labels and source space for extracting time courses from all participants.

Important: Morphing alone does not guarantee correct polarity. You still need consistent orientation conventions when computing the inverse solutions.

## 3. Consider using `pca_flip`

MNE also offers another extraction method:

```
label_tc = mne.extract_label_time_course(    stc,    labels,    src,    mode="pca_flip")
```

This performs PCA within each label and uses the first principal component as its representative time course.

The sign is adjusted using the source-space orientation information.

It can be useful when:

- Activity is spatially heterogeneous within a label.
- A simple mean is not representative.
- You want a more robust summary of the dominant temporal pattern.

However, `pca_flip` is not a guaranteed solution to intersubject polarity differences. It does not replace consistent source orientation conventions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1



## 4. Decide whether polarity or activation magnitude is your scientific question

This is probably the most important methodological decision.

There are two different situations:

A. You care about activation magnitude, not polarity.

For example, you want to know whether a particular cortical region responds more strongly to a stimulus, regardless of whether the estimated current is positive or negative.

You could use an unsigned measure:

```
label_tc = mne.extract_label_time_course(    stc,    labels,    src,    mode="mean")
```

But be careful: `mean` does not take absolute values. If you want mean absolute amplitude, you must explicitly calculate it:

```
label_tc_abs = np.mean(    np.abs(stc.data[label_vertex_indices]),    axis=0)
```

This changes the scientific quantity being measured.

B. You care about the polarity of cortical currents.

For example, you want to compare the polarity and latency of an N100 component across participants.

In this case, you should preserve the sign. Do not take absolute values.

Instead, investigate whether the orientation convention is consistent across subjects and whether the observed polarity differences are physiologically meaningful.

## 5. What I would recommend for your analysis

For a typical group-level dSPM analysis involving cortical ROIs, my recommended workflow would be:

1. Compute individual dSPM estimates

   Use a consistent inverse solution configuration and cortical orientation convention.
2. Morph all estimates to fsaverage

   Use the same target source space for every participant.
3. Use identical labels

   Extract the same anatomical ROIs from the common template.
4. Extract signed time courses

   Start with `mode="mean_flip"` and compare with `mode="pca_flip"`.
5. Inspect individual participant waveforms

   Check whether polarity differences are systematic or genuinely reflect differences in cortical responses.
6. Perform group averaging

   Only after establishing that the sign convention is consistent.

## 6. One important diagnostic question

I would particularly like to know how you computed your dSPM estimates, because this can change the answer substantially.

Which of these did you use when calling `apply_inverse()`?

1\. Source orientation (`pick_ori`)

`pick_ori="normal"`

`pick_ori=None` (default)

`pick_ori="vector"`

Something else / not sure

2\. Inverse orientation constraint (`loose`)

`loose=0`

`loose=0.2`

`loose=1`

Other / not sure

3\. Did you morph estimates to a common brain?

Yes, to fsaverage

No, using individual source spaces

Another template / not sure

Submit

With these three details, I can help identify whether your sign differences are caused by source orientation, label extraction, or genuine intersubject differences—and recommend the appropriate group-level procedure without artificially changing the polarity of your data.
