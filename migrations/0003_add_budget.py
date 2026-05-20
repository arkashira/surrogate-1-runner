"""Add budget table

Revision ID: 0003_add_budget
Revises: 0002_add_organization
Create Date: 2024-05-04 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '0003_add_budget'
down_revision = '0002_add_organization'
branch_labels = None
depends_on = None

def upgrade():
    """Create the budgets table."""
    op.create_table('budgets',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.Column('month', sa.String(length=7), nullable=False),  # Format: YYYY-MM
        sa.Column('limit', sa.Numeric(12, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(('organization_id',), ['organizations.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_budgets_month'), 'budgets', ['month'], unique=False)
    op.create_index(op.f('ix_budgets_organization_id'), 'budgets', ['organization_id'], unique=False)

def downgrade():
    """Drop the budgets table."""
    op.drop_table('budgets')