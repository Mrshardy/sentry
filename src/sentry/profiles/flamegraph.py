from datetime import datetime
from typing import Dict, List

from snuba_sdk import Column, Condition, Entity, Op, Query, Request

from sentry.snuba.dataset import Dataset, EntityKey
from sentry.snuba.referrer import Referrer
from sentry.utils.snuba import raw_snql_query

MAX_RETENTION_DAYS = 90


def get_profiles_id(
    organization_id: int,
    project_id: int,
    transaction_name: str,
    start: datetime,
    end: datetime,
) -> Dict[str, List[str]]:
    query = Query(
        match=Entity(EntityKey.Profiles.value),
        select=[
            Column("profile_id"),
        ],
        where=[
            Condition(Column("organization_id"), Op.EQ, organization_id),
            Condition(Column("project_id"), Op.EQ, project_id),
            Condition(Column("transaction_name"), Op.EQ, transaction_name),
            Condition(Column("received"), Op.GTE, start),
            Condition(Column("received"), Op.LT, end),
        ],
    ).set_limit(100)
    request = Request(
        dataset=Dataset.Profiles.value,
        app_id="default",
        query=query,
        tenant_ids={
            "referrer": Referrer.API_PROFILING_PROFILE_SUMMARY_TABLE.value,
            "organization_id": 8,
        },
    )
    data = raw_snql_query(
        request,
        referrer=Referrer.API_PROFILING_PROFILE_SUMMARY_TABLE.value,
    )["data"]
    return {"profiles_id": [row["profile_id"] for row in data]}
