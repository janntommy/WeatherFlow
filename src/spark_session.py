import os
import sys

from pyspark.sql import SparkSession


def get_spark_session() -> SparkSession:
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    spark = (
        SparkSession.builder
        .master("local")
        .appName("WeatherFlow")
        .config("spark.driver.memory", "4g")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("ERROR")
    return spark
