from django.test import TestCase
from neuralartcms.models import Material, Result
import pytest


class MaterialTest(TestCase):

    @pytest.mark.django_db
    def test_material_name_length(self):
        pass


