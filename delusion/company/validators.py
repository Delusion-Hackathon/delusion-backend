import os
import magic

from django.core.exceptions import ValidationError


def validate_file_mimetype(file):
    accept = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf', 'text/plain', 'text/log']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in accept:
        raise ValidationError(f'File type {file_mime_type} not supported')

def validate_file_extension(uploaded_file):
    allowed_extensions = ['.txt', '.pdf', '.jpg', '.jpeg', '.png', '.log']
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    if file_extension not in allowed_extensions:
        raise ValidationError(f"File with extension {file_extension} is not allowed.")
