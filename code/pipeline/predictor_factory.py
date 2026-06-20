from pipeline.Laptop.laptop_predictor import (
    LaptopPredictor,
)


class PredictorFactory:

    @staticmethod
    def get_predictor(
        claim_object: str,
    ):

        return LaptopPredictor()