from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('components', sa.Column('benchmark_scores', sa.JSON(), nullable=True))
    op.add_column('components', sa.Column('composite_score', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('components', 'composite_score')
    op.drop_column('components', 'benchmark_scores')