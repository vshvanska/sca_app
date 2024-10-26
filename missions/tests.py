from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from cats.models import Cat
from missions.models import Mission, Target


class MissionsTests(APITestCase):
    def setUp(self):
        self.cat_data = {
            "name": "Persik",
            "years_of_experience": 2,
            "breed": "American Shorthair",
            "salary": 500,
        }
        self.cat = Cat.objects.create(**self.cat_data)
        self.mission = Mission.objects.create()

        self.target_data = {
            "name": "First Target",
            "country": "Ukraine",
            "is_completed": False,
            "mission": self.mission,
        }
        Target.objects.create(**self.target_data)
        self.url = reverse("missions:mission-list")

    def test_get_mission_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_mission(self):
        response = self.client.get(
            reverse("missions:mission-detail", args=[self.mission.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.mission.id)

    def test_update_mission_cat(self):
        response = self.client.put(
            reverse("missions:mission-detail", args=[self.mission.id]),
            {"cat": self.cat.id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mission.refresh_from_db()
        self.assertEqual(self.mission.cat, self.cat)

    def test_update_mission_cat_does_not_exist(self):
        response = self.client.put(
            reverse("missions:mission-detail", args=[self.mission.id]), {"cat": 15}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forbidden_delete_mission_with_cat(self):
        self.mission.cat = self.cat
        self.mission.save()
        response = self.client.delete(
            reverse("missions:mission-detail", args=[self.mission.id])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Mission.objects.count(), 1)

    def test_delete_mission(self):
        response = self.client.delete(
            reverse("missions:mission-detail", args=[self.mission.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Mission.objects.count(), 0)


class TargetsTests(APITestCase):
    def setUp(self):
        self.cat_data = {
            "name": "Persik",
            "years_of_experience": 2,
            "breed": "American Shorthair",
            "salary": 500,
        }
        self.cat = Cat.objects.create(**self.cat_data)
        self.mission = Mission.objects.create(cat=self.cat)
        self.target_data = {
            "name": "Test Target",
            "mission": self.mission,
            "country": "Ukraine",
            "is_completed": False,
        }
        self.target = Target.objects.create(**self.target_data)

    def test_get_single_target(self):
        response = self.client.get(
            reverse("missions:target-detail", args=[self.target.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.target.id)

    def test_update_target(self):
        response = self.client.patch(
            reverse("missions:target-detail", args=[self.target.id]),
            {"is_completed": True},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.target.refresh_from_db()
        self.assertTrue(self.target.is_completed)

    def test_update_completed_target(self):
        self.target.is_completed = True
        self.target.save()
        response = self.client.patch(
            reverse("missions:target-detail", args=[self.target.id]),
            {"notes": "New notes"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
