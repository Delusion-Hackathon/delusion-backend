from .selectors import all_companies
import random
import string


LETTERS = list(string.ascii_lowercase)  


def generate_company_username(name: str=None, extra: list=None) -> str:
    """
    * The function is to create a `company username`. `extra` takes no argument on first call.
    * If the generated `company username` exists in the DB, then the recursion is triggered and a list of random letters is sent to `extra`.
    """
    
    username = name.casefold().replace(' ', '_')
    if (extra): username += '_' + ''.join(extra)
    return username if not all_companies().filter(username=username).exists() \
        else generate_company_username(name, random.choices(LETTERS, k=random.randrange(1, 9)))
