import pandas as pd
import json


def prepare_dataframe(raw_data: str) -> pd.DataFrame:
    data = json.loads(raw_data)
    return pd.DataFrame(data)
