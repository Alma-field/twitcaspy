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
        ok_(hasattr(data, 'live'))
        ok_(hasattr(data.live, 'movie'))
        ok_(hasattr(data.live, 'broadcaster'))
        ok_(hasattr(data.live, 'tags'))

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

    @raises(TwitcaspyException)
    @tape.use_cassette('testsetcurrentlivesubtitle_raise1.json')
    def testsetcurrentlivesubtitle_raise1(self):
        data = self.api.set_current_live_subtitle('')

    @raises(TwitcaspyException)
    @tape.use_cassette('testsetcurrentlivesubtitle_raise2.json')
    def testsetcurrentlivesubtitle_raise2(self):
        data = self.api.set_current_live_subtitle(
            '123456789012345678')

    @tape.use_cassette('testgetcomments.yaml', serializer='yaml')
    def testgetcomments(self):
        data = self.api.get_comments('189037369')
        ok_(hasattr(data, 'movie_id'))
        eq_(data.movie_id, '189037369')
        ok_(hasattr(data, 'all_count'))
        ok_(hasattr(data, 'comments'))

    @tape.use_cassette('testsupportuser.json')
    def testsupportuser(self):
        target_user_ids = ['twitcasting_jp']
        data = self.api.support_user(target_user_ids=target_user_ids)
        ok_(hasattr(data, 'added_count'))
        eq_(data.added_count, len(target_user_ids))

    @tape.use_cassette('testunsupportuser.json')
    def testunsupportuser(self):
        target_user_ids = ['twitcasting_jp']
        data = self.api.unsupport_user(target_user_ids=target_user_ids)
        ok_(hasattr(data, 'removed_count'))
        eq_(data.removed_count, len(target_user_ids))

    @tape.use_cassette('testsupportinglist.json')
    def testsupportinglist(self):
        data = self.api.supporting_list(id=user_id)
        ok_(hasattr(data, 'total'))
        ok_(hasattr(data, 'supporting'))

    @tape.use_cassette('testsupporterlist.json')
    def testsupporterlist(self):
        data = self.api.supporter_list(id=user_id)
        ok_(hasattr(data, 'total'))
        ok_(hasattr(data, 'supporters'))

    @raises(TwitcaspyException)
    @tape.use_cassette('testgetcategories_raise.json')
    def testgetcategories_raise(self):
        data = self.api.get_categories(lang='fr')

    @tape.use_cassette('testgetcategories.yaml', serializer='yaml')
    def testgetcategories(self):
        data = self.api.get_categories()
        ok_(hasattr(data, 'categories'))

    @tape.use_cassette('testsearchusers.yaml', serializer='yaml')
    def testsearchusers(self):
        data = self.api.search_users(words='ツイキャス 公式')
        ok_(hasattr(data, 'users'))

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchusers_raise1.json')
    def testsearchusers_raise1(self):
        data = self.api.search_users(words='ツイキャス 公式', lang='en')

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchusers_raise2.json')
    def testsearchusers_raise2(self):
        data = self.api.search_users()

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchusers_raise3.json')
    def testsearchusers_raise3(self):
        data = self.api.search_users(words=0)

    @tape.use_cassette('testsearchmovies.yaml', serializer='yaml')
    def testsearchmovies(self):
        data = self.api.search_live_movies(type='new')
        ok_(hasattr(data, 'movies'))
        ok_(isinstance(data.movies, list))

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchmovies_raise1.json')
    def testsearchmovies_raise1(self):
        #When type are not specified.
        data = self.api.search_live_movies()

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchmovies_raise2.json')
    def testsearchmovies_raise2(self):
        #When type is not a `tag`, `word`, `category`, `new` or `recommend`.
        data = self.api.search_live_movies(type='error')

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchmovies_raise3.json')
    def testsearchmovies_raise3(self):
        #No context specified when type is tag, word or category.
        data = self.api.search_live_movies(type='word')

    @raises(TwitcaspyException)
    @tape.use_cassette('testsearchmovies_raise4.json')
    def testsearchmovies_raise4(self):
        #When lang is not a 'ja'.
        data = self.api.search_live_movies(type='new', lang='en')

    def testincomingwebhook(self):
        from json import load
        file_name = 'cassettes/testincomingwebhook.json'
        with open(file_name, "r", encoding='utf-8') as file:
            json = load(file)
        data = self.api.incoming_webhook(json)
        ok_(hasattr(data, 'signature'))
        ok_(isinstance(data.signature, str))
        ok_(hasattr(data, 'movie'))
        ok_(hasattr(data, 'broadcaster'))

    @tape.use_cassette('testgetwebhooklist.json')
    def testgetwebhooklist(self):
        data = self.api.get_webhook_list()
        ok_(hasattr(data, 'all_count'))
        ok_(isinstance(data.all_count, int))
        ok_(hasattr(data, 'webhooks'))
        ok_(isinstance(data.webhooks, list))

    @tape.use_cassette('testgetwebhooklist_idstring.json')
    def testgetwebhooklist_idstring(self):
        data = self.api.get_webhook_list(user_id=username)
        ok_(hasattr(data, 'all_count'))
        ok_(isinstance(data.all_count, int))
        ok_(hasattr(data, 'webhooks'))
        ok_(isinstance(data.webhooks, list))

    @tape.use_cassette('testregisterwebhook.json')
    def testregisterwebhook(self):
        events = ['livestart', 'liveend']
        data = self.api.register_webhook(user_id=user_id, events=events)
        ok_(hasattr(data, 'user_id'))
        eq_(data.user_id, user_id)
        ok_(hasattr(data, 'added_events'))
        ok_(isinstance(data.added_events, list))

    @raises(TwitcaspyException)
    @tape.use_cassette('testregisterwebhook_raise1.json')
    def testregisterwebhook_raise1(self):
        data = self.api.register_webhook(user_id=username, events='events')

    @raises(TwitcaspyException)
    @tape.use_cassette('testregisterwebhook_raise2.json')
    def testregisterwebhook_raise2(self):
        events = ['livestart', 'liveend', 'none']
        data = self.api.register_webhook(user_id=username, events=events)

    @tape.use_cassette('testremovewebhook.json')
    def testremovewebhook(self):
        events = ['livestart', 'liveend']
        data = self.api.remove_webhook(user_id=user_id, events=events)
        ok_(hasattr(data, 'user_id'))
        eq_(data.user_id, user_id)
        ok_(hasattr(data, 'removed_events'))
        ok_(isinstance(data.removed_events, list))

    @raises(TwitcaspyException)
    @tape.use_cassette('testremovewebhook_raise1.json')
    def testremovewebhook_raise1(self):
        data = self.api.remove_webhook(user_id=username, events='events')

    @raises(TwitcaspyException)
    @tape.use_cassette('testremovewebhook_raise2.json')
    def testremovewebhook_raise2(self):
        events = ['livestart', 'liveend', 'none']
        data = self.api.remove_webhook(user_id=username, events=events)
