from pathlib import Path

import pandas as pd


class OutputGenerator:
    """
    Responsible for:
    1. Loading claims.csv
    2. Running predictor on every row
    3. Producing output.csv
    """

    def __init__(self, predictor):
        self.predictor = predictor

    def generate(
        self,
        claims_path: Path,
        output_path: Path,
    ) -> None:

        claims_df = self._load_claims(
            claims_path
        )

        predictions = [
            self.predictor.predict(row)
            for _, row in claims_df.iterrows()
        ]

        predictions_df = pd.DataFrame(
            predictions
        )

        output_df = pd.concat(
            [
                claims_df,
                predictions_df,
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