from rest_framework import viewsets
from care_diet.models.nutrition_intake import NutritionIntake
from care_diet.api.serializers.intake_log import NutritionIntakeCreateSpec
from care.emr.api.viewsets.base import EMRCreateMixin, EMRListMixin

class IntakeLogViewSet(EMRCreateMixin, EMRListMixin, viewsets.GenericViewSet):
    database_model = NutritionIntake
    pydantic_model = NutritionIntakeCreateSpec

    queryset = NutritionIntake.objects.all().select_related("patient", "facility", "location")

    def authorize_create(self, instance):
        """
        This hook is called before saving. We set the user here.
        """
        instance.logged_by = self.request.user
