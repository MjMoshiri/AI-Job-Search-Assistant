"""Remove is_a_match_ and is_duplicated columns

Revision ID: 6e645f1bdbc2
Revises: 
Create Date: 2024-05-20 13:51:14.149414

"""
from typing import Sequence, Union
from sqlalchemy import text
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e645f1bdbc2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('job_applications', 'is_a_match')
    op.drop_column('job_applications', 'is_duplicate')
    op.alter_column('job_applications', 'website', new_column_name='link')
    op.execute(
        text(
            """
            UPDATE job_applications
            SET link = CONCAT('https://www.indeed.com/viewjob?jk=', id)
            """
        )
    )
def downgrade():
    op.add_column('job_applications', sa.Column('is_a_match', sa.Boolean(), nullable=True))
    op.add_column('job_applications', sa.Column('is_duplicate', sa.Boolean(), nullable=True))
    op.alter_column('job_applications', 'link', new_column_name='website')
