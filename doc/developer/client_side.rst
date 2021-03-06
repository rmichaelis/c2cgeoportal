.. _developer_client_side:

Client-side development
=======================

CGXP
----

The UI of c2cgeoportal applications is built from components of the CGXP
JavaScript library. This library is on GitHub:
https://github.com/camptocamp/cgxp.

Running tests
~~~~~~~~~~~~~

To run the CGXP tests start by cloning the repository, and updating its
submodules (for GXP, OpenLayers, etc.):

.. prompt:: bash

    git clone https://github.com/camptocamp/cgxp
    cd cgxp
    git submodule update --init

Now open the Jasmine Spec Runner file (``core/tests/SpecRunner.html``) in your
browser. The tests should automatically run (and pass!).

Adding tests
~~~~~~~~~~~~

The test suite is located in the ``core/tests`` directory.

Test files (known as spec files in the Jasmine jargon) are located in the
``spec`` subdirectory. For example, to add tests for a new plugin whose js file
is ``core/src/script/CGXP/plugins/Foo.js``, a spec file named ``Foo.js`` is to
be added in ``core/tests/spec/script/CGXP/plugins/``.

Spec files are referenced using ``<script>`` tags ``SpecRunner.html``.

Coding style
++++++++++++

Lines should not exceed 80 characters.

Dependencies
~~~~~~~~~~~~

Major dependencies docs:

* `CGXP <http://docs.camptocamp.net/cgxp/1.6/>`_
* `GXP <http://gxp.opengeo.org/master/doc/>`_
* `GeoExt <http://dev.geoext.org/geoext/docs/lib/>`_
* `OpenLayers <http://dev.openlayers.org/apidocs/files/OpenLayers-js.html>`_
* `Ext JS <http://docs.sencha.com/ext-js/3-4/>`_

NGEO
----

link
~~~~

Use ngeo in dev mode:

.. prompt:: bash

    git clone git@github.com:camptocamp/ngeo.git
    cd ngeo
    npm config set prefix ~/.npm
    npm link

The `npm config set` command tells npm to use the local folder to store the npm
packages instead of a system folder.

then:

.. prompt:: bash

    cd <your-project>
    npm link ngeo
    make -f <user>.mk build

unlink
~~~~~~

Use packaged npm, production mode:

.. prompt:: bash

    cd <your-project>
    npm unlink ngeo
