"""initial

Revision ID: 9d37c22e257e
Revises: 
Create Date: 2023-04-19 01:31:22.766909

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9d37c22e257e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
                    sa.Column('guid', sa.UUID(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('scientometric_database', sa.Enum('scopus', 'wos', 'risc', name='scientometric_status'),
                              nullable=True),
                    sa.Column('document_count', sa.Integer(), server_default='0', nullable=True),
                    sa.Column('citation_count', sa.Integer(), server_default='0', nullable=True),
                    sa.Column('h_index', sa.Integer(), server_default='0', nullable=True),
                    sa.Column('url', sa.String(), nullable=True),
                    sa.Column('created_at', sa.Integer(), server_default=sa.text('EXTRACT(epoch FROM now())'),
                              nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###