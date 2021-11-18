def create_tables(app, db):
    from app.udaconnect import create_tables as create_database_tables

    create_database_tables(app, db)