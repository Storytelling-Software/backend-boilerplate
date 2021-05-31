from models import Profile


class TestProfile:
    def test_init(self):
        result = Profile()

        assert isinstance(result, Profile) is True
        assert result.first_name is None
        assert result.last_name is None

    def test_from_request(self):
        attributes = {
            'first_name': 'John',
            'last_name': 'Doe'
        }

        result = Profile.from_request(attributes)

        assert isinstance(result, Profile) is True
        assert result.first_name == attributes.get('first_name')
        assert result.last_name == attributes.get('last_name')

    def test_assign_request(self):
        profile = Profile()
        profile.first_name = 'John'
        profile.last_name = 'Doe'

        attributes = {
            'first_name': 'Sarah',
            'last_name': 'Connor'
        }

        profile.assign_request(attributes)

        assert isinstance(profile, Profile) is True
        assert profile.first_name == attributes.get('first_name')
        assert profile.last_name == attributes.get('last_name')
