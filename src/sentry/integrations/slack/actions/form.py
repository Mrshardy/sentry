from __future__ import annotations

import logging
from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from sentry.integrations.slack.utils import (
    SLACK_RATE_LIMITED_MESSAGE,
    strip_channel_name,
    validate_channel_id,
)
from sentry.models import Integration
from sentry.shared_integrations.exceptions import ApiRateLimitedError, DuplicateDisplayNameError

logger = logging.getLogger("sentry.rules")


class SlackNotifyServiceForm(forms.Form):
    workspace = forms.ChoiceField(choices=(), widget=forms.Select())
    channel = forms.CharField(widget=forms.TextInput())
    channel_id = forms.CharField(required=False, widget=forms.TextInput())
    tags = forms.CharField(required=False, widget=forms.TextInput())

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # NOTE: Workspace maps directly to the integration ID
        workspace_list = [(i.id, i.name) for i in kwargs.pop("integrations")]
        self.channel_transformer = kwargs.pop("channel_transformer")

        super().__init__(*args, **kwargs)

        if workspace_list:
            self.fields["workspace"].initial = workspace_list[0][0]

        # https://github.com/typeddjango/django-stubs/issues/1208
        self.fields["workspace"].choices = workspace_list  # type: ignore[attr-defined]
        self.fields["workspace"].widget.choices = self.fields["workspace"].choices  # type: ignore[attr-defined]

        # XXX(meredith): When this gets set to True, it lets the RuleSerializer
        # know to only save if and when we have the channel_id. The rule will get saved
        # in the task (integrations/slack/tasks.py) if the channel_id is found.
        self._pending_save = False

    def _format_slack_error_message(self, message: str) -> Any:
        return _(f"Slack: {message}")

    def clean(self) -> dict[str, Any] | None:
        channel_id = (
            self.data.get("inputChannelId")
            or self.data.get("input_channel_id")
            or self.data.get("channel_id")
        )
        if channel_id:
            logger.info(
                "rule.slack.provide_channel_id",
                extra={
                    "slack_integration_id": self.data.get("workspace"),
                    "channel_id": self.data.get("channel_id"),
                },
            )
            if not self.data.get("channel"):
                raise forms.ValidationError(
                    self._format_slack_error_message("Channel name is a required field."),
                    code="invalid",
                )
            # default to "#" if they have the channel name without the prefix
            channel_prefix = self.data["channel"][0] if self.data["channel"][0] == "@" else "#"

        cleaned_data = super().clean()
        assert cleaned_data is not None

        workspace = cleaned_data.get("workspace")

        if channel_id:
            try:
                validate_channel_id(
                    self.data["channel"],
                    integration_id=workspace,
                    input_channel_id=channel_id,
                )
            except ValidationError as e:
                params = {"channel": self.data.get("channel"), "channel_id": channel_id}
                raise forms.ValidationError(
                    # ValidationErrors contain a list of error messages, not just one.
                    self._format_slack_error_message("; ".join(e.messages)),
                    code="invalid",
                    params=params,
                )
        try:
            integration = Integration.objects.get(id=workspace)
        except Integration.DoesNotExist:
            raise forms.ValidationError(
                self._format_slack_error_message("Workspace is a required field."),
                code="invalid",
            )

        channel = cleaned_data.get("channel", "")
        timed_out = False
        channel_prefix = ""

        # XXX(meredith): If the user is creating/updating a rule via the API and provides
        # the channel_id in the request, we don't need to call the channel_transformer - we
        # are assuming that they passed in the correct channel_id for the channel
        if not channel_id:
            try:
                channel_prefix, channel_id, timed_out = self.channel_transformer(
                    integration, channel
                )
            except DuplicateDisplayNameError:
                domain = integration.metadata["domain_name"]

                params = {"channel": channel, "domain": domain}

                raise forms.ValidationError(
                    self._format_slack_error_message(
                        "Multiple users were found with display name '%(channel)s'. "
                        "Please use your username, found at %(domain)s/account/settings#username."
                    ),
                    code="invalid",
                    params=params,
                )
            except ApiRateLimitedError:
                raise forms.ValidationError(
                    self._format_slack_error_message(SLACK_RATE_LIMITED_MESSAGE),
                    code="invalid",
                )

        channel = strip_channel_name(channel)
        if channel_id is None and timed_out:
            cleaned_data["channel"] = channel_prefix + channel
            self._pending_save = True
            return cleaned_data

        if channel_id is None and workspace is not None:
            params = {
                "channel": channel,
                # https://github.com/typeddjango/django-stubs/issues/1208
                "workspace": dict(self.fields["workspace"].choices).get(int(workspace)),  # type: ignore[attr-defined]
            }
            raise forms.ValidationError(
                self._format_slack_error_message(
                    'The resource "%(channel)s" does not exist or has not been granted access in the %(workspace)s Slack workspace.'
                ),
                code="invalid",
                params=params,
            )

        cleaned_data["channel"] = channel_prefix + channel
        cleaned_data["channel_id"] = channel_id

        return cleaned_data
