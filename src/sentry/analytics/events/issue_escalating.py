from sentry import analytics


class IssueEscalatingEvent(analytics.Event):
    type = "issue.escalating"

    attributes = (
        analytics.Attribute("organization_id", type=int),
        analytics.Attribute("project_id", type=int),
        analytics.Attribute("group_id"),
        analytics.Attribute("event_id"),
    )


analytics.register(IssueEscalatingEvent)
