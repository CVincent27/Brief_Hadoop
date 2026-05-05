#!/usr/bin/env python3
import sys
import json

def mapper():
    for line in sys.stdin:
        try:
            data = json.loads(line)

            # ID station
            station_id = data.get("number")
            timestamp = data.get("last_update", 0)

            # Données vélo
            available_bikes = data.get("available_bikes", 0)
            available_bike_stands = data.get("available_bike_stands", 0)
            bike_stands = data.get("bike_stands", 0)
            status = data.get("status", "CLOSED")

            # LOAD FACTOR
            total = available_bikes + available_bike_stands
            load_factor = (
                available_bikes / total if total > 0 else 0.0
            )

            # STATUS VALIDE
            status_valide = 1 if (
                status == "OPEN"
                and 0 <= available_bikes <= bike_stands
            ) else 0

            # OUTPUT STRICT (TAB)
            print("{0}\t{1}\t{2:.3f}\t{3}".format(station_id, timestamp, load_factor, status_valide))

        except Exception:
            continue


if __name__ == "__main__":
    mapper()