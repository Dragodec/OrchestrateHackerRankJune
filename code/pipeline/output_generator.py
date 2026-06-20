from pathlib import Path

import pandas as pd

from pipeline.predictor_factory import (
    PredictorFactory,
)


class OutputGenerator:
    """
    Responsible for:

    1. Loading claims.csv
    2. Selecting predictor
    3. Running prediction
    4. Producing output.csv
    """

    def generate(
        self,
        claims_path: Path,
        output_path: Path,
    ) -> None:

        claims_df = self._load_claims(
            claims_path
        )

        # TEMPORARY:
        # Run only specific test cases

        claims_df = claims_df[
            claims_df["user_id"].isin(
                [
                     "user_020",
            "user_026",
            "user_028",
                ]
            )
        ]

        predictions = []

        # =====================================
        # Create predictor ONLY ONCE
        # =====================================

        predictor = (
            PredictorFactory.get_predictor(
                "laptop"
            )
        )

        for _, row in (
            claims_df.iterrows()
        ):

            prediction = (
                predictor.predict(
                    row
                )
            )

            predictions.append(
                prediction
            )

        predictions_df = pd.DataFrame(
            predictions
        )

        output_df = pd.concat(
            [
                claims_df.reset_index(
                    drop=True
                ),
                predictions_df.reset_index(
                    drop=True,
                ),
            ],
            axis=1,
        )

        output_df.to_csv(
            output_path,
            index=False,
        )

    @staticmethod
    def _load_claims(
        claims_path: Path,
    ) -> pd.DataFrame:

        return pd.read_csv(
            claims_path
        )