#!/usr/bin/env python3
import sys
import math
from collections import defaultdict

def reducer():

    all_values = defaultdict(list)
    valid_values = defaultdict(list)

    total_samples = defaultdict(int)
    valid_samples = defaultdict(int)

    for line in sys.stdin:
        try:
            station_id, timestamp, load_factor, status_valide = line.strip().split("\t")

            load_factor = float(load_factor)
            status_valide = int(status_valide)

            # toujours compter
            total_samples[station_id] += 1
            all_values[station_id].append(load_factor)

            # seulement si valide
            if status_valide == 1:
                valid_samples[station_id] += 1
                valid_values[station_id].append(load_factor)

        except:
            continue

    for station_id in sorted(total_samples.keys()):

        vals_all = all_values[station_id]
        vals_valid = valid_values[station_id]

        # moyenne sur valides uniquement
        avg = sum(vals_valid) / len(vals_valid) if vals_valid else 0.0

        # std sur toutes les valeurs
        mean_all = sum(vals_all) / len(vals_all) if vals_all else 0.0
        std = math.sqrt(sum((x - mean_all) ** 2 for x in vals_all) / len(vals_all)) if vals_all else 0.0

        print(
            "{0}\t{1:.2f}\t{2:.2f}\t{3}/{4}".format(
                station_id,
                avg,
                std,
                valid_samples[station_id],
                total_samples[station_id]
            )
        )

if __name__ == "__main__":
    reducer()