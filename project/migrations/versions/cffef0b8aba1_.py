"""empty message

Revision ID: cffef0b8aba1
Revises: cf8b86182eb8
Create Date: 2017-09-18 14:05:32.968000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cffef0b8aba1'
down_revision = 'cf8b86182eb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animes', sa.Column('genres', sa.String(length=100), nullable=True))
    op.drop_constraint(u'genres_ibfk_1', 'genres', type_='foreignkey')
    op.drop_column('genres', 'anime_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('genres', sa.Column('anime_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key(u'genres_ibfk_1', 'genres', 'animes', ['anime_id'], ['id'])
    op.drop_column('animes', 'genres')
    # ### end Alembic commands ###