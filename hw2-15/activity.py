import time
from dataclasses import dataclass

from temporalio import activity


@dataclass
class CreateApplicationInput:
    customer_name: str


@activity.defn(name="create_application")
async def create_application(inp: CreateApplicationInput) -> None:
    time.sleep(10)
    print("Application created")


@activity.defn(name="reserve_place")
async def reserve_place() -> None:
    time.sleep(10)
    print("Place reserved")


@dataclass
class ProcessPaymentInput:
    card_number: str


@activity.defn(name="process_payment")
async def process_payment(inp: ProcessPaymentInput) -> None:
    time.sleep(10)
    print("Payment processed")


@dataclass
class SendNotificationInput:
    content: str


@activity.defn(name="send_notification")
async def send_notification(inp: SendNotificationInput) -> None:
    time.sleep(10)
    print(inp.content)
