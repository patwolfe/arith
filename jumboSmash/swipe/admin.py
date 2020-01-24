from django.contrib import admin
from swipe.models import Interaction


class InteractionAdmin(admin.ModelAdmin):
    list_display = ["id", "swiper", "swiped_on", "smash"]


admin.site.register(Interaction, InteractionAdmin)
