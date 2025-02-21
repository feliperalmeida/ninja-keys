from ninja import NinjaAPI, Router

from test_project.heroes.auth import HeroAPIKeyAuth

api = NinjaAPI()
router = Router()


@router.get("/public")
def public(request):
    return "Hello, world!"


@router.get("/protected", auth=HeroAPIKeyAuth())
def protected(request):
    return "Hello, protected!"


api.add_router("", router)
