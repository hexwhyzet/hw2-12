import asyncio
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum

from temporalio import workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy
from temporalio.exceptions import FailureError
from temporalio.worker import Worker

from activity import create_application, CreateApplicationInput, send_notification, \
    SendNotificationInput, process_payment, ProcessPaymentInput

DEFAULT_TIMEOUT = timedelta(seconds=30)
DEFAULT_RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1)
)
TASK_QUEUE = "course-purchase-queue"
WORKFLOW_NAME = "CoursePurchase"


class Status(str, Enum):
    new = "new"
    fail_course = "fail_course"
    ok_course = "ok_course"
    fail_payment = "fail_payment"
    ok_payment = "ok_payment"


@dataclass
class CoursePurchaseWorkflowInput:
    customer_name: str
    card_number: str


@workflow.defn(name=WORKFLOW_NAME)
class CoursePurchaseWorkflow:
    status: Status = Status.new

    @workflow.run
    async def run(self, inp: CoursePurchaseWorkflowInput) -> None:
        try:
            await workflow.execute_activity(
                create_application,
                CreateApplicationInput(customer_name=inp.customer_name),
                start_to_close_timeout=DEFAULT_TIMEOUT,
            )
            self.status = Status.ok_course
        except FailureError as e:
            await workflow.execute_activity(
                send_notification,
                SendNotificationInput(content=f"Failed to get place in course: {e}"),
                retry_policy=DEFAULT_RETRY_POLICY,
                start_to_close_timeout=DEFAULT_TIMEOUT,
            )
            self.status = Status.fail_course
            return
        try:
            await workflow.execute_activity(
                process_payment,
                ProcessPaymentInput(card_number=inp.card_number),
                start_to_close_timeout=DEFAULT_TIMEOUT,
            )
            self.status = Status.ok_payment
        except FailureError as e:
            await workflow.execute_activity(
                send_notification,
                SendNotificationInput(content=f"Failed to pay for course: {e}"),
                retry_policy=DEFAULT_RETRY_POLICY,
                start_to_close_timeout=DEFAULT_TIMEOUT,
            )
            self.status = Status.fail_payment
            return
        await workflow.execute_activity(
            send_notification,
            SendNotificationInput(content="Success!"),
            retry_policy=DEFAULT_RETRY_POLICY,
            start_to_close_timeout=DEFAULT_TIMEOUT,
        )

    @workflow.query
    def get_status(self) -> str:
        return self.status.value


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[CoursePurchaseWorkflow],
        activities=[create_application, process_payment, send_notification]
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
