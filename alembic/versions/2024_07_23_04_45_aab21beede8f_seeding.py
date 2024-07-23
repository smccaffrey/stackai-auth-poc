# type: ignore
"""seeding

Revision ID: aab21beede8f
Revises: 00f2d1ffc2bd
Create Date: 2024-07-23 04:45:54.738583+00:00

"""
# pylint: skip-file

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Enum

from auth.enums import *
from auth.db.type_utils import *





# revision identifiers, used by Alembic.
revision = 'aab21beede8f'
down_revision = '00f2d1ffc2bd'
branch_labels = None
depends_on = None



def upgrade():
    # Create a table reference for bulk insert
    user_table = table('users',
        column('id', Integer),
        column('name', String)
    )
    
    org_table = table('organizations',
        column('id', Integer),
        column('name', String)
    )

    team_table = table('teams',
        column('id', Integer),
        column('name', String),
        column('organization_id', Integer)
    )
    
    user_organizations_table = table('user_organizations',
        column('user_id', Integer),
        column('organization_id', Integer),
        column('role', EnumAsString(OrgRoles))
    )

    user_teams_table = table('user_teams',
        column('user_id', Integer),
        column('team_id', Integer),
        column('role', EnumAsString(TeamRoles))
    )
    
    # Insert test data
    op.bulk_insert(user_table,
        [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 3, 'name': 'Charlie'},
            {'id': 4, 'name': 'Dave'},
        ]
    )
    
    op.bulk_insert(org_table,
        [
            {'id': 1, 'name': 'Org1'},
            {'id': 2, 'name': 'Org2'}
        ]
    )
    
    op.bulk_insert(team_table,
        [
            {'id': 1, 'name': 'Team1', 'organization_id': 1},
            {'id': 2, 'name': 'Team2', 'organization_id': 2},
            {'id': 3, 'name': 'Team3', 'organization_id': 1}
        ]
    )
    
    op.bulk_insert(user_organizations_table,
        [
            {'user_id': 1, 'organization_id': 1, 'role': OrgRoles.SUPER_ADMIN},
            {'user_id': 1, 'organization_id': 2, 'role': OrgRoles.MEMBER},
            {'user_id': 2, 'organization_id': 1, 'role': OrgRoles.MEMBER},
            {'user_id': 3, 'organization_id': 2, 'role': OrgRoles.MEMBER},
            {'user_id': 4, 'organization_id': 2, 'role': OrgRoles.SUPER_ADMIN}
        ]
    )
    
    op.bulk_insert(user_teams_table,
        [
            {'user_id': 1, 'team_id': 1, 'role': TeamRoles.ADMIN},
            {'user_id': 1, 'team_id': 2, 'role': TeamRoles.VIEWER},
            {'user_id': 2, 'team_id': 1, 'role': TeamRoles.EDITOR},
            {'user_id': 3, 'team_id': 2, 'role': TeamRoles.VIEWER},
            {'user_id': 4, 'team_id': 2, 'role': TeamRoles.ADMIN},
            {'user_id': 2, 'team_id': 3, 'role': TeamRoles.VIEWER}
        ]
    )

def downgrade():
    # Deleting the test data
    op.execute("DELETE FROM user_teams WHERE user_id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM user_organizations WHERE user_id IN (1, 2, 3, 4)")
    op.execute("DELETE FROM teams WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM organizations WHERE id IN (1, 2)")
    op.execute("DELETE FROM users WHERE id IN (1, 2, 3, 4)")