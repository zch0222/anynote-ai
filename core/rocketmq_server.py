import json

from rocketmq.client import Producer, Message
from core.config import ROCKETMQ_NAMESERVER_ADDRESS, ROCKETMQ_ACCESS_KEY, ROCKETMQ_ACCESS_SECRET


class RocketMQServer:

    def send(self, topic: str, tags: str, body: dict):
        print(topic, tags, body)
        producer = Producer('PID-XXX')
        producer.set_name_server_address(ROCKETMQ_NAMESERVER_ADDRESS)
        producer.set_session_credentials(
            ROCKETMQ_ACCESS_KEY,
            ROCKETMQ_ACCESS_SECRET,
            None
        )
        producer.start()

        msg = Message(topic)
        msg.set_keys(tags)
        msg.set_tags(tags)
        msg.set_body(json.dumps(body))
        ret = producer.send_sync(msg)
        print(ret.status, ret.msg_id, ret.offset)
        producer.shutdown()
