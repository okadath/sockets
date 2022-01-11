from django.contrib import admin
from .models import JuntaVP_Encuesta, SUVW_Privacidad, SUVW_Privacidad_2, SUVW_Carta_Responsiva, TextArticle, NJ_Encuesta,\
    NJ_Registro
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class ModelAdmin(ImportExportModelAdmin):
    pass


#
# admin.site.register(NJ_Registro, ModelAdmin)
# admin.site.register(NJ_Encuesta, ModelAdmin)
#
admin.site.register(JuntaVP_Encuesta, ModelAdmin)
# admin.site.register(SUVW_Privacidad, ModelAdmin)
# admin.site.register(SUVW_Privacidad_2, ModelAdmin)
# admin.site.register(SUVW_Carta_Responsiva, ModelAdmin)
#
admin.site.register(TextArticle)
