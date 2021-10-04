from __future__ import absolute_import

from inkit.products.abstract_product import AbstractProduct
from inkit.resources.render_resources import RenderResource


class Render(AbstractProduct):

    _main_resource = RenderResource()
