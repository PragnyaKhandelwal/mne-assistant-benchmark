In MNE-Python 1.13, the simplest way is to use the standard `standard_1020` montage and attach it to your existing `raw` object using `raw.set_montage()`.

```
import mne# Load the standard 10-20 electrode positionsmontage = mne.channels.make_standard_montage("standard_1020")# Apply positions directly to raw (in place)raw.set_montage(montage)
```

That's it. Your existing `raw` object is modified; you don't need to reassign it.

### Plot the electrode positions

```
raw.plot_sensors(show_names=True)
```

### Plot a topomap

For example, to plot EEG power:

```
spectrum = raw.compute_psd()spectrum.plot_topomap()
```

### Important: channel-name matching

MNE matches channel names case-sensitively by default. If your channels are named `FP1`, `FZ`, `CZ` rather than `Fp1`, `Fz`, `Cz`, use:

```
montage = mne.channels.make_standard_montage("standard_1020")raw.set_montage(montage, match_case=False)
```

If some channels aren't part of the standard montage, MNE will raise an error by default. You can inspect them with:

```
missing = set(raw.ch_names) - set(montage.ch_names)print(missing)
```

Note: These are template (idealized) electrode positions, not individually digitized positions. They're suitable for conventional topomap visualization, but may not exactly reflect the actual electrode placement.

Documentation: [MNE standard montages](https://mne.tools/stable/generated/mne.channels.make_standard_montage.html?utm_source=chatgpt.com) · [Raw.set_montage](https://mne.tools/stable/generated/mne.io.Raw.html?utm_source=chatgpt.com#mne.io.Raw.set_montage).&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub+2
