# Generated by Django 4.2.1 on 2023-10-20 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=100, null=True)),
                ('device_id', models.CharField(blank=True, max_length=30, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True)),
                ('max_clock_speed', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('socket_designation', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'cpu',
            },
        ),
        migrations.CreateModel(
            name='GPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('current_horizontal_resolution', models.IntegerField(blank=True, null=True)),
                ('current_vertical_resolution', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'gpu',
            },
        ),
        migrations.CreateModel(
            name='PCUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'pc_user',
            },
        ),
        migrations.AddField(
            model_name='node',
            name='antivirus',
            field=models.CharField(blank=True, choices=[('l', 'Low'), ('m', 'Medium'), ('h', 'High')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='auto_update',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='node',
            name='domain',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='firewall',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='node',
            name='host',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='ip',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='node',
            name='os_desc',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='node_id',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='StorageDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_devices', to='node.node')),
            ],
            options={
                'db_table': 'storage_device',
            },
        ),
        migrations.CreateModel(
            name='Partition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_size', models.CharField(blank=True, max_length=30, null=True)),
                ('caption', models.CharField(blank=True, max_length=50, null=True)),
                ('creation_class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('device_id', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('number_of_blocks', models.CharField(blank=True, max_length=50, null=True)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('system_creation_class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('system_name', models.CharField(blank=True, max_length=100, null=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partitions', to='node.node')),
            ],
            options={
                'db_table': 'partition',
            },
        ),
        migrations.CreateModel(
            name='OSInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boot_device', models.CharField(blank=True, max_length=100, null=True)),
                ('build_number', models.CharField(blank=True, max_length=30, null=True)),
                ('build_type', models.CharField(blank=True, max_length=50, null=True)),
                ('caption', models.CharField(blank=True, max_length=50, null=True)),
                ('code_set', models.CharField(blank=True, max_length=30, null=True)),
                ('country_code', models.CharField(blank=True, max_length=10, null=True)),
                ('creation_class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cs_creation_class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('cs_name', models.CharField(blank=True, max_length=50, null=True)),
                ('current_time_zone', models.IntegerField(blank=True, null=True)),
                ('data_execution_prevention_32_bit_applications', models.BooleanField(blank=True, null=True)),
                ('data_execution_prevention_available', models.BooleanField(blank=True, null=True)),
                ('data_execution_prevention_drivers', models.BooleanField(blank=True, null=True)),
                ('encryption_level', models.IntegerField(blank=True, null=True)),
                ('install_date', models.CharField(blank=True, max_length=50, null=True)),
                ('last_boot_up_time', models.CharField(blank=True, max_length=50, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True)),
                ('max_number_of_processes', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('number_of_processes', models.IntegerField(blank=True, null=True)),
                ('number_of_users', models.IntegerField(blank=True, null=True)),
                ('operating_system_sku', models.IntegerField(blank=True, null=True)),
                ('os_architecture', models.CharField(blank=True, max_length=20, null=True)),
                ('os_language', models.IntegerField(blank=True, null=True)),
                ('os_product_suite', models.IntegerField(blank=True, null=True)),
                ('os_type', models.IntegerField(blank=True, null=True)),
                ('primary', models.BooleanField(blank=True, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=50, null=True)),
                ('size_stored_in_paging_files', models.CharField(blank=True, max_length=50, null=True)),
                ('system_device', models.CharField(blank=True, max_length=50, null=True)),
                ('system_directory', models.CharField(blank=True, max_length=100, null=True)),
                ('system_drive', models.CharField(blank=True, max_length=100, null=True)),
                ('version', models.CharField(blank=True, max_length=30, null=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='os_infos', to='node.node')),
            ],
            options={
                'db_table': 'os_info',
            },
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_label', models.CharField(blank=True, max_length=50, null=True)),
                ('capacity', models.CharField(blank=True, max_length=50, null=True)),
                ('caption', models.CharField(blank=True, max_length=50, null=True)),
                ('creation_class_name', models.CharField(blank=True, max_length=50, null=True)),
                ('data_width', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=50, null=True)),
                ('device_locator', models.CharField(blank=True, max_length=30, null=True)),
                ('max_voltage', models.IntegerField(blank=True, null=True)),
                ('min_voltage', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('part_number', models.CharField(blank=True, max_length=100, null=True)),
                ('serial_number', models.CharField(blank=True, max_length=50, null=True)),
                ('sm_bios_memory_type', models.IntegerField(blank=True, null=True)),
                ('speed', models.IntegerField(blank=True, null=True)),
                ('tag', models.CharField(blank=True, max_length=50, null=True)),
                ('total_width', models.IntegerField(blank=True, null=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memories', to='node.node')),
            ],
            options={
                'db_table': 'memory',
            },
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bios_date', models.CharField(blank=True, max_length=50, null=True)),
                ('bios_vendor', models.CharField(blank=True, max_length=50, null=True)),
                ('bios_version', models.CharField(blank=True, max_length=30, null=True)),
                ('board_name', models.CharField(blank=True, max_length=50, null=True)),
                ('board_serial', models.CharField(blank=True, max_length=100, null=True)),
                ('board_vendor', models.CharField(blank=True, max_length=50, null=True)),
                ('board_version', models.CharField(blank=True, max_length=50, null=True)),
                ('product_uuid', models.CharField(blank=True, max_length=100, null=True)),
                ('cpu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='node.cpu')),
                ('gpu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='node.gpu')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='node.node')),
                ('storage_device', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='node.storagedevice')),
            ],
            options={
                'db_table': 'identifier',
            },
        ),
        migrations.AddField(
            model_name='gpu',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gpus', to='node.node'),
        ),
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(blank=True, max_length=50, null=True)),
                ('device_id', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=100, null=True)),
                ('partitions', models.IntegerField(blank=True, null=True)),
                ('size', models.CharField(blank=True, max_length=50, null=True)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='node.node')),
            ],
            options={
                'db_table': 'drive',
            },
        ),
        migrations.AddField(
            model_name='cpu',
            name='node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cpus', to='node.node'),
        ),
        migrations.AddField(
            model_name='node',
            name='pc_users',
            field=models.ManyToManyField(related_name='nodes', to='node.pcuser'),
        ),
    ]
