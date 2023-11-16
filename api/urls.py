from ninja_extra import NinjaExtraAPI

from apps.classifieds.api import CategoryAPI, ClassifiedAPI

api = NinjaExtraAPI(
    title="Kelishamiz Documantation",
    version="1.0.",
    description="Developed documentation by Murtazo for Kelishamiz API",
    docs_url='/docs'
)

api.register_controllers(
    CategoryAPI,
    ClassifiedAPI
)
