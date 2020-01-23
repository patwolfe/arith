from django.contrib import admin
from swipe.models import Interaction


class InteractionAdmin(admin.ModelAdmin):
    list_display = ["id", "swiper", "swipe_target", "choice"]


admin.site.register(Interaction, InteractionAdmin)
