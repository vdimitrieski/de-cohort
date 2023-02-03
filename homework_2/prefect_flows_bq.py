from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3, log_prints=True)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("de-cohort-gcs-bucket-block")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task(log_prints=True)
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    return df


@task(retries=3, log_prints=True)
def write_bq(df: pd.DataFrame, color: str) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load(
        "de-cohort-gcp-credentials-block")

    df.to_gbq(
        destination_table=f"taxi_data.{color}",
        project_id="de-cohort",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(log_prints=True)
def etl_gcs_to_bq(year: int, month: int, color: str) -> int:
    """Main ETL flow to load data into Big Query"""

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df, color)
    return len(df)


@flow(log_prints=True)
def bq_etl_parent_flow(
    months: list[int] = [1], year: int = 2020, color: str = "green"
):
    count = 0
    for month in months:
        count += etl_gcs_to_bq(year, month, color)
    print(f"Total number of rows processed: {count}")


if __name__ == "__main__":
    color = "green"
    months = [1]
    year = 2020
    bq_etl_parent_flow(months, year, color)
