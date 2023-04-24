from concurrent.futures import Future
from typing import Mapping, Optional, Sequence, Union

from arroyo import Message, Topic
from arroyo.backends.kafka import KafkaPayload, KafkaProducer, build_kafka_configuration
from django.conf import settings

from sentry.sentry_metrics.metrics_interface import GenericMetricsBackend
from sentry.sentry_metrics.use_case_id_registry import UseCaseID
from sentry.utils import json
from sentry.utils.kafka_config import get_kafka_producer_cluster_options


def build_mri(metric_name: str, type: str, use_case_id: UseCaseID, unit: Optional[str]) -> str:
    mri_unit = "none" if unit is None else unit
    return f"{type}:{use_case_id.value}/{metric_name}@{mri_unit}"


class KafkaMetricsBackend(GenericMetricsBackend):
    def __init__(self) -> None:

        self.kafka_topic = settings.KAFKA_INGEST_PERFORMANCE_METRICS

        cluster_name = settings.KAFKA_TOPICS[self.kafka_topic]["cluster"]
        producer_config = get_kafka_producer_cluster_options(cluster_name)
        self.producer = KafkaProducer(build_kafka_configuration(default_config=producer_config))

    def counter(
        self,
        use_case_id: UseCaseID,
        org_id: int,
        project_id: int,
        metric_name: str,
        value: Union[int, float],
        timestamp: int,
        tags: Mapping[str, str],
        unit: Optional[str] = None,
        retention_days: Optional[int] = 90,
    ) -> Future[Message[KafkaPayload]]:

        """
        Used for emitting a counter metric for internal use cases only.
        Ensure that the use_case_id passed in has been registered
        in the UseCaseID enum.
        """

        counter_metric = {
            "org_id": org_id,
            "project_id": project_id,
            "name": build_mri(metric_name, "c", use_case_id, unit),
            "value": value,
            "timestamp": timestamp,
            "tags": tags,
            "retention_days": retention_days,
        }

        payload = KafkaPayload(None, json.dumps(counter_metric).encode("utf-8"), [])
        future = self.producer.produce(Topic(self.kafka_topic), payload)

        return future

    def set(
        self,
        use_case_id: UseCaseID,
        org_id: int,
        project_id: int,
        metric_name: str,
        value: Sequence[int],
        timestamp: int,
        tags: Mapping[str, str],
        unit: Optional[str] = None,
        retention_days: Optional[int] = 90,
    ) -> Future[Message[KafkaPayload]]:

        """
        Used for emitting a set metric for internal use cases only. Can support
        a sequence of values. Ensure that the use_case_id passed in has
        been registered in the UseCaseID enum.
        """
        raise NotImplementedError()

    def distribution(
        self,
        use_case_id: UseCaseID,
        org_id: int,
        project_id: int,
        metric_name: str,
        value: Sequence[Union[int, float]],
        timestamp: int,
        tags: Mapping[str, str],
        unit: Optional[str] = None,
        retention_days: Optional[int] = 90,
    ) -> Future[Message[KafkaPayload]]:

        """
        Used for emitting a distribution metric for internal use cases only. Can
        support a sequence of values. Ensure that the use_case_id passed in
        has been registered in the UseCaseID enum.
        """
        raise NotImplementedError()
