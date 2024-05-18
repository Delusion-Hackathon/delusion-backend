from decouple import config
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from delusion.services import WebSocketClient
from delusion.users.models import MeshUser
from delusion.company.selectors import all_companies
from .pc_user_services import create_pc_users
from ..choices import AntiVirusChoices
from ..models import Node
from .. import *


def get_url(
    user,
    *,
    option: int=None,
    company_name: str=None
) -> str:
    """
    * A function that `loads the agent` and returns the `url` at the end.
    """

    company = all_companies().filter(username=company_name).last()
    if (not company): raise ValidationError({'detail': 'Company not found'})
    mesh_id = company.get_mesh_id

    if (option == WIN_32): url = f"{config('MESH_URL')}/meshagents?id={WIN_32}&meshid={mesh_id}&installflags=0"
    elif (option == WIN_64): url = f"{config('MESH_URL')}/meshagents?id={WIN_64}&meshid={mesh_id}&installflags=0"
    elif (option == WIN_ARM): url = f"{config('MESH_URL')}/meshagents?id={WIN_ARM}&meshid={mesh_id}&installflags=0"
    elif (option == LBM_BINARY): url = f"{config('MESH_URL')}/meshagents?id={mesh_id}&installflags=0&meshinstall=6"
    elif (option == MAC): url = f"{config('MESH_URL')}/meshosxagent?id={MAC}&meshid={mesh_id}"
    elif (option == MESH_ASSISTANT): url = f"{config('MESH_URL')}/meshagents?id={MESH_ASSISTANT}&meshid={mesh_id}&ac=2"
    elif (option == MOBILE): url = f"{config('MESH_URL')},52Ahk0MDK0hEBL6LU6m7iwa2HccqO$pCk2dQXrmyISUPC2pwz1ntQ3qCSCxK8mS8,{mesh_id}"
    elif (option == LB): url = f"""(wget "{config('MESH_URL')}/meshagents?script=1" --no-check-certificate -O ./meshinstall.sh || wget "{config('MESH_URL')}/meshagents?script=1" --no-proxy --no-check-certificate -O ./meshinstall.sh) && chmod 755 ./meshinstall.sh && sudo -E ./meshinstall.sh {config('MESH_URL')} '{mesh_id}' || ./meshinstall.sh {config('MESH_URL')} '{mesh_id}'"""
    else: raise ValidationError({'detail': 'Invalid option'})

    return url


def create_node(
    user,
    *,
    mesh_id: str=None,
    node_id: str=None,
    name: str=None,
    domain: str=None,
    host: str=None,
    pc_users: list=[],
    os_desc: str=None,
    ip: str=None,
    antivirus: AntiVirusChoices=None,
    auto_update: bool=True,
    firewall: bool=True
) -> Node:
    """
    * A function that creates a node object that also stores the data of the remote computer based on the sent data.
    """

    if (not node_id): raise ValidationError({'detail': 'Enter the node_id'})
    company = get_object_or_404(all_companies(), mesh_id=mesh_id)
    node_obj = Node.objects.create(
        company=company,
        node_id=node_id,
        name=name,
        domain=domain,
        host=host,
        os_desc=os_desc,
        ip=ip,
        antivirus=antivirus,
        auto_update=auto_update,
        firewall=firewall
    )
    pc_users = create_pc_users(pc_users=pc_users)
    if (pc_users != []): node_obj.pc_users.set(pc_users)

    ...
    #== Ardı İlkin bəydən sonra ==#

    return node_obj
