import pytest
from django.urls import reverse


# проверка получения 1го курса (retrieve-логика
@pytest.mark.django_db
def test_one_course(api_client, course_factory):
    course = course_factory()
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]['name'] == course.name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    course_factory(_quantity=2)
    url = reverse('courses-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filtered_by_id_courses(api_client, course_factory):
    course = course_factory()
    url = f'{reverse("courses-list")}?id={course.id}'
    response = api_client.get(url)
    assert response.status_code == 200


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filtered_by_name_courses(api_client, course_factory):
    course = course_factory()
    url = f'{reverse("courses-list")}?name={course.name}'
    response = api_client.get(url)
    assert len(response.data) == 1
    assert response.data[0]["name"] == course.name
    assert response.status_code == 200


# тест успешного создания курса
@pytest.mark.django_db
def test_create_a_course(api_client):
    data = {"name": "math"}
    url = reverse("courses-list")
    response = api_client.post(url, data)
    assert response.status_code == 201


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_a_course(api_client, course_factory):
    course = course_factory()
    url = f'{reverse("courses-list")}{course.id}/'
    data = {"name": "chemistry"}
    response = api_client.put(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_a_course(api_client, course_factory):
    course = course_factory()
    url = f'{reverse("courses-list")}{course.id}/'
    response = api_client.delete(url)
    assert response.status_code == 204
