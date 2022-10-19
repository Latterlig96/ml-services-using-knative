import argparse
from knative_ml_services.models.training.train import main as train_main
from knative_ml_services.api.main import main as api_main

parser = argparse.ArgumentParser("Knative ml services module handler")

parser.add_argument("-m",
                    "--mode",
                    dest="mode",
                    type=str,
                    help="Mode to run application, either 'API' or 'Train'")

if __name__ == "__main__":
    args = parser.parse_known_args()
    if args[0].__dict__["mode"] == "api":
        api_main()
    else:
        train_main()
