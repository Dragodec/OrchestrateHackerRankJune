from pipeline.Car.car_predictor import (
    CarPredictor,
)

from pipeline.Laptop.laptop_predictor import (
    LaptopPredictor,
)

from pipeline.Package.package_predictor import (
    PackagePredictor,
)


class PredictorFactory:

    @staticmethod
    def get_predictor(
        claim_object: str,
    ):

        claim_object = (
            str(claim_object)
            .lower()
            .strip()
        )

        if claim_object == "car":
            return CarPredictor()

        if claim_object == "laptop":
            return LaptopPredictor()

        if claim_object == "package":
            return PackagePredictor()

        raise ValueError(
            f"Unsupported claim object: "
            f"{claim_object}"
        )