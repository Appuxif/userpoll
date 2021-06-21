from rest_framework.routers import SimpleRouter

from mainapp.api import (
    PollAPIView,
    MemberAnswerAPIView,
)

router = SimpleRouter()
router.register('polls', PollAPIView)
router.register('answers', MemberAnswerAPIView)

app_name = 'mainapp'
urlpatterns = router.urls
