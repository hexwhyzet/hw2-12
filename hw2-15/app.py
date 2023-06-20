import string
from random import choices

import uvicorn as uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from temporalio.client import Client

from worker import TASK_QUEUE, CoursePurchaseWorkflow, WORKFLOW_NAME, CoursePurchaseWorkflowInput

app = FastAPI()


class RegisterPost(BaseModel):
    name: str
    card: str


@app.post("/register")
async def register(request: RegisterPost):
    client = await Client.connect("localhost:7233")
    workflow_id = "".join(
        choices(string.ascii_uppercase + string.digits, k=5)
    )
    await client.start_workflow(
        WORKFLOW_NAME, CoursePurchaseWorkflowInput(request.name, request.card), id=workflow_id,
        task_queue=TASK_QUEUE
    )
    return workflow_id


@app.get("/status/{workflow_id}")
async def register(workflow_id: str):
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(workflow_id)
    return await handle.query(CoursePurchaseWorkflow.get_status)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
