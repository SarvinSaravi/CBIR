from .resnet50 import Resnet50
from .resnet101 import Resnet101

MODELS = dict(resnet50=Resnet50,
              resnet101=Resnet101,
              # other models
              )


def load_model(model_name, **kwargs):
    """Get models"""
    return MODELS[model_name](**kwargs).get_model()

