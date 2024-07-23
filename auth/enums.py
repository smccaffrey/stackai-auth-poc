import enum

class OrgRoles(enum.Enum):
    """
    - **Super-admin**: Can see, edit, create, and delete all resources in the organization, regardless of team membership. Can manage users within the organization.
    - **Member**: A regular member of the organization.
    """
    SUPER_ADMIN="super_admin"
    MEMBER="member"

class TeamRoles(enum.Enum):
    """
    - **Admin**: Can manage team members and their roles. Also has editor permissions.
    - **Editor**: Can see and edit team-specific resources. Also has viewer permissions.
    - **Viewer**: Can only see team-specific resources.
    - **External user:** Someone who is not logged in the platform, can only have access to exported resources.
    """
    ADMIN="admin"
    EDITOR="editor"
    VIEWER="viewer"
    EXTERNAL_USER="external_user"
