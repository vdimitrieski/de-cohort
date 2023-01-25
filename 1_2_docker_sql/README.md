# Commands

- ```
  docker build -t de_test:pandas .
  ```
- ```
  docker run -it de_test:pandas 2021-01-15
  ```
- ```
  docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5432:5432 \
      postgres:15
  ```
- ```
  pgcli -h localhost -p 5432 -u root -d ny_taxi
  ```

- ```
  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
  ```

- ```
  gzip -d yellow_tripdata_2021-01.csv.gz
  ```

- https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

- ```
  jupyter notebook
  ```

- ```
  docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    dpage/pgadmin4
  ```

- ```
  docker network create pg-network

  docker run -it \
      -e POSTGRES_USER="root" \
      -e POSTGRES_PASSWORD="root" \
      -e POSTGRES_DB="ny_taxi" \
      -v ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5432:5432 \
      --network=pg-network \
      --name=pg-database \
      postgres:15

  docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
      --network=pg-network \
      --name=pg-admin \
    dpage/pgadmin4
  ```

- ```
  jupyter nbconvert --to=script ingesting\ yellow\ taxi.ipynb
  ```
- ```
  python pipeline.py --user 'root' --password 'root' --host 'localhost' --port 5432 --db 'ny_taxi' --table_name 'yellow_taxi_trips' --url 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
  ```
- ```
  docker build -t test_ingest:v001 .
  ```
- ```
  docker run -it --network=pg-network test_ingest:v001 --user 'root' --password 'root' --host 'pg-database' --port 5432 --db 'ny_taxi' --table_name 'yellow_taxi_trips' --url 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
  ```
- ```
  export GOOGLE_APPLICATION_CREDENTIALS="/home/vdimitrieski/projects/de_cohort_2023/de-cohort-e7ed22b3baef.json"
  ```