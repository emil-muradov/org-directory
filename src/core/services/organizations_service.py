from persistence.db.repositories import OrganizationsRepository


class OrganizationsService:
    def __init__(self, organizations_repository: OrganizationsRepository):
        self._organizations_repository = organizations_repository
