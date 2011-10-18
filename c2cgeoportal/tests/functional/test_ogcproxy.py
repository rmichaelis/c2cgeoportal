# -*- coding: utf-8 -*-

from c2cgeoportal.tests import TestView
from papyrus_ogcproxy.views import ogcproxy
from pyramid import testing

class TestOgcproxyView(TestView):

    def test_nourl(self):
        request = testing.DummyRequest()
        request.scheme = 'http'
        response = ogcproxy(request)
        self.assertEqual(response.status_int, 400)

    def test_badurl(self):
        request = testing.DummyRequest()
        request.scheme = 'http'
        request.params['url'] = 'http:/toto'
        response = ogcproxy(request)
        self.assertEqual(response.status_int, 400)

        request.params['url'] = 'ftp://toto'
        response = ogcproxy(request)
        self.assertEqual(response.status_int, 400)
