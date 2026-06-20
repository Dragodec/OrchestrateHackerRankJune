from pathlib import Path
import time

import pandas as pd

from pipeline.predictor_factory import (
    PredictorFactory,
)


class OutputGenerator:

    BATCH_SIZE = 2
    MAX_RETRIES = 3

    def generate(
        self,
        claims_path: Path,
        output_path: Path,
    ) -> None:

        claims_df = self._load_claims(
            claims_path
        )

        processed_claims = set()

        if output_path.exists():

            existing_output = pd.read_csv(
                output_path
            )

            processed_claims = set(
                existing_output[
                    "image_paths"
                ]
            )

        remaining_df = claims_df[
            ~claims_df["image_paths"].isin(
                processed_claims
            )
        ]

        batch_df = remaining_df.head(
            self.BATCH_SIZE
        )

        if batch_df.empty:

            print(
                "All test cases processed."
            )

            return

        output_rows = []

        for _, row in batch_df.iterrows():

            user_id = row.get(
                "user_id",
                "unknown"
            )

            predictor = (
                PredictorFactory.get_predictor(
                    row["claim_object"]
                )
            )

            prediction = None

            for attempt in range(
                self.MAX_RETRIES
            ):

                try:

                    print(
                        f"Processing {user_id}..."
                    )

                    prediction = (
                        predictor.predict(
                            row
                        )
                    )

                    break

                except Exception as e:

                    error_message = str(
                        e
                    )

                    if (
                        "503"
                        in error_message
                        or "Service Unavailable"
                        in error_message
                    ):

                        wait_time = (
                            2 ** attempt
                        )

                        print(
                            f"503 received for "
                            f"{user_id}. "
                            f"Retrying in "
                            f"{wait_time}s..."
                        )

                        time.sleep(
                            wait_time
                        )

                        continue

                    print(
                        f"Failed {user_id}: "
                        f"{e}"
                    )

                    break

            if prediction is None:

                print(
                    f"Skipping {user_id} "
                    f"after retries."
                )

                continue

            output_rows.append(
                {
                    **row.to_dict(),
                    **prediction,
                }
            )

        if not output_rows:

            print(
                "No successful predictions."
            )

            return

        output_df = pd.DataFrame(
            output_rows
        )

        file_exists = (
            output_path.exists()
        )

        output_df.to_csv(
            output_path,
            mode="a",
            header=not file_exists,
            index=False,
        )

        print(
            f"Processed "
            f"{len(output_rows)} case(s)."
        )

    @staticmethod
    def _load_claims(
        claims_path: Path,
    ) -> pd.DataFrame:

        return pd.read_csv(
            claims_path
        )