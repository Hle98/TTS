import csv
import numpy as np

def GetNames(filepath):
    with open(filepath,encoding="utf8") as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        candidates = list(csvReader)
        candidates.pop(0)
        candidates_array = np.array(candidates)
        return candidates_array

