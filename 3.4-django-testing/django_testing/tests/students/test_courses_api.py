
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student, Course

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory

@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory

# проверка получения первого курса (retrieve-логика):
# создаем курс через фабрику;
# строим урл и делаем запрос через тестовый клиент;
# проверяем, что вернулся именно тот курс, который запрашивали;
@pytest.mark.django_db
def test_get_course(client, course_factory):
    # Arrange
    course = course_factory(_quantity=1)[0]

    # Act
    response = client.get(reverse("courses-list") + "1/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course.name

# проверка получения списка курсов (list-логика):
# аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат;
@pytest.mark.django_db
def test_list_courses(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(reverse("courses-list"))

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name

# # проверка фильтрации списка курсов по id:
# # создаем курсы через фабрику, передать ID одного курса в фильтр, проверить результат запроса с фильтром;
@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(reverse("courses-list") + f"?id={courses[5].id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == courses[5].id

# проверка фильтрации списка курсов по name;
@pytest.mark.django_db
def test_filter_course_by_name(client, course_factory):
    # Arrange
    courses = course_factory(_quantity=10)

    # Act
    response = client.get(reverse("courses-list") + f"?name={courses[3].name}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[3].name

# тест успешного создания курса:
# здесь фабрика не нужна, готовим JSON-данные и создаём курс;
@pytest.mark.django_db
def test_create_course(client):
    # Arrange
    course_data = {"name": "Course 1"}

    # Act
    response = client.post(reverse("courses-list"), data=course_data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == "Course 1"


# тест успешного обновления курса:
# сначала через фабрику создаём, потом обновляем JSON-данными;
@pytest.mark.django_db
def test_update_course(client, course_factory):
    # Arrange
    course_data = {"name": "Course 1"}
    course = course_factory(_quantity=1)[0]

    # Act
    response = client.patch(reverse("courses-list") + f"{course.id}/", data=course_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == "Course 1"

# тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    # Arrange
    course_data = {"name": "Course 1"}
    course = course_factory(_quantity=1)[0]

    # Act
    response = client.delete(reverse("courses-list") + f"{course.id}/")

    # Assert
    assert response.status_code == 204

