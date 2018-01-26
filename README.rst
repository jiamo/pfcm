=====
pfcm
=====


.. image:: https://img.shields.io/pypi/v/pfcm.svg
        :target: https://pypi.python.org/pypi/pfcm

.. image:: https://img.shields.io/travis/jiamo/pfcm.svg
        :target: https://travis-ci.org/jiamo/pfcm

.. image:: https://readthedocs.org/projects/pfcm/badge/?version=latest
        :target: https://pfcm.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/jiamo/pfcm/shield.svg
     :target: https://pyup.io/repos/github/jiamo/pfcm/
     :alt: Updates


another python wraper for firebase cloud message


* Free software: MIT license
* Documentation: https://pfcm.readthedocs.io.
* message ref: https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages
* auth ref: https://firebase.google.com/docs/cloud-messaging/auth-server


test
--------
* you should put config.yml in top dir like ::

    default:
        one_token: one_token
        project_name: you project name

* the private key file should be in top dir with filename ``service_token.json``
