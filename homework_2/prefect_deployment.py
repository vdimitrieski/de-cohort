from prefect_flows_gcs import etl_parent_flow
from prefect_flows_bq import bq_etl_parent_flow
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule
from prefect.filesystems import GitHub

deployment_gcs = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="gcs_etl_deployment",
    version=1,
    work_queue_name="demo",
    # schedule=(CronSchedule(cron="0 5 1 * *", timezone="Etc/UTC"))
    # storage=GitHub.load("de-cohort-github-block")
)
deployment_gcs.apply()

deployment_bq = Deployment.build_from_flow(
    flow=bq_etl_parent_flow,
    name="bq_etl_deployment",
    version=1,
    work_queue_name="demo",
    # schedule=(CronSchedule(cron="0 5 1 * *", timezone="Etc/UTC"))
)
deployment_bq.apply()
