from nose.tools import ok_, eq_, raises

from twitcaspy import API

from twitcaspy.errors import TwitcaspyException, Unauthorized, NotFound

from .config import tape, TwitcaspyTestCase, user_id, username

movie_id = '189037369'

class TwitcaspyAPITests(TwitcaspyTestCase):
    @raises(TwitcaspyException)
    @tape.use_cassette('testraise_authenticationrequired.json')
    def testraise_authenticationrequired(self):
        from twitcaspy import api
        data = api.get_user_info(id=user_id)

    @tape.use_cassette('testgetuserinfo.json')
    def testgetuserinfo(self):
        data = self.api.get_user_info(id=user_id)
        ok_(hasattr(data, 'user'))
        eq_(data.user.screen_id, username)
        ok_(hasattr(data, 'supporter_count'))
        ok_(hasattr(data, 'supporting_count'))

    @raises(Unauthorized)
    @tape.use_cassette('testverifycredentials.json')
    def testverifycredentials(self):
        data = self.api.verify_credentials()

    @tape.use_cassette('testgetlivethumbnailimage.yaml', serializer='yaml')
    def testgetlivethumbnailimage(self):
        data = self.api.get_live_thumbnail_image(id=user_id)
        eq_(data.status_code, 200)
        ok_(len(data.content) > 0)

    @tape.use_cassette('testgetmovieinfo.json')
    def testgetmovieinfo(self):
        data = self.api.get_movie_info(movie_id=movie_id)
        ok_(hasattr(data, 'movie'))
        eq_(data.movie.user_id, user_id)
        ok_(hasattr(data, 'broadcaster'))
        eq_(data.broadcaster.id, user_id)
        eq_(data.broadcaster.screen_id, username)
        ok_(hasattr(data, 'tags'))
        ok_(isinstance(data.tags, list))

    @tape.use_cassette('testgetmoviesbyuser.yaml', serializer='yaml')
    def testgetmoviesbyuser(self):
        data = self.api.get_movies_by_user(id=user_id)
        ok_(hasattr(data, 'total_count'))
        ok_(hasattr(data, 'movies'))
        ok_(len(data.movies) == 20 or len(data.movies) == data.total_count)

    @raises(NotFound)
    @tape.use_cassette('testgetcurrentlive_raise404.json')
    def testgetcurrentlive_raise404(self):
        data = self.api.get_current_live(id=user_id)
