from pipeline.Package.package_domain import (
    ISSUE_TO_REQUIREMENT,
)


class RequirementMapper:

    def get_requirement_id(
        self,
        issue_type: str,
    ) -> str:

        return ISSUE_TO_REQUIREMENT.get(
            issue_type,
            "REQ_PACKAGE_GENERAL",
        )