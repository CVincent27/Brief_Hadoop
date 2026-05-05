#!/usr/bin/env python3
import sys
from collections import defaultdict

def reducer():
    total_counts = defaultdict(int)
    anomaly_counts = defaultdict(int)
    last_anomaly = {}

    for line in sys.stdin:
        try:
            station_id, anomaly_type, timestamp, age = line.strip().split("\t")
            timestamp = int(timestamp)

            # total samples
            total_counts[station_id] += 1

            # anomalies
            if anomaly_type != "OK":
                anomaly_counts[station_id] += 1

                # dernière anomalie (timestamp max)
                if (station_id not in last_anomaly) or (timestamp > last_anomaly[station_id][0]):
                    last_anomaly[station_id] = (timestamp, anomaly_type)

        except:
            continue

    # OUTPUT
    for station_id in sorted(total_counts.keys()):
        total = total_counts[station_id]
        anomalies = anomaly_counts[station_id]

        if total > 0:
            fiabilite = ((total - anomalies) / total) * 100
        else:
            fiabilite = 0.0

        # dernière panne
        if station_id in last_anomaly:
            derniere_panne = last_anomaly[station_id][1]
        else:
            derniere_panne = "NONE"

        print("{0}\t{1:.0f}%\t{2}\t{3}".format(
            station_id,
            fiabilite,
            anomalies,
            derniere_panne
        ))

if __name__ == "__main__":
    reducer()