For BioSemi `.bdf` files, the `Status` channel usually contains event trigger codes encoded as integers. In MNE-Python, the recommended approach is to read the BDF file with `stim_channel='auto'` and extract events using `mne.find_events()`.

There is one important detail: BioSemi stores trigger codes in the lower 16 bits of the Status channel, while the upper bits can contain system information (such as CMS status). You may need to mask the trigger values to obtain the correct event codes.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

MNE 1.13.2 documentation+1



## 1. Read the BDF file correctly

```
import mne# Read BDF fileraw = mne.io.read_raw_bdf(    'your_file.bdf',    preload=True,    stim_channel='auto')# Check channel names and typesprint(raw.ch_names)print(raw.get_channel_types())
```

MNE automatically recognizes channels named `Status` or `Trigger` (case-insensitive) as stimulus channels.

## 2. Extract events from the Status channel

```
# Extract events, keeping only the lower 16 bitsevents = mne.find_events(    raw,    stim_channel='Status',    output='onset',    consecutive='increasing',    mask=2**16 - 1,    mask_type='and',    uint_cast=True)print(events[:10])
```

The resulting `events` array has three columns:

| Column | Meaning                 |
| ------ | ----------------------- |
| 0      | Event sample number     |
| 1      | Previous stimulus value |
| 2      | Event trigger code      |

## 3. Inspect the event codes

```
import numpy as np# Print unique event codes and their frequenciesevent_codes, counts = np.unique(events[:, 2], return_counts=True)for code, count in zip(event_codes, counts):    print(f'Event code: {code}, Count: {count}')
```

You can also visualize the event distribution:

```
mne.viz.plot_events(    events,    sfreq=raw.info['sfreq'])
```

## 4. Create an event dictionary

Suppose your experiment uses the following trigger codes:

```
event_id = {    'Condition_1': 1,    'Condition_2': 2,    'Condition_3': 3,    'Condition_4': 4}
```

You can then create epochs:

```
epochs = mne.Epochs(    raw,    events,    event_id=event_id,    tmin=-0.2,    tmax=0.5,    baseline=(-0.2, 0),    preload=True)
```

## 5. Important: BDF Status channel versus BDF annotations

These are two different things:

- Status channel: Contains numerical trigger codes. Use `mne.find_events()`.
- BDF annotations: Contains textual event descriptions stored in the BDF annotation channel. MNE generally reads these into `raw.annotations`. Use `mne.events_from_annotations()` to extract events from them.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://mne.tools\&sz=32)

  MNE 1.13.2 documentation



If you have both, inspect them separately to avoid missing events or counting the same experimental events twice.

## My recommendation

For a typical BioSemi EEG dataset, start with:

```
raw = mne.io.read_raw_bdf(    'your_file.bdf',    preload=True,    stim_channel='auto')events = mne.find_events(    raw,    stim_channel='Status',    mask=65535,    mask_type='and',    uint_cast=True)
```

One question: Are you using a BioSemi ActiveTwo system (e.g., 32-, 64-, or 128-channel EEG)?

This matters because BioSemi encodes trigger information in the Status channel, and occasionally the trigger values need additional bit shifting depending on the external trigger hardware.
