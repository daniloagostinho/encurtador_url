import pika
import os
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def get_rabbitmq_connection():
    """Cria e retorna uma conexão com o RabbitMQ."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    return connection

def publish_message(queue_name, message):
    """Publica uma mensagem na fila especificada."""
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declara a fila (garante que ela exista)
    channel.queue_declare(queue=queue_name, durable=True)

    # Publica a mensagem convertida para JSON
    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Mensagem persistente
        ),
    )

    connection.close()
