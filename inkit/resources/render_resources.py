from __future__ import absolute_import

from inkit.resources.abstract_resources import (
    CreatableResource,
    RetrievableResource,
    ListableResource,
    UpdatableResource,
    DeletableResource
)


class RenderResource(
    CreatableResource,
    RetrievableResource,
    ListableResource,
    UpdatableResource,
    DeletableResource
):
    _module_name = "renders"
