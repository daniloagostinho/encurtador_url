import os
import pika
import json

# Pegando as credenciais corretas das variáveis de ambiente
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "encurtador_queue")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "user")  # Certifique-se de que esse usuário existe
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "password")  # Senha correta

def start_consumer():
    """Inicia o consumidor para processar mensagens da fila."""

    # Configurar credenciais para RabbitMQ
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

    # Criar conexão com RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, credentials=credentials
    ))

    channel = connection.channel()

    channel.queue_declare(queue="access_logs", durable=True)

    def callback(ch, method, properties, body):
        log = json.loads(body)
        print(f"📌 Novo Log: {log}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue="access_logs", on_message_callback=callback)

    print("🟢 Consumidor de Logs rodando... Aguardando mensagens.")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
