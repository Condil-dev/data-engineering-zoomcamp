#!/usr/bin/env python
# coding: utf-8

import os 

from time import time

import pandas as pd

from sqlalchemy import create_engine

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    par_name = 'output'
    
    #download csv

    os.system(f'wget {url} -O {par_name}') 

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    engine.connect()

    df_par = pd.read_parquet(par_name)
    df_par.to_csv('csv_name')
    df_iter = pd.read_csv('csv_name',iterator=True,chunksize=100000)
    
    df = next(df_iter) 
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.head(n=100000).to_sql(name=table_name, con=engine, if_exists='replace')
    
    while True:
        t_start = time()
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.to_sql(name=table_name, con=engine, if_exists = 'append')
        t_end = time()
        print("inserting another chunk,took %.3f second" % (t_end - t_start))


if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser(description='Ingest CSV into postgres')

    parser.add_argument('--user', help="database username")
    parser.add_argument('--password', help="database password")
    parser.add_argument('--host', help="database host")
    parser.add_argument('--port', help="database port")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table_name', help="table name in postgres")
    parser.add_argument('--url',help='url of the data')

    args = parser.parse_args()
    
    main(args)

