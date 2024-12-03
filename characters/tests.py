from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from characters.models import Team, Position, Skills, Content, ContentType, Character

# Create your tests here.
class CharactersViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_get_character(self):
        tm = baker.make(Team)
        character = baker.make(Character, team = tm)

        r = self.client.get('/api/characters/')
        data = r.json()

        assert character.name == data[0]['name']
        assert character.id == data[0]['id']
        assert character.team.id == data[0]['team']
        assert len(data) == 1


    def test_create_character(self):
        tm = baker.make(Team)
        
        r = self.client.post('/api/characters/', {
            "name": "Персонаж2",
            "team": tm.id
        })

        new_character_id = r.json()['id']

        characters = Character.objects.all()
        assert len(characters) == 1

        new_character = Character.objects.filter(id = new_character_id).first()
        assert new_character.name == 'Персонаж2'
        assert new_character.team == tm


    def test_delete_character(self):
        characters = baker.make(Character, 10)
        r = self.client.get('/api/characters/')
        data = r.json()
        assert len(data) == 10

        character_id_to_delete = characters[3].id
        self.client.delete(f'/api/characters/{character_id_to_delete}/')

        r = self.client.get('/api/characters/')
        data = r.json()
        assert len(data) == 9

        assert character_id_to_delete not in [i['id'] for i in data]


    def test_update_character(self):
        characters = baker.make(Character, 10)
        character: Character = characters[3]

        r = self.client.get(f'/api/characters/{character.id}/')
        data = r.json()
        assert data['name'] == character.name
        
        r = self.client.patch(f'/api/characters/{character.id}/', {
          "name": "Тэцуя Куроко"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/characters/{character.id}/')
        data = r.json()
        assert data['name'] == "Тэцуя Куроко"

        character.refresh_from_db()
        assert data['name'] == character.name

class TeamViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_get_team(self):
        team = baker.make(Team, name="Команда 1")

        response = self.client.get('/api/teams/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == team.name
        assert data[0]['id'] == team.id


    def test_create_team(self):
        response = self.client.post('/api/teams/', {
            "name": "Команда 2"
        })

        new_team_id = response.json()['id']
        teams = Team.objects.all()

        assert response.status_code == 201
        assert len(teams) == 1

        new_team = Team.objects.get(id=new_team_id)
        assert new_team.name == 'Команда 2'


    def test_delete_team(self):
        teams = baker.make(Team, 10)
        response = self.client.get('/api/teams/')
        data = response.json()
        assert len(data) == 10

        team_id_to_delete = teams[3].id
        self.client.delete(f'/api/teams/{team_id_to_delete}/')

        response = self.client.get('/api/teams/')
        data = response.json()
        assert len(data) == 9
        assert team_id_to_delete not in [i['id'] for i in data]


    def test_update_team(self):
        team = baker.make(Team, name="Команда 1")

        response = self.client.get(f'/api/teams/{team.id}/')
        data = response.json()
        assert data['name'] == team.name

        response = self.client.patch(f'/api/teams/{team.id}/', {
            "name": "Новая Команда"
        })
        assert response.status_code == 200

        response = self.client.get(f'/api/teams/{team.id}/')
        data = response.json()
        assert data['name'] == "Новая Команда"

        team.refresh_from_db()
        assert data['name'] == team.name

class PositionViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_get_position(self):
        position = baker.make(Position, name="Нападающий")

        response = self.client.get('/api/positions/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == position.name
        assert data[0]['id'] == position.id


    def test_create_position(self):
        response = self.client.post('/api/positions/', {
            "name": "Защитник"
        })

        new_position_id = response.json()['id']
        positions = Position.objects.all()

        assert response.status_code == 201
        assert len(positions) == 1

        new_position = Position.objects.get(id=new_position_id)
        assert new_position.name == 'Защитник'


    def test_delete_position(self):
        positions = baker.make(Position, 10)
        response = self.client.get('/api/positions/')
        data = response.json()
        assert len(data) == 10

        position_id_to_delete = positions[3].id
        self.client.delete(f'/api/positions/{position_id_to_delete}/')

        response = self.client.get('/api/positions/')
        data = response.json()
        assert len(data) == 9
        assert position_id_to_delete not in [i['id'] for i in data]


    def test_update_position(self):
        position = baker.make(Position, name="Нападающий")

        response = self.client.get(f'/api/positions/{position.id}/')
        data = response.json()
        assert data['name'] == position.name

        response = self.client.patch(f'/api/positions/{position.id}/', {
            "name": "Новая Позиция"
        })
        assert response.status_code == 200

        response = self.client.get(f'/api/positions/{position.id}/')
        data = response.json()
        assert data['name'] == "Новая Позиция"

        position.refresh_from_db()
        assert data['name'] == position.name


class SkillsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_skill(self):
        skill = baker.make(Skills, name="Скорость")

        response = self.client.get('/api/skills/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == skill.name
        assert data[0]['id'] == skill.id


    def test_create_skill(self):
        response = self.client.post('/api/skills/', {
            "name": "Сила",
            "description": "Описание силы"
        })

        new_skill_id = response.json()['id']
        skills = Skills.objects.all()

        assert response.status_code == 201
        assert len(skills) == 1

        new_skill = Skills.objects.get(id=new_skill_id)
        assert new_skill.name == 'Сила'
        assert new_skill.description == 'Описание силы'


    def test_delete_skill(self):
        skills = baker.make(Skills, 10)
        response = self.client.get('/api/skills/')
        data = response.json()
        assert len(data) == 10

        skill_id_to_delete = skills[3].id
        self.client.delete(f'/api/skills/{skill_id_to_delete}/')

        response = self.client.get('/api/skills/')
        data = response.json()
        assert len(data) == 9
        assert skill_id_to_delete not in [i['id'] for i in data]


    def test_update_skill(self):
        skill = baker.make(Skills, name="Скорость")

        response = self.client.get(f'/api/skills/{skill.id}/')
        data = response.json()
        assert data['name'] == skill.name

        response = self.client.patch(f'/api/skills/{skill.id}/', {
            "name": "Новая Способность"
        })
        assert response.status_code == 200

        response = self.client.get(f'/api/skills/{skill.id}/')
        data = response.json()
        assert data['name'] == "Новая Способность"

        skill.refresh_from_db()
        assert data['name'] == skill.name


class ContentTypeViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_get_content_type(self):
        content_type = baker.make(ContentType, name="Тип 1")

        response = self.client.get('/api/content-types/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['name'] == content_type.name
        assert data[0]['id'] == content_type.id


    def test_create_content_type(self):
        response = self.client.post('/api/content-types/', {
            "name": "Тип 2"
        })

        new_content_type_id = response.json()['id']
        content_types = ContentType.objects.all()

        assert response.status_code == 201
        assert len(content_types) == 1

        new_content_type = ContentType.objects.get(id=new_content_type_id)
        assert new_content_type.name == 'Тип 2'


    def test_delete_content_type(self):
        content_types = baker.make(ContentType, 10)
        response = self.client.get('/api/content-types/')
        data = response.json()
        assert len(data) == 10

        content_type_id_to_delete = content_types[3].id
        self.client.delete(f'/api/content-types/{content_type_id_to_delete}/')

        response = self.client.get('/api/content-types/')
        data = response.json()
        assert len(data) == 9
        assert content_type_id_to_delete not in [i['id'] for i in data]


    def test_update_content_type(self):
        content_type = baker.make(ContentType, name="Тип 1")

        response = self.client.get(f'/api/content-types/{content_type.id}/')
        data = response.json()
        assert data['name'] == content_type.name

        response = self.client.patch(f'/api/content-types/{content_type.id}/', {
            "name": "Новый Тип"
        })
        assert response.status_code == 200

        response = self.client.get(f'/api/content-types/{content_type.id}/')
        data = response.json()
        assert data['name'] == "Новый Тип"

        content_type.refresh_from_db()
        assert data['name'] == content_type.name


class ContentViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()


    def test_get_content(self):
        content_type = baker.make(ContentType, name="Тип 1")
        content = baker.make(Content, type=content_type, episode_name="Эпизод 1", episode=1, volume=1, description="Описание 1")

        response = self.client.get('/api/content/')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['episode_name'] == content.episode_name
        assert data[0]['id'] == content.id


    def test_create_content(self):
        content_type = baker.make(ContentType, name="Тип 1")
        
        response = self.client.post('/api/content/', {
            "type": content_type.id,
            "episode_name": "Эпизод 2",
            "episode": 2,
            "volume": 1,
            "description": "Описание 2"
        })

        new_content_id = response.json()['id']
        contents = Content.objects.all()

        assert response.status_code == 201
        assert len(contents) == 1

        new_content = Content.objects.get(id=new_content_id)
        assert new_content.episode_name == 'Эпизод 2'


    def test_delete_content(self):
        content_type = baker.make(ContentType, name="Тип 1")
        contents = baker.make(Content, type=content_type, _quantity=10)
        response = self.client.get('/api/content/')
        data = response.json()
        assert len(data) == 10

        content_id_to_delete = contents[3].id
        self.client.delete(f'/api/content/{content_id_to_delete}/')

        response = self.client.get('/api/content/')
        data = response.json()
        assert len(data) == 9
        assert content_id_to_delete not in [i['id'] for i in data]

    def test_update_content(self):
        content_type = baker.make(ContentType, name="Тип 1")
        content = baker.make(Content, type=content_type, episode_name="Эпизод 1")

        response = self.client.get(f'/api/content/{content.id}/')
        data = response.json()
        assert data['episode_name'] == content.episode_name

        response = self.client.patch(f'/api/content/{content.id}/', {
            "episode_name": "Новый Эпизод"
        })
        assert response.status_code == 200

        response = self.client.get(f'/api/content/{content.id}/')
        data = response.json()
        assert data['episode_name'] == "Новый Эпизод"

        content.refresh_from_db()
        assert data['episode_name'] == content.episode_name