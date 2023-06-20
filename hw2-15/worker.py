from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import FailureError

from activity import create_application, CreateApplicationInput, change_status, ChangeStatusInput, Status, \
    send_notification, SendNotificationInput, process_payment, ProcessPaymentInput

DEFAULT_TIMEOUT = timedelta(seconds=10)
DEFAULT_RETRY_POLICY = RetryPolicy(
    initial_interval=timedelta(seconds=1)
)


@workflow.defn(name="CoursePurchase")
class CoursePurchase:
    @workflow.run
    async def run(self, customer_name: str, card_number: str) -> str:
        try:
            await workflow.execute_activity(
                create_application,
                CreateApplicationInput(customer_name=customer_name),
                start_to_close_timeout=DEFAULT_TIMEOUT,
            )
        except FailureError as e:
            await workflow.execute_activity(
                change_status,
                ChangeStatusInput(new_status=Status.fail_course),
                retry_policy=DEFAULT_RETRY_POLICY,
            )
            await workflow.execute_activity(
                send_notification,
                SendNotificationInput(content=f"Failed to get place in course: {e}"),
                retry_policy=DEFAULT_RETRY_POLICY,
            )
        await workflow.execute_activity(
            change_status,
            ChangeStatusInput(new_status=Status.ok_course),
            retry_policy=DEFAULT_RETRY_POLICY,
        )
        try:
            await workflow.execute_activity(
                process_payment,
                ProcessPaymentInput(card_number=card_number),
                start_to_close_timeout=DEFAULT_TIMEOUT,
            )
        except FailureError as e:
            await workflow.execute_activity(
                change_status,
                ChangeStatusInput(new_status=Status.fail_payment),
                retry_policy=DEFAULT_RETRY_POLICY,
            )
            await workflow.execute_activity(
                send_notification,
                SendNotificationInput(content=f"Failed to pay for course: {e}"),
                retry_policy=DEFAULT_RETRY_POLICY,
            )
        await workflow.execute_activity(
            change_status,
            ChangeStatusInput(new_status=Status.ok_payment),
            retry_policy=DEFAULT_RETRY_POLICY,
        )
        await workflow.execute_activity(
            send_notification,
            SendNotificationInput(content="Success!"),
            retry_policy=DEFAULT_RETRY_POLICY,
        )
