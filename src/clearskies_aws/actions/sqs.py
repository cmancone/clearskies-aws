import boto3
import json
import datetime

from botocore.exceptions import ClientError
from clearskies.environment import Environment
from clearskies.models import Models
from collections.abc import Sequence
from collections import OrderedDict
from mypy_boto3_sqs import SQSClient
from typing import List, Optional, Callable

from ..di import StandardDependencies
from . import assume_role
from .action_aws import ActionAws
class SQS(ActionAws):
    def __init__(self, environment: Environment, boto3: boto3, di: StandardDependencies) -> None:
        """Setup action."""
        super().__init__(environment, boto3, di)

    def configure(
        self,
        queue_url: str = '',
        queue_url_environment_key: str = '',
        queue_url_callable: Optional[Callable] = None,
        message_callable: Optional[Callable] = None,
        when: Optional[Callable] = None,
        assume_role: Optional[assume_role.AssumeRole] = None,
    ) -> None:
        super().configure(message_callable=message_callable, when=when, assume_role=assume_role)

        self.queue_url = queue_url
        self.queue_url_environment_key = queue_url_environment_key
        self.queue_url_callable = queue_url_callable

        queue_urls = 0
        for value in [queue_url, queue_url_environment_key, queue_url_callable]:
            if value:
                queue_urls += 1
        if queue_urls > 1:
            raise ValueError(
                "You can only provide one of 'queue_url', 'queue_url_environment_key', or 'queue_url_callable', but more than one were provided."
            )
        if not queue_urls:
            raise ValueError(
                "You must provide at least one of 'queue_url', 'queue_url_environment_key', or 'queue_url_callable'."
            )

    def _execute_action(self, client, model) -> None:
        """Send a notification as configured."""
        try:
            client.send_message(
                QueueUrl=self.get_queue_url(model),
                MessageBody=self.get_message_body(model),
            )
        except ClientError as e:
            raise e

    def get_queue_url(self, model):
        if self.queue_url:
            return self.queue_url
        if self.queue_url_environment_key:
            return self.environment.get(self.queue_url_environment_key)
        return self.di.call_function(self.queue_url_callable, model=model)
