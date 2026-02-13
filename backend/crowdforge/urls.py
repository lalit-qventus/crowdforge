from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.accounts.api import router as accounts_router
from apps.projects.api import router as projects_router
from apps.contributions.api import router as contributions_router
from apps.tasks.api import router as tasks_router
from apps.karma.api import router as karma_router
from apps.voting.api import router as voting_router
from apps.activity.api import router as activity_router
from apps.search.api import router as search_router

api = NinjaAPI(
    title="CrowdForge API",
    version="0.1.0",
    description="Collaborative open-source platform API",
)

api.add_router("/accounts", accounts_router, tags=["accounts"])
api.add_router("/projects", projects_router, tags=["projects"])
api.add_router("/contributions", contributions_router, tags=["contributions"])
api.add_router("/tasks", tasks_router, tags=["tasks"])
api.add_router("/karma", karma_router, tags=["karma"])
api.add_router("/voting", voting_router, tags=["voting"])
api.add_router("/activity", activity_router, tags=["activity"])
api.add_router("/search", search_router, tags=["search"])

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
