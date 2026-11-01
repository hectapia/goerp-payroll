# Database Migrations with flask-alembic

This document describes how to use flask-alembic for database migrations in goerp-payroll.

## Overview

flask-alembic is now integrated into goerp-payroll to manage database schema changes in a versioned and controlled manner. Migrations are stored in `goerp_payroll/migrations/`.

## CLI Commands

### Apply Migrations

```bash
# Apply all pending migrations to the latest version
flask database migrate

# Or use the alias:
flask database upgrade
```

### Check Current Version

```bash
# Display the current migration version of the database
flask database current
```

### Rollback Migrations

```bash
# Rollback one migration
flask database downgrade -1

# Rollback to a specific revision
flask database downgrade <revision_id>

# Rollback all migrations
flask database downgrade base
```

### Mark Database Version

```bash
# Mark database as up-to-date without running migrations
flask database stamp head

# Mark database at a specific revision
flask database stamp <revision_id>
```

## Auto-Migration

Enable automatic migrations on application startup by setting the environment variable:

```bash
export COATI_AUTO_MIGRATE=1
```

**Note**: Auto-migration is recommended for development only. In production, run migrations manually before deployment.

## Migration Workflow

### For New Installations

1. Initialize the database:
   ```bash
   flask database init
   ```

2. Mark the database as up-to-date:
   ```bash
   flask database stamp head
   ```

3. Verify the current version:
   ```bash
   flask database current
   ```

### For Existing Databases

If you have an existing database before flask-alembic was implemented:

1. Mark your current database state:
   ```bash
   flask database stamp head
   ```

2. Future migrations can now be applied:
   ```bash
   flask database migrate
   ```

### Creating New Migrations

When you need to modify the database schema:

1. Update your SQLAlchemy models in `goerp_payroll/model.py`

2. Create a new migration file in `goerp_payroll/migrations/` following the naming convention:
   ```
   YYYYMMDD_HHMMSS_description.py
   ```
   For example: `20260125_150000_add_user_profile_field.py`

3. Use the template from `script.py.mako` or copy an existing migration

4. Implement `upgrade()` and `downgrade()` functions

5. Test the migration on a development database:
   ```bash
   flask database upgrade
   flask database downgrade -1
   flask database upgrade
   ```

## Best Practices

1. **Always verify before creating**: Check if tables/columns exist before creating them to make migrations idempotent
2. **Use server defaults**: When adding NOT NULL columns, always provide a `server_default`
3. **Test both directions**: Always test both `upgrade()` and `downgrade()` functions
4. **Keep migrations small**: One logical change per migration file
5. **Document changes**: Include clear docstrings explaining what the migration does

## Testing

Run the migration tests to verify everything works:

```bash
pytest tests/test_alembic_migrations.py -v
```

## Troubleshooting

### "No migration version found"

The database needs to be stamped first:
```bash
flask database stamp head
```

### "Can't locate revision"

Verify that all migration files are in `goerp_payroll/migrations/` and follow the correct naming convention.

### Database out of sync

If your database schema doesn't match the migrations:
1. Backup your data
2. Either: Update migrations to match current schema, or
3. Drop and recreate the database with `flask database init`

## Example Migration

```python
"""Add user profile field

Revision ID: 20260125_150000
Revises: 20260125_032900
Create Date: 2026-01-25 15:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = '20260125_150000'
down_revision = '20260125_032900'
branch_labels = None
depends_on = None


def upgrade():
    """Add profile field to usuario table."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if "usuario" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("usuario")]
        
        if "profile" not in columns:
            op.add_column(
                "usuario",
                sa.Column("profile", sa.Text(), nullable=True)
            )


def downgrade():
    """Remove profile field from usuario table."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    
    if "usuario" in inspector.get_table_names():
        columns = [col["name"] for col in inspector.get_columns("usuario")]
        
        if "profile" in columns:
            op.drop_column("usuario", "profile")
```

## Additional Resources

- [flask-alembic documentation](https://github.com/davidism/flask-alembic)
- [Alembic documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy documentation](https://docs.sqlalchemy.org/)
