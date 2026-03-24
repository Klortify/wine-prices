import time
import json
import pika

from config import settings

credentials = pika.PlainCredentials(
    settings.rabbitmq_user,
    settings.rabbitmq_password,
)

def publish_done_event(count: int):
    max_retries = 3
    retry_delay = 5
    connection = None

    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.rabbitmq_host,
                    port=settings.rabbitmq_port,
                    credentials=credentials,
                    connection_attempts=max_retries,
                    retry_delay=retry_delay
                )
            )
            break
        except pika.exceptions.AMQPConnectionError:
            if attempt < max_retries - 1:
                print(f"RabbitMQ not ready, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
            else:
                raise

    if not connection:
        raise pika.exceptions.AMQPConnectionError("Could not connect to RabbitMQ")

    channel = connection.channel()

    channel.exchange_declare(
        exchange=settings.rabbitmq_exchange,
        exchange_type="topic",
        durable=True,
    )

    message = {
        "event": "wine.prices.collected",
        "rows_inserted": count,
    }

    channel.basic_publish(
        exchange=settings.rabbitmq_exchange,
        routing_key="wine.prices.done",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )

    connection.close()