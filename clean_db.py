"""
Database cleaning script.
This script drops all tables and recreates them for fresh data import.

WARNING: This will delete ALL data in the database!
Use this when you want to start fresh with new CSV data imports.

Usage:
    python clean_db.py              # Interactive mode (asks for confirmation)
    python clean_db.py --force      # Non-interactive mode (no confirmation)
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.database import clean_database as clean_db_function, engine
from sqlalchemy import inspect


def clean_database(force: bool = False):
    """
    Drop all tables and recreate them.
    
    Args:
        force: If True, skip confirmation prompt
    """
    print("=" * 60)
    print("DATABASE CLEANING SCRIPT")
    print("=" * 60)
    print()
    
    # Check if database has tables
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if existing_tables:
        print(f"Found {len(existing_tables)} existing tables:")
        for table in existing_tables:
            print(f"  - {table}")
        print()
        print("⚠️  WARNING: This will DELETE ALL DATA in these tables!")
        print()
        
        if not force:
            response = input("Are you sure you want to proceed? (yes/no): ")
            if response.lower() not in ["yes", "y"]:
                print("Operation cancelled.")
                return
            print()
    else:
        print("No existing tables found.")
        print()
    
    # Drop and recreate all tables, including default levels
    print("Dropping all tables...")
    clean_db_function(create_default_levels=True)
    print("✓ All tables dropped and recreated successfully")
    print("✓ Default levels created successfully")
    
    print()
    print("=" * 60)
    print("Database cleaning completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run import scripts to load vocabulary data:")
    print("   python scripts/import_vocabulary_levels.py")
    print("2. Run import scripts to load quiz sentences:")
    print("   python scripts/import_quiz_sentences_levels.py")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean database by dropping and recreating all tables"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip confirmation prompt (non-interactive mode)"
    )
    args = parser.parse_args()
    
    try:
        clean_database(force=args.force)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
