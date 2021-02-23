from django.contrib import admin
from domestic.models import Post_Domestic
# Register your models here.
@admin.register(Post_Domestic)
class Post_DomesticAdmin(admin.ModelAdmin):
    list_display =('id','title', 'modify_dt', 'tag_list')
    list_filter=('modify_dt',)
    search_fields=('title','content')
    prepopulated_fields={'slug':('title',)}

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self,obj):
        return ', '.join(o.name for o in obj.tags.all())