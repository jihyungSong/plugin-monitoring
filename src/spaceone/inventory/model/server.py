import logging

from schematics import Model
from schematics.types import ModelType, StringType, ListType, DictType
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse

_LOGGER = logging.getLogger(__name__)

'''
ComputeEngine Instance
'''


class CollectType(Model):
    avg = StringType()
    max = StringType()


class CPUMonitoring(Model):
    utilization = ModelType(CollectType)


class MemoryMonitoring(Model):
    usage = ModelType(CollectType)
    total = ModelType(CollectType)
    used = ModelType(CollectType)


class DiskMonitoring(Model):
    write_iops = ModelType(CollectType)
    write_throughput = ModelType(CollectType)
    read_iops = ModelType(CollectType)
    read_throughput = ModelType(CollectType)


class NetworkCPUMonitoring(Model):
    received_throughput = ModelType(CollectType)
    received_pps = ModelType(CollectType)
    sent_throughput = ModelType(CollectType)
    sent_pps = ModelType(CollectType)


class Monitoring(Model):
    cpu = ModelType(CPUMonitoring, serialize_when_none=False)
    memory = ModelType(MemoryMonitoring, serialize_when_none=False)
    disk = ModelType(DiskMonitoring, serialize_when_none=False)
    network = ModelType(NetworkCPUMonitoring, serialize_when_none=False)


class Server(Model):
    monitoring = ModelType(Monitoring, default={})

    def reference(self, reference_id):
        return {
            "resource_id": reference_id,
        }


class ComputeInstanceResource(CloudServiceResource):
    cloud_service_group = StringType(default='ComputeEngine')
    cloud_service_type = StringType(default='Instance')
    data = ModelType(Server)


class ComputeInstanceResponse(CloudServiceResponse):
    match_rules = DictType(ListType(StringType), default={'1': ['reference.resource_id']})
    resource_type = StringType(default='inventory.Server')
    resource = ModelType(ComputeInstanceResource)
