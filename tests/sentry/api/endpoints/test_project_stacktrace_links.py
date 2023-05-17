from unittest.mock import patch

from rest_framework.exceptions import ErrorDetail

from sentry.api.endpoints.project_stacktrace_link import get_code_mapping_configs
from sentry.integrations.example.integration import ExampleIntegration
from sentry.models import Integration, OrganizationIntegration
from sentry.testutils import APITestCase
from sentry.testutils.silo import region_silo_test


@region_silo_test
class ProjectStacktraceLinksTest(APITestCase):
    endpoint = "sentry-api-0-project-stacktrace-links"
    filepath = "foo/bar/baz.py"
    url = "https://example.com/example/foo/blob/master/src/foo/bar/baz.py"

    def setUp(self):
        self.integration = Integration.objects.create(provider="example", name="Example")
        self.integration.add_organization(self.organization, self.user)
        self.oi = OrganizationIntegration.objects.get(integration_id=self.integration.id)

        self.repo = self.create_repo(
            project=self.project,
            name="example/foo",
        )
        self.repo.integration_id = self.integration.id
        self.repo.provider = "example"
        self.repo.save()

        self.login_as(self.user)

    def setup_code_mapping(self, stack_root, source_root):
        return self.create_code_mapping(
            organization_integration=self.oi,
            project=self.project,
            repo=self.repo,
            stack_root=stack_root,
            source_root=source_root,
        )

    def test_no_files(self):
        """The file query search is missing"""
        response = self.get_error_response(
            self.organization.slug, self.project.slug, status_code=400
        )
        assert response.data == {
            "file": [ErrorDetail(string="This field is required.", code="required")]
        }

    def test_no_configs(self):
        """No code mappings have been set for this project"""
        # new project that has no configurations set up for it
        project = self.create_project(
            name="foo",
            organization=self.organization,
            teams=[self.create_team(organization=self.organization)],
        )

        response = self.get_success_response(
            self.organization.slug, project.slug, qs_params={"file": self.filepath}
        )
        assert response.data == {
            "files": [
                {
                    "error": "no_code_mappings",
                    "file": self.filepath,
                },
            ],
        }

    def test_file_not_found_error(self):
        self.setup_code_mapping("foo", "src/foo")

        response = self.get_success_response(
            self.organization.slug, self.project.slug, qs_params={"file": self.filepath}
        )
        assert response.data == {
            "files": [
                {
                    "attemptedUrl": self.url,
                    "error": "file_not_found",
                    "file": self.filepath,
                },
            ],
        }

    def test_stack_root_mismatch_error(self):
        self.setup_code_mapping("baz", "src/foo")

        response = self.get_success_response(
            self.organization.slug, self.project.slug, qs_params={"file": self.filepath}
        )
        assert response.data == {
            "files": [
                {
                    "error": "stack_root_mismatch",
                    "file": self.filepath,
                },
            ],
        }

    def test_config_and_source_url(self):
        with patch.object(
            ExampleIntegration, "get_stacktrace_link", return_value="https://sourceurl.com"
        ):
            self.setup_code_mapping("foo", "src/foo")

            response = self.get_success_response(
                self.organization.slug, self.project.slug, qs_params={"file": self.filepath}
            )
            assert response.data == {
                "files": [
                    {
                        "file": self.filepath,
                        "sourceUrl": self.url,
                    },
                ],
            }

    def test_config_and_source_url_with_commit_id(self):
        with patch.object(
            ExampleIntegration, "get_stacktrace_link", return_value="https://sourceurl.com"
        ):
            self.setup_code_mapping("foo", "src/foo")

            qs = {
                "commit_id": "3c2e87573d3bd16f61cf08fece0638cc47a4fc22",
                "file": self.filepath,
            }

            response = self.get_success_response(
                self.organization.slug, self.project.slug, qs_params=qs
            )
            assert response.data == {
                "files": [
                    {
                        "file": self.filepath,
                        "sourceUrl": "https://example.com/example/foo/blob/3c2e87573d3bd16f61cf08fece0638cc47a4fc22/src/foo/bar/baz.py",
                    },
                ],
            }

    def test_fallback_to_default_branch(self):
        with patch.object(
            ExampleIntegration, "get_stacktrace_link", side_effect=[None, "https://sourceurl.com"]
        ):
            self.setup_code_mapping("foo", "src/foo")

            qs = {
                "commit_id": "3c2e87573d3bd16f61cf08fece0638cc47a4fc22",
                "file": self.filepath,
            }

            response = self.get_success_response(
                self.organization.slug, self.project.slug, qs_params=qs
            )
            assert response.data == {
                "files": [
                    {
                        "file": self.filepath,
                        "sourceUrl": self.url,
                    },
                ],
            }

    def test_second_config_works(self):
        with patch.object(
            ExampleIntegration, "get_stacktrace_link", side_effect=[None, "https://sourceurl.com"]
        ):
            code_mapping1 = self.setup_code_mapping("foo", "src/foo")
            code_mapping2 = self.setup_code_mapping("foo/bar", "bar")
            assert get_code_mapping_configs(self.project) == [code_mapping2, code_mapping1]

            response = self.get_success_response(
                self.organization.slug, self.project.slug, qs_params={"file": self.filepath}
            )
            assert response.data == {
                "files": [
                    {
                        "file": self.filepath,
                        "sourceUrl": self.url,
                    },
                ],
            }

    def test_multiple_configs_and_files(self):
        files = [
            "foo0/bar.py",
            "foo0/baz.py",
            "foo1/bar.py",
            "foo1/baz.py",
            "foo2/bar.py",
            "foo2/baz.py",
            "foo3/bar.py",
            "foo3/baz.py",
        ]

        expected = [
            {
                "file": "foo0/bar.py",
                "sourceUrl": "https://example.com/example/foo/blob/master/src/foo0/bar.py",
            },
            {
                "file": "foo0/baz.py",
                "sourceUrl": "https://example.com/example/foo/blob/master/src/foo0/baz.py",
            },
            {
                "error": "file_not_found",
                "file": "foo1/bar.py",
                "attemptedUrl": "https://example.com/example/foo/blob/master/src/foo1/bar.py",
            },
            {
                "error": "file_not_found",
                "file": "foo1/baz.py",
                "attemptedUrl": "https://example.com/example/foo/blob/master/src/foo1/baz.py",
            },
            {
                "file": "foo2/bar.py",
                "sourceUrl": "https://example.com/example/foo/blob/master/src/foo2/bar.py",
            },
            {
                "file": "foo2/baz.py",
                "sourceUrl": "https://example.com/example/foo/blob/master/src/foo2/baz.py",
            },
            {
                "error": "stack_root_mismatch",
                "file": "foo3/bar.py",
            },
            {
                "error": "stack_root_mismatch",
                "file": "foo3/baz.py",
            },
        ]

        self.setup_code_mapping("bar", "")
        self.setup_code_mapping("foo0", "src/foo0")
        self.setup_code_mapping("foo1", "src/foo1")
        self.setup_code_mapping("foo2", "src/foo2")
        self.setup_code_mapping("baz", "")

        with patch.object(
            ExampleIntegration,
            "get_stacktrace_link",
            side_effect=["https://sourceurl.com", None, "https://sourceurl.com"],
        ):
            qs = {"file": files}

            response = self.get_success_response(
                self.organization.slug, self.project.slug, qs_params=qs
            )
            assert response.data == {"files": expected}
