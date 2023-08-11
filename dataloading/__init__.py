
from .mirflickr1m import Mirflickr1m
from .holidays import Holidays
from .selected import Selected
MODELS = dict(mirflickr1m=Mirflickr1m,
              holidays=Holidays,
              selected=Selected,
              # other dataset
              )


def load_dataset(dataset_name, **kwargs):
    """Get dataset"""
    return MODELS[dataset_name](**kwargs)

