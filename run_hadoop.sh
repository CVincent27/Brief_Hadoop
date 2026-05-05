#!/bin/bash

set -e  # stop si erreur

CONTAINER="namenode"
HADOOP_STREAMING_JAR="/opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar"
OUTPUT="/output/load_factor_results"
INPUT="/input/velo_lyon.json"

echo "Suppression de l'ancien output..."
docker exec -it $CONTAINER hdfs dfs -rm -r -f $OUTPUT || true

echo "Copie des scripts dans le container..."
docker cp mapper_load_factor.py $CONTAINER:/mapper_load_factor.py
docker cp reducer_load_factor.py $CONTAINER:/reducer_load_factor.py

echo "Lancement du job Hadoop Streaming..."
docker exec -it $CONTAINER hadoop jar $HADOOP_STREAMING_JAR \
  -files /mapper_load_factor.py,/reducer_load_factor.py \
  -mapper "python3 mapper_load_factor.py" \
  -reducer "python3 reducer_load_factor.py" \
  -input $INPUT \
  -output $OUTPUT

echo "Résultats :"
docker exec -it $CONTAINER hdfs dfs -cat $OUTPUT/part-00000