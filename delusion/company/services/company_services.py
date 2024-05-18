from rest_framework.exceptions import ValidationError
from ..selectors import all_companies
from ..models import Company, Worker
from ..utils import generate_company_username
from delusion.services import WebSocketClient
from delusion.company import OK


def create_worker(
    *,
    user: object,
    company: object
) -> Worker:
    """
    * Function to create a worker.
    """
    obj = Worker.objects.create(
        user=user,
        company=company
    )
    return obj


def create_company(
    user,
    *,
    mesh_username: str,
    mesh_password: str,
    name: str=None,
    description: str=None,
    parent_company: object=None
) -> Company:
    """
    * The function is called by `signal`.
    * Creates a new group in `MeshCentral` based on data sent via a new `WebSocketClient` object.
    * Finally, a new company is created in `DB`.
    """

    username = generate_company_username(name)

    wss = WebSocketClient(mesh_username, mesh_password)
    wss.connect()
    wss.create_new_group(company_name=username, desc=description)
    last_message = wss.last_message
    wss.close()

    result, mesh_id= last_message.get('result'), last_message.get('meshid')
    if (result != OK or mesh_id is None):
        raise ValidationError({'detail': 'An unexpected error occurred'})

    obj = Company.objects.create(
        username=username,
        mesh_id=mesh_id,
        name=name,
        description=description,
        parent_company=parent_company
    )
    create_worker(user=user, company=obj)
    return obj


def update_company(instance, **data) -> Company:
    """
    * The function updates the information of the respective company based on the information sent.
    """
    
    obj = all_companies().filter(id=instance.id).update(**data)
    return obj


def delete_company(instance) -> None:
    """
    * The function checks the presence of devices belonging to the company. If there are no devices, then it deletes the company.
    """
    
    if (instance.nodes.exists()): raise ValidationError({'detail': 'There are devices belonging to the company you want to delete. Move them to a different company first.'})
    instance.delete()
    return None
