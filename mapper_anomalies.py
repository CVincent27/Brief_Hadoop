#!/usr/bin/env python3
import sys
import json
import time

# seuils
THRESHOLD_NO_UPDATE = 30 * 60      # 30 min en s
THRESHOLD_ZERO_BIKES = 2 * 60 * 60  # 2h en s

def mapper():

    current_time = int(time.time())

    for line in sys.stdin:
        try:
            data = json.loads(line)

            station_id = data.get("number", "unknown")
            status = data.get("status", "UNKNOWN")

            available_bikes = data.get("available_bikes", 0)
            bike_stands = data.get("bike_stands", 0)
            available_bike_stands = data.get("available_bike_stands", 0)

            last_update_ms = data.get("last_update", 0)
            last_update = int(last_update_ms / 1000)  # ms → s

            age_last_update = current_time - last_update

            # 1. ZERO_BIKES
            if status == "OPEN" and available_bikes == 0 and age_last_update > THRESHOLD_ZERO_BIKES:
                print("{0}\tZERO_BIKES\t{1}\t{2}".format(station_id, current_time, age_last_update))

            # 2. FULL_STANDS
            elif available_bike_stands == bike_stands:
                print("{0}\tFULL_STANDS\t{1}\t{2}".format(station_id, current_time, age_last_update))

            # 3. NO_UPDATE
            elif age_last_update > THRESHOLD_NO_UPDATE:
                print("{0}\tNO_UPDATE\t{1}\t{2}".format(station_id, current_time, age_last_update))

            # 4. OK
            else:
                print("{0}\tOK\t{1}\t{2}".format(station_id, current_time, age_last_update))

        except Exception:
            continue

if __name__ == "__main__":
    mapper()