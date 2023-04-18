"""change_scientometric_database_nullble

Revision ID: 41e87100a92e
Revises: 4d403b4c9088
Create Date: 2023-04-18 10:55:28.177884

"""
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '41e87100a92e'
down_revision = '4d403b4c9088'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'scientometric_database',
                    existing_type=postgresql.ENUM('scopus', 'wos', 'risc', name='scientometric_status'),
                    nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'scientometric_database',
                    existing_type=postgresql.ENUM('scopus', 'wos', 'risc', name='scientometric_status'),
                    nullable=False)
    # ### end Alembic commands ###
