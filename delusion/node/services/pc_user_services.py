from ..models import PCUser


def create_pc_users(*, pc_users) -> list:
    data = []
    if (pc_users): 
        for user in pc_users:
            pc_user_obj = PCUser.objects.create(name=user)
            data.append(pc_user_obj)
    return data
