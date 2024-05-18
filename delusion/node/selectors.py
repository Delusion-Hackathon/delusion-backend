from django.db.models.query import QuerySet
from .models import (
    PCUser,
    Node,
    Memory,
    OSInfo,
    Partition,
    CPU,
    GPU,
    Drive,
    Identifier,
    StorageDevice
)


def all_pc_users() -> QuerySet[PCUser]:
    return PCUser.objects.all()


def all_nodes() -> QuerySet[Node]:
    return Node.objects.select_related('company').prefetch_related('pc_users').all()


def all_memories() -> QuerySet[Memory]:
    return Memory.objects.select_related('node').all()


def all_os_infos() -> QuerySet[OSInfo]:
    return OSInfo.objects.select_related('node').all()


def all_partitions() -> QuerySet[Partition]:
    return Partition.objects.select_related('node').all()


def all_cpus() -> QuerySet[CPU]:
    return CPU.objects.select_related('node').all()


def all_gpus() -> QuerySet[GPU]:
    return GPU.objects.select_related('node').all()


def all_drives() -> QuerySet[Drive]:
    return Drive.objects.select_related('node').all()


def all_identifiers() -> QuerySet[Identifier]:
    return Identifier.objects.select_related('node', 'cpu', 'gpu', 'storage_device').all()


def all_storage_devices() -> QuerySet[StorageDevice]:
    return StorageDevice.objects.select_related('node').all()
