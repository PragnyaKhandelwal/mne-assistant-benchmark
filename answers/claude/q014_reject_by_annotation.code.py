import numpy as np

data = raw.get_data(reject_by_annotation="omit")

variances = np.var(data, axis=1)
