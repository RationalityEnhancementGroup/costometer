"""Profile optimization API."""
import logging
from argparse import ArgumentParser
from pathlib import Path

from .analysis_utils import AnalysisObject
from .plotting_utils import set_font_sizes

class AnalysisFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.format_without_log_prefix_message = "%(message)s"

    def format(self, record):
        # Check if we need to format without timestamp and log level
        if not getattr(record, 'log_prefix', True):
            self._style._fmt = self.format_without_log_prefix_message
        else:
            self._style._fmt = self._fmt
        return super().format(record)

class AnalysisFilter(logging.Filter):
    """Sometimes we need the logs to be easily copy/pasted into document."""
    def filter(self, record):
        # Modify msg based on custom attributes
        record.log_prefix = getattr(record, 'log_prefix', True)
        return True

def standard_parse_args(
        description: str,
        irl_path: Path,
        filename:str,
        default_experiment : str = "MainExperiment",
        default_subdirectory : Path = Path("methods") / "static",
    ):
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "-e",
        "--exp",
        dest="experiment_name",
        default=default_experiment,
    )
    parser.add_argument(
        "-s",
        "--subdirectory",
        default=default_subdirectory,
        dest="experiment_subdirectory",
        metavar="experiment_subdirectory",
        type=Path,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
        action="store_const",
        help="When set, logs progress while running.",
    )
    inputs = parser.parse_args()

    subdirectory = irl_path / "analysis" / inputs.experiment_subdirectory
    
    set_plotting_and_logging_defaults(subdirectory=subdirectory, experiment_name=inputs.experiment_name, filename=filename, logging_level=inputs.loglevel)
    analysis_obj = load_analysis_object(inputs.experiment_name, irl_path, subdirectory)
    logging.info("Analysis started...\n----------")
    return analysis_obj, inputs, subdirectory


def set_plotting_and_logging_defaults(
        subdirectory : Path,
        experiment_name : str, 
        filename : str,
        logging_level : int= logging.INFO):
    set_font_sizes()
    
    subdirectory.joinpath("log").mkdir(parents=True, exist_ok=True)
    subdirectory.joinpath("data").mkdir(parents=True, exist_ok=True)
    subdirectory.joinpath("figs").mkdir(parents=True, exist_ok=True)

    handlers = [
        logging.FileHandler(subdirectory / "log" / f"{experiment_name}_{filename}.log"),
        logging.StreamHandler(),
    ]

    for handler in handlers:
        handler.setFormatter(AnalysisFormatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                               datefmt='%Y-%m-%d %H:%M:%S',
                                               )
                             )
        handler.addFilter(AnalysisFilter())

    logging.basicConfig(
        level=logging_level,
        handlers=handlers,
    )

def load_analysis_object(experiment_name : str,
                         irl_path : Path,
                         experiment_subdirectory : Path):
    analysis_obj = AnalysisObject(
        experiment_name,
        irl_path=irl_path,
        experiment_subdirectory=experiment_subdirectory,
    )
    
    return analysis_obj



class DissertationLogHandler:
    """Log handler for saving tex snippets for my dissertation."""
    def __init__(self, file_path_string : str):
        self.logger = logging.getLogger()

        # Create the directory if it doesn't exist
        file_path = Path(file_path_string)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self.handler = logging.FileHandler(file_path)

    def __enter__(self):
        self.logger.addHandler(self.handler)

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.removeHandler(self.handler)

