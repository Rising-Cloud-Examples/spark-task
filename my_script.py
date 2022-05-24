import json
import random
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PiApproximator").getOrCreate()

request = {}
with open("request.json", 'r') as f:
    request = json.load(f)

NUM_SAMPLES = request["samples"]

def inside(p):
    x, y = random.random(), random.random()
    return x*x + y*y < 1

count = spark.sparkContext.parallelize(range(0, NUM_SAMPLES)) \
             .filter(inside).count()
response = {"pi": (4.0 * count / NUM_SAMPLES)}

with open("response.json", 'w+') as f:
    json.dump(response, f)
