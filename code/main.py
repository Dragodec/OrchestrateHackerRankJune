from pathlib import Path

from pipeline.output_generator import OutputGenerator
from pipeline.car_predictor import CarPredictor


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent

    claims_path = project_root / "dataset" / "claims.csv"
    output_path = project_root / "dataset" / "myOutput.csv"

    predictor = CarPredictor()

    generator = OutputGenerator(
        predictor=predictor
    )

    generator.generate(
        claims_path=claims_path,
        output_path=output_path,
    )

    print(f"Output generated: {output_path}")


if __name__ == "__main__":
    main()