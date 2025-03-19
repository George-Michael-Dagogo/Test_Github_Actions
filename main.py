from get_data import get_article_data
import pandas as pd
import psycopg2
import os



df = get_article_data()



df.columns = [x.lower() for x in df.columns]
df.columns = [x.replace(' ','_') for x in df.columns]
df['reading_time'] = df['reading_time'].str.replace(' min read','')
df['article_content'] = df['article_content'].str.replace('\n','')


df = df.astype({
    'link': 'string',
    'title': 'string',
    'time_uploaded': 'string',  # Can be converted to datetime later
    'author': 'string',
    'tags': 'string',
    'reading_time': 'int64',
    'article_content': 'string',
    'word_count': 'int64',
    'sentiment': 'string',
    'compound_score': 'float64'
})


df['time_uploaded'] = pd.to_datetime(df['time_uploaded'])




# Database connection parameters
db_params = {
    "dbname": "postgres",
    "user": "testtech",
    "password": os.getenv("DB_PASSWORD"),
    "host": "testtech.postgres.database.azure.com",
    "port": "5432"
}


try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    # SQL Insert Query
    insert_query = """
    INSERT INTO michael (link, title, time_uploaded, author, tags, reading_time, article_content, word_count, sentiment, compound_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (link) DO NOTHING;  -- Avoids duplicate primary key errors
    """
    
    # Insert DataFrame records one by one
    for _, row in df.iterrows():
        cursor.execute(insert_query, (
            row['link'], row['title'], row['time_uploaded'], row['author'], row['tags'],
            row['reading_time'], row['article_content'], row['word_count'], row['sentiment'], row['compound_score']
        ))

    # Commit and close
    conn.commit()
    print("Data inserted successfully!")

except Exception as e:
    print("Error:", e)

finally:
    if conn:
        cursor.close()
        conn.close()




#"password": os.getenv("DB_PASSWORD")
