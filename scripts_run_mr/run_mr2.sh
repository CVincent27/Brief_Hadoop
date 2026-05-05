#!/bin/bash

set -e  # stop si erreur

CONTAINER="namenode"
HADOOP_STREAMING_JAR="/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"
OUTPUT="/output/anomalies_results"
INPUT="/input/velo_lyon.json"

echo "Suppression de l'ancien output..."
docker exec -it $CONTAINER hdfs dfs -rm -r -f $OUTPUT || true

echo "Copie du mapper dans le container..."
docker cp mapper_anomalies.py $CONTAINER:/mapper_anomalies.py
docker cp reducer_anomalies.py $CONTAINER:/reducer_anomalies.py

echo "Lancement du job Hadoop Streaming..."
docker exec -it $CONTAINER hadoop jar $HADOOP_STREAMING_JAR \
  -files /mapper_anomalies.py,/reducer_anomalies.py \
  -mapper "python3 mapper_anomalies.py" \
  -reducer "python3 reducer_anomalies.py" \
  -input $INPUT \
  -output $OUTPUT

echo "Résultats MR2 :"
docker exec -it $CONTAINER hdfs dfs -cat $OUTPUT/part-00000