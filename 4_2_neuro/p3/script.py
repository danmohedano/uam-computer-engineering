import numpy as np
import pandas as pd


def subsample(x, y):
    old_classes = []
    min_n = np.inf
    for c in np.unique(y):
        class_data = x[(y == c)]
        old_classes.append(class_data)
        if len(class_data) < min_n:
            min_n = len(class_data)

    classes = []
    for i in range(len(old_classes)):
        np.random.shuffle(old_classes[i])
        classes.append(old_classes[:min_n])

    classes = np.concatenate(classes)
    for i in range(len(classes)):
        stats_x = pd.DataFrame(old_classes[i])
        stats_sub_x = pd.DataFrame(classes[i])
        print(f"Old Class {i} Mean: {stats_x.mean:.4f} Std: {stats_x.std:.4f}")
        print(f"New Class {i} Mean: {stats_sub_x.mean:.4f} Std: {stats_sub_x.std:.4f}")
    return np.random.shuffle(classes)


