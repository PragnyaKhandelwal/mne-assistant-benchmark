This sign flip is a known property of `mean_flip`, and it usually has a clean fix.

**Why it happens**

With signed (fixed-orientation or `pick_ori="normal"`) estimates, `mean_flip` flips each vertex's sign relative to the label's dominant normal direction before averaging. That direction comes from an SVD, and its overall sign is arbitrary. So the output sign can differ from one participant to the next, depending on their cortical folding. The flip makes vertices within a label agree with each other, but it doesn't make the sign comparable across subjects.

If your stcs are free-orientation dSPM (the default, `pick_ori=None`), they are magnitude-only and always positive, so you wouldn't see this. Check that you are actually working with signed data.

**Options, roughly in order of preference**

1. **Morph to `fsaverage` first, then extract.** Use `mne.compute_source_morph` and `morph.apply(stc)`, then extract with the `fsaverage` source space and labels. Every subject then shares the same source space and normals, so `mean_flip` applies an identical flip vector to everyone. The sign is consistent across subjects, and you can average them safely.

2. **Use `mode="mean"` on a fixed-orientation stc.** The sign then has a fixed meaning (current pointing out of or into the cortex relative to the surface normal). The downside is that opposite-signed sources in sulci and gyri can cancel within the label.

3. **Drop the sign.** If polarity isn't what you care about, use free-orientation dSPM or a vector stc (`pick_ori="vector"`, then `.magnitude()`), or rectify or square the label time course. This avoids the problem, but the values are positively biased, so be careful comparing against baseline or interpreting small effects.

4. **Align signs post hoc.** Flip each subject's time course according to its correlation with a group template or a defined window. It works, but it is circular if you then test effects in that same window. Use an independent criterion, such as a localizer or a different condition, and report it.

I'd start with option 1. It is the least invasive and keeps the signed information. If you tell me your inverse settings (`loose`, `pick_ori`) and whether you morph before or after label extraction, I can check which case you're in.
