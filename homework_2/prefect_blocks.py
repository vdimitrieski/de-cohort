from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
import json

# alternative to creating GCP blocks in the UI
# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!
gcp_credentials_file = open('../service-account-private-key.json')
credentials_block = GcpCredentials(
    # enter your credentials info or use the file method.
    service_account_info=json.load(gcp_credentials_file)
)
credentials_block.save("de-cohort-gcp-credentials-block", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("de-cohort-gcp-credentials-block"),
    bucket="dtc_data_lake_de-cohort",  # insert your  GCS bucket name
)

bucket_block.save("de-cohort-gcs-bucket-block", overwrite=True)
