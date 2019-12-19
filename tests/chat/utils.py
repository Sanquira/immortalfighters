"""
Util methods for use in tests
"""

from channels.testing import WebsocketCommunicator


def is_valid_message(message) -> bool:
    """Checks if message has all basic fields"""
    return "type" in message and "time" in message


def is_valid_message_with_type(message, message_type: str) -> bool:
    """Checks if message has all basic fields and has specific type"""
    return is_valid_message(message) and message["type"] == message_type


def is_valid_error_message(message) -> bool:
    """Checks if message is valid error"""
    if not is_valid_message(message):
        return False

    return message["type"] == "error" and "error_type" in message


def is_error(message, expected_error: str) -> bool:
    """Checks if message is valid error of type"""
    return is_valid_error_message(message) and message["error_type"] == expected_error


async def next_message(communicator: WebsocketCommunicator):
    """Returns next message received from server"""
    return await communicator.receive_json_from()


async def next_message_of_type(communicator: WebsocketCommunicator, message_type: str, max_messages: int = -1):
    """Returns next message of specific type with max number of messages ignored"""
    incorrect_messages = 0
    while True:
        message = await communicator.receive_json_from()
        if not is_valid_message(message):
            raise TypeError("Invalid message received")

        if message["type"] == message_type:
            return message, incorrect_messages

        incorrect_messages = incorrect_messages + 1
        if 0 < max_messages <= incorrect_messages:
            raise TimeoutError("Didn't receive message of type %s in %d messages" % (message_type, incorrect_messages))


async def next_error(communicator: WebsocketCommunicator, max_messages: int = -1):
    """Returns next error"""
    return await next_message_of_type(communicator, "error", max_messages)


async def ignore_messages(communicator: WebsocketCommunicator, num_of_messages: int):
    """Ignore certain number of messages"""
    for _ in range(num_of_messages):
        await communicator.receive_from()
