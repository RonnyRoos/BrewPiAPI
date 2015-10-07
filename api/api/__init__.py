"""Main entry point
"""
from pyramid.config import Configurator


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")

    config.scan()

    # print renderer_factory.serializer
    # config.scan("messaging.api.v1")
    return config.make_wsgi_app()
