# -*- coding: utf-8 -*-

# Copyright (c) 2011-2016, Camptocamp SA
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.


import re
from json import loads, dumps
from argparse import ArgumentParser


def _sub(pattern, repl, string, count=0, flags=0):
    new_string = re.sub(pattern, repl, string, count=count, flags=flags)
    if new_string == string:
        print("Unable to find the pattern:")
        print(pattern)
        print("in")
        print(string)
        exit(1)
    return new_string


def main():
    """
    Import the ngeo apps files
    """

    parser = ArgumentParser(description='import ngeo apps files')

    parser.add_argument('--html', action="store_true", help="Import the html template")
    parser.add_argument('--js', action="store_true", help="Import the javascript controller")
    parser.add_argument('--package', action="store_true", help="Import the package JSON")
    parser.add_argument('interface', metavar='INTERFACE', help="The interface we import")
    parser.add_argument('src', metavar='SRC', help="The ngeo source file")
    parser.add_argument('dst', metavar='DST', help="The destination file")

    args = parser.parse_args()

    with open(args.src) as src:
        data = src.read()

        if args.package:
            json_data = loads(data)
            json_data["name"] = "{{package}}"
            json_data["description"] = "GeoMapfish project"
            del json_data["repository"]
            del json_data["bugs"]
            json_data["devDependencies"]["ngeo"] = "git://github.com/camptocamp/ngeo#master"
            del json_data["devDependencies"]["angular-jsdoc"]
            del json_data["devDependencies"]["jsdoc"]
            del json_data["devDependencies"]["jsdom"]

            del json_data["scripts"]

            data = dumps(json_data, indent=4)
            data = _sub(r" +\n", "\n", data)

        else:
            data = re.sub(r"{{", r"\\{\\{", data)
            data = re.sub(r"}}", r"\\}\\}", data)
            data = re.sub("app", "{{package}}", data)

# temporary disable ...
#        if args.js:
            # Full text search
#            data = _sub(r"datasetTitle: 'Internal',", r"datasetTitle: '{{project}}',", data)

        if args.html:
            # back for ng-app
            data = _sub(r"ng-{{package}}", r"ng-app", data)
            # back for mobile-web-app-capable
            data = _sub(
                r"mobile-web-{{package}}-capable",
                r"mobile-web-app-capable", data
            )
            # Styles
            data = _sub(
                r'    <link rel="stylesheet.*/build/mobile.css">',
                r"""% if debug:
    <link rel="stylesheet/less" href="${{request.static_url('%s/ngeo/contribs/gmf/less/font.less' % request.registry.settings['node_modules_path'])}}" type="text/css">
    <link rel="stylesheet/less" href="${{request.static_url('{{{{package}}}}:static-ngeo/less/{interface}.less')}}" type="text/css">
    <link rel="stylesheet/less" href="${{request.static_url('%s/ngeo/contribs/gmf/less/{interface}.less' % request.registry.settings['node_modules_path'])}}" type="text/css">
% else:
    <link rel="stylesheet" href="${{request.static_url('{{{{package}}}}:static-ngeo/build/{interface}.css')}}" type="text/css">
% endif""".format(interface=args.interface),  # noqa
                data,
                count=1,
                flags=re.DOTALL
            )
            # Scripts
            data = _sub(
                r'    <script .*watchwatchers.js"></script>',
                r"""% if debug:
    <script>
        window.CLOSURE_BASE_PATH = '';
        window.CLOSURE_NO_DEPS = true;
    </script>
    <script src="${{request.static_url('%s/jquery/dist/jquery.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/angular/angular.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/angular-gettext/dist/angular-gettext.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/bootstrap/dist/js/bootstrap.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/proj4/dist/proj4-src.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/d3/d3.min.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/typeahead.js/dist/typeahead.bundle.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/closure/goog/base.js' % request.registry.settings['closure_library_path'])}}"></script>
    <script src="${{request.route_url('deps.js')}}"></script>
    <script>
        goog.require('{{{{package}}}}_{interface}');
    </script>
    <script src="${{request.static_url('{{{{package}}}}:static-ngeo/build/templatecache.js')}}"></script>
    <script src="${{request.static_url('%s/ngeo/utils/watchwatchers.js' % request.registry.settings['node_modules_path'])}}"></script>
    <script src="${{request.static_url('%s/less/dist/less.min.js' % request.registry.settings['node_modules_path'])}}"></script>
% else:
    <script src="${{request.static_url('{{{{package}}}}:static-ngeo/build/{interface}.js')}}"></script>
% endif""".format(interface=args.interface),  # noqa
                data,
                count=1,
                flags=re.DOTALL
            )
            # i18n
            data = _sub(
                "module.constant\('defaultLang', 'en'\);",
                "module.constant('defaultLang', "
                "'${request.registry.settings[\"default_locale_name\"]}');",
                data,
            )
            data = _sub(
                "module.constant\('langUrls', {[^}]*}\);",
                r"""module.constant('langUrls', {
${ ',\\n'.join([
    "             '{lang}': '{url}'".format(
        lang=lang,
        url=request.static_url('demo:static-ngeo/build/{lang}.json'.format(lang=lang))
    )
    for lang in request.registry.settings["available_locale_names"]
]) | n}
           });""",
                data,
            )

            # replace routes
            for constant, url_end, route, query in [
                ("authenticationBaseUrl", r"", "base", None),
                ("fulltextsearchUrl", r"/fulltextsearch", "fulltextsearch", None),
                ("gmfWmsUrl", r"/mapserv_proxy", "mapserverproxy", None),
                ("gmfTreeUrl", r"/themes\?version=2&background=background", "themes", {
                    "version": 2,
                    "background": "background"
                }),
            ]:
                route_args = "" if query is None else ", _query=%s" % dumps(query)
                data = _sub(
                    r"module.constant\('%s', "
                    "'https://geomapfish-demo.camptocamp.net/2.0/wsgi%s'\);" % (
                        constant, url_end
                    ),
                    r"module.constant('%s', '${request.route_url('%s'%s) | n}');" % (
                        constant, route, route_args
                    ),
                    data,
                )

        with open(args.dst, "wt") as dst:
            dst.write(data)
