from inkit.metaclasses import ResourceBuilderMetaclass
from inkit.client import ClientRequest


class RenderResource(metaclass=ResourceBuilderMetaclass):

    client = ClientRequest()
