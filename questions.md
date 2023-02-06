# Prefect questions and advanced topics

- how to extract chunks with prefect? parameterize with pagination?
  - first task to split the file? then to do extract data from each chunk and run task for each chunk?
- how to run some tasks in parallel? 
- how to do it in docker, not on local PC
  - how to configure and permanently store blocks/configs if it is run in Docker?
  - how to configure orion and agents in the docker?
- how to check if task has already been run?
  - should we make tasks idempotent? what if they are not?
- how to extract tasks into separate files in python?
- how to show graph of flow task dependencies?
  - to know what to expect to be executed in parallel
- how to do this with the Airflow tool?
