from prefect import flow

@flow
def hello_world():
    name = "Prefect"
    print(f"Getting good at {name}")
    return

hello_world()
