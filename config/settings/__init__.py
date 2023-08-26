from .base import *

from decouple import config

env_type = config("ENV_TYPE")

if env_type == "local":
    from .local import *
elif env_type == "staging":
    from .staging import *
elif env_type == "prod":
    from .prod import *
