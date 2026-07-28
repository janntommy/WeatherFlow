from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import substring

DIR = Path("data/raw/by_year")
BRONZE_DIR = Path("data/bronze")

my_schema = StructType([
    StructField("station_id", IntegerType),
    StructField("date", StringType),
    StructField("element", StringType(), nullable=False),
    StructField("value", IntegerType(), nullable=True),
    StructField("m_flag", StringType(), nullable=True),
    StructField("q_flag", StringType(), nullable=True),
    StructField("s_flag", StringType(), nullable=True),
    StructField("obs_time", StringType(), nullable=True),
])


def read_raw_csv_data(spark: SparkSession, dir: Path = DIR) -> DataFrame:
    df = (
        spark.read
        .option("header", "false")
        .schema(my_schema)
        .csv(str(dir / "*.csv.gz"))
    )
    return df


def add_year_col(df: DataFrame) -> DataFrame:
    return df.withColumn("year", substring("date", 1, 4))


def write_bronze(df: DataFrame, output_dir: Path = BRONZE_DIR) -> None:
    df.write.mode("overwrite").partitionBy("year").parquet(str(output_dir))