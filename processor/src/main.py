import json
import time
import pika
from config import settings
from processing import run_processing_flow

QUEUE_NAME = "wine_price_processor"


def callback(ch, method, properties, body):
    print(f" [x] Received event: {body.decode()}")
    # TODO Proceed only if new records were inserted (check event payload).
    try:
        inserted = run_processing_flow()
        
        # Publish finished event
        message = {
            "event": "wine.prices.processed",
            "averages_inserted": inserted,
        }
        
        ch.basic_publish(
            exchange=settings.rabbitmq_exchange,
            routing_key="wine.prices.averages.done",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
        print(f" [x] Published finished event: wine.prices.averages.done")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Error during processing: {e}")
        # In case of error, we can either re-queue or discard.
        # Discarding for now to avoid infinite loops in this exercise.
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    credentials = pika.PlainCredentials(
        settings.rabbitmq_user,
        settings.rabbitmq_password
    )
    
    # Wait for RabbitMQ to be ready
    max_retries = 10
    retry_delay = 5
    connection = None

    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.rabbitmq_host,
                    port=settings.rabbitmq_port,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            break
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready, retrying in {retry_delay}s (attempt {attempt + 1}/{max_retries})")
            time.sleep(retry_delay)

    if not connection:
        print("Could not connect to RabbitMQ. Exiting.")
        return

    channel = connection.channel()

    channel.exchange_declare(
        exchange=settings.rabbitmq_exchange,
        exchange_type="topic",
        durable=True,
    )

    # Use a persistent queue for the processor
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(
        exchange=settings.rabbitmq_exchange,
        queue=QUEUE_NAME,
        routing_key="wine.prices.done"
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        connection.close()

if __name__ == "__main__":
    main()
