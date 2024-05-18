from django.db import models
from delusion.utils.models import TrackingModel
from .choices import AntiVirusChoices


class PCUser(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'pc_user'


class Node(TrackingModel):
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='nodes')
    node_id = models.CharField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    domain = models.CharField(max_length=100, null=True, blank=True)
    host = models.CharField(max_length=100, null=True, blank=True)
    pc_users = models.ManyToManyField('PCUser', related_name='nodes')
    os_desc = models.CharField(max_length=150, null=True, blank=True)
    ip = models.CharField(max_length=100, null=True, blank=True)
    antivirus = models.CharField(max_length=1, choices=AntiVirusChoices.choices, null=True, blank=True)
    auto_update = models.BooleanField(default=True)
    firewall = models.BooleanField(default=True)

    @property
    def get_node_id(self):
        return self.node_id.replace('node//', '', 1)

    class Meta:
        db_table = 'node'
        ordering = ('-pk', )


class Memory(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='memories')
    bank_label = models.CharField(max_length=50, null=True, blank=True)
    capacity = models.CharField(max_length=50, null=True, blank=True)
    caption = models.CharField(max_length=50, null=True, blank=True)
    creation_class_name = models.CharField(max_length=50, null=True, blank=True)
    data_width = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=50, null=True, blank=True)
    device_locator = models.CharField(max_length=30, null=True, blank=True)
    max_voltage = models.IntegerField(null=True, blank=True)
    min_voltage = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    part_number = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    sm_bios_memory_type = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    tag = models.CharField(max_length=50, null=True, blank=True)
    total_width = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'memory'


class OSInfo(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='os_infos')
    boot_device = models.CharField(max_length=100, null=True, blank=True)
    build_number = models.CharField(max_length=30, null=True, blank=True)
    build_type = models.CharField(max_length=50, null=True, blank=True)
    caption = models.CharField(max_length=50, null=True, blank=True)
    code_set = models.CharField(max_length=30, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    creation_class_name = models.CharField(max_length=50, null=True, blank=True)
    cs_creation_class_name = models.CharField(max_length=50, null=True, blank=True)
    cs_name = models.CharField(max_length=50, null=True, blank=True)
    current_time_zone = models.IntegerField(null=True, blank=True)
    data_execution_prevention_32_bit_applications = models.BooleanField(null=True, blank=True)
    data_execution_prevention_available = models.BooleanField(null=True, blank=True)
    data_execution_prevention_drivers = models.BooleanField(null=True, blank=True)
    encryption_level = models.IntegerField(null=True, blank=True)
    install_date = models.CharField(max_length=50, null=True, blank=True)
    last_boot_up_time = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)
    max_number_of_processes = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    number_of_processes = models.IntegerField(null=True, blank=True)
    number_of_users = models.IntegerField(null=True, blank=True)
    operating_system_sku = models.IntegerField(null=True, blank=True)
    os_architecture = models.CharField(max_length=20, null=True, blank=True)
    os_language = models.IntegerField(null=True, blank=True)
    os_product_suite = models.IntegerField(null=True, blank=True)
    os_type = models.IntegerField(null=True, blank=True)
    primary = models.BooleanField(null=True, blank=True)
    serial_number = models.CharField(max_length=50, null=True, blank=True)
    size_stored_in_paging_files = models.CharField(max_length=50, null=True, blank=True)
    system_device = models.CharField(max_length=50, null=True, blank=True)
    system_directory = models.CharField(max_length=100, null=True, blank=True)
    system_drive = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        db_table = 'os_info'


class Partition(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='partitions')
    block_size = models.CharField(max_length=30, null=True, blank=True)
    caption = models.CharField(max_length=50, null=True, blank=True)
    creation_class_name = models.CharField(max_length=50, null=True, blank=True)
    device_id = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    number_of_blocks = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)
    system_creation_class_name = models.CharField(max_length=50, null=True, blank=True)
    system_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'partition'


class CPU(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='cpus')
    caption = models.CharField(max_length=100, null=True, blank=True)
    device_id = models.CharField(max_length=30, null=True, blank=True)
    manufacturer = models.CharField(max_length=50, null=True, blank=True)
    max_clock_speed = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    socket_designation = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'cpu'


class GPU(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='gpus')
    name = models.CharField(max_length=100, null=True, blank=True)
    current_horizontal_resolution = models.IntegerField(null=True, blank=True)
    current_vertical_resolution = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'gpu'


class Drive(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='drives')
    caption = models.CharField(max_length=50, null=True, blank=True)
    device_id = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    partitions = models.IntegerField(null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'drive'


class Identifier(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='identifiers')
    bios_date = models.CharField(max_length=50, null=True, blank=True)
    bios_vendor = models.CharField(max_length=50, null=True, blank=True)
    bios_version = models.CharField(max_length=30, null=True, blank=True)
    board_name = models.CharField(max_length=50, null=True, blank=True)
    board_serial = models.CharField(max_length=100, null=True, blank=True)
    board_vendor = models.CharField(max_length=50, null=True, blank=True)
    board_version = models.CharField(max_length=50, null=True, blank=True)
    product_uuid = models.CharField(max_length=100, null=True, blank=True)
    gpu = models.ForeignKey('GPU', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    cpu = models.ForeignKey('CPU', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')
    storage_device = models.ForeignKey('StorageDevice', null=True, blank=True, on_delete=models.CASCADE, related_name='identifiers')

    class Meta:
        db_table = 'identifier'


class StorageDevice(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='storage_devices')
    caption = models.CharField(max_length=50, null=True, blank=True)
    model = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'storage_device'
