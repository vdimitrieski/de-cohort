### Setting up the virtual environment

```
python3 -m venv prefect-env
```

```
source prefect-env/bin/activate
```

### Register blocks

```
prefect block register -f blocks/make_gcp_blocks.py
```

### Run agents

```
prefect agent start -q demo
```
