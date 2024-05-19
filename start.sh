#!/bin/bash

# Bekleme işlemi (örneğin, PostgreSQL sunucusunun hazır olduğunu kontrol edin)
python wait_for_postgres.py

# Veritabanını migre edin
./manage.py migrate

# Django sunucusunu başlatın
./manage.py runserver 0.0.0.0:8000
