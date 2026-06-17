from providers.connectors.vast_connector import VastConnector
from providers.connectors.runpod_connector import RunPodConnector
from providers.connectors.coreweave_connector import CoreWeaveConnector
from providers.connectors.lambda_connector import LambdaConnector
from providers.connectors.nebius_connector import NebiusConnector
from providers.connectors.crusoe_connector import CrusoeConnector


CONNECTORS = [
    VastConnector(),
    RunPodConnector(),
    CoreWeaveConnector(),
    LambdaConnector(),
    NebiusConnector(),
    CrusoeConnector()
]
