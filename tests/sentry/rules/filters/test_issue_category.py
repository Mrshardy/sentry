from sentry.eventstore.models import Event, GroupEvent
from sentry.issues.grouptype import GroupCategory
from sentry.rules.filters.issue_category import IssueCategoryFilter
from sentry.testutils import RuleTestCase, SnubaTestCase
from sentry.testutils.cases import PerformanceIssueTestCase
from sentry.testutils.performance_issues.store_transaction import PerfIssueTransactionTestMixin


class IssueCategoryFilterErrorTest(RuleTestCase):
    rule_cls = IssueCategoryFilter

    def test_valid_input_values(self):
        event = self.get_event()

        self.assertPasses(self.get_rule(data={"value": 1}), event)
        self.assertPasses(self.get_rule(data={"value": str(GroupCategory.ERROR.value)}), event)
        self.assertPasses(self.get_rule(data={"value": GroupCategory.ERROR.value}), event)

    def test_no_group_does_not_pass(self):
        event = self.get_event()
        event.group_id = None
        event.groups = None

        self.assertDoesNotPass(self.get_rule(data={"value": GroupCategory.ERROR.value}), event)

    def test_fail_on_invalid_data(self):
        event = self.get_event()
        data_cases = [
            {"value": None},
            {},
            {"value": GroupCategory.ERROR.name},
            {"value": "ERROR"},
            {"value": "error"},
        ]

        for data_case in data_cases:
            rule = self.get_rule(data=data_case)
            self.assertDoesNotPass(rule, event)

    def test_group_event(self):
        event: Event = self.get_event()
        group_event: GroupEvent = event.for_group(event.group)

        self.assertPasses(self.get_rule(data={"value": GroupCategory.ERROR.value}), event)
        self.assertPasses(self.get_rule(data={"value": GroupCategory.ERROR.value}), group_event)


class IssueCategoryFilterPerformanceTest(
    RuleTestCase,
    SnubaTestCase,
    PerfIssueTransactionTestMixin,
    PerformanceIssueTestCase,
):
    rule_cls = IssueCategoryFilter

    def test_transaction_category(self):
        tx_event = self.create_performance_issue()
        assert tx_event.group
        self.assertPasses(self.get_rule(data={"value": GroupCategory.PERFORMANCE.value}), tx_event)
