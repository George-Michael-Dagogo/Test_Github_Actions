from get_data import get_article_data

df = get_article_data()
print(df)



# Define your Azure PostgreSQL connection details
    USERNAME = "testtech"
    PASSWORD = "Your_password"
    HOST = "testtech.postgres.database.azure.com"
    PORT = "5432"  # Default PostgreSQL port
    DATABASE = "postgres"

    # Create the database connection URL
    DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

    # Create an SQLAlchemy engine
    engine = create_engine(DATABASE_URL)



    # Push DataFrame to Azure PostgreSQL
    df.to_sql("player_table", engine, if_exists="append", index=False)

    print("Data pushed successfully!")
