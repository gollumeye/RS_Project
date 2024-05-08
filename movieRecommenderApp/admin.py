from django.contrib import admin

# Register your models here.

#user gollu
#email larandl@edu.aau.at
#pw: asdf123

from .models import Movie, Rating, Tag

admin.site.register(Movie)
admin.site.register(Rating)
admin.site.register(Tag)

