from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
import os


@task(retries=3, log_prints=True)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    print('pre:task fetch')
    df = pd.read_csv(dataset_url)
    print('post:task fetch')
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Fix dtype issues"""
    print('pre:task clean')
    print(df.head(2))
    if 'lpep_pickup_datetime' in df.columns:
        df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
    if 'lpep_dropoff_datetime' in df.columns:
        df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
    if 'tpep_pickup_datetime' in df.columns:
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    if 'tpep_dropoff_datetime' in df.columns:
        df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    print('post:task clean')
    return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    print('pre:task write local')
    data_dir_path = Path(f"data/{color}")
    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)
    file_path = Path(f"{data_dir_path}/{dataset_file}.parquet")
    df.to_parquet(file_path, compression="gzip")
    print('post:task write local')
    return file_path


@task(retries=3, log_prints=True)
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    print('pre:task write gcs')
    gcs_block = GcsBucket.load("de-cohort-gcs-bucket-block")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    print('post:task write gcs')
    return


@flow(log_prints=True)
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    print('pre:flow etl_web_to_gcs')
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)
    print('post:flow etl_web_to_gcs')


@flow(log_prints=True)
def etl_parent_flow(
    months: list[int] = [1], year: int = 2020, color: str = "green"
):
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__ == "__main__":
    color = "green"
    months = [11]
    year = 2020
    etl_parent_flow(months, year, color)
