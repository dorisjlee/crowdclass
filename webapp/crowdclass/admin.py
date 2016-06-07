from django.contrib import admin

# Register your models here.
from .models import Elliptical, Spiral, Edge, Bulge, Bar, Merging, Dust, Lens, Tidal, UserSession, PrePostTest, Participant, EdgeDescription, BulgeDescription, BarDescription, MergingDescription, DustDescription, LensDescription, TidalDescription, EllipticalDescription, SpiralDescription, Introduction


admin.site.register(EdgeDescription)
admin.site.register(BulgeDescription)
admin.site.register(BarDescription)
admin.site.register(MergingDescription)
admin.site.register(DustDescription)
admin.site.register(LensDescription)
admin.site.register(TidalDescription)
admin.site.register(EllipticalDescription)
admin.site.register(SpiralDescription)

admin.site.register(Introduction)

admin.site.register(Elliptical)
admin.site.register(Spiral)
admin.site.register(Edge)
admin.site.register(Bulge)
admin.site.register(Bar)
admin.site.register(Merging)
admin.site.register(Dust)
admin.site.register(Lens)
admin.site.register(Tidal)
admin.site.register(UserSession)
admin.site.register(PrePostTest)
admin.site.register(Participant)