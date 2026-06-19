from pipeline.car_domain import ISSUE_TO_REQUIREMENT


class RequirementMapper:

    def get_requirement_id(
        self,
        issue_type: str,
    ) -> str:

        return ISSUE_TO_REQUIREMENT.get(
            issue_type,
            "REQ_GENERAL_OBJECT_PART",
        )