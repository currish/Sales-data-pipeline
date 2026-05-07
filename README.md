# Sales Data Pipeline

## Project Overview

This project is an end-to-end data pipeline built using python, PostgreSQL, SQL and docker

Operations performed by the pipeline:
- Data Ingestion from csv file called assignment_dataset.csv

- Data Cleaning and validation in clean.py

- Revenue calculation by adding gross revenue column which is unit Price * quantity

- Then Loaded the cleaned dataset using Load.py in Postgres in sales database, in sales_db container present in Docker. Stored this cleaned dataset in table called sales_raw

- Aggregated sales analytics in sales database by creating three tables, daily_sales, monthly_sales and top_items from sales_raw table

## Tech Stack Used

- Python

- Pandas

- PostgreSQL

- SQLAlchemy

- Docker

- SQL

- Github


## Docker Setup

You need to first download Docker if you dont have one in your PC. You need to go to this site https://www.docker.com/products/docker-desktop/  and click  on download Docker Desktop as shown below to download it.

![alt text](image-3.png)

In some cases, you might face an error while installing Docker called   “C:\ProgramData\DockerDesktop must be owned by an elevated account”. 

To resolve this issue, you need to follow the steps in this youtube video tutorial link 
https://www.youtube.com/watch?v=uv9Le1THeeY to resolve this issue.


Sales database is contained inside the container called sales_db inside the docker

docker-compose.yml is used under the docker section in this project, which basically crerates and run a PostgresSQL container (Sales_db) that contains the database Sales. Given below is how the configuration of the Yml file looks like:-

![alt text](image-2.png)


What this configuration does is that  it creates a container called sales_db where the database created inside this container will be sales and this will be running on port 5432. The volume configuration ensures that PostGresql table remains available even after restarting the docker container

# Steps to run the code from Github
## How Another User Can Run This Project from GitHub

A user can run this project locally by following the steps below.

Step 0: Install Docker Desktop

- Download and install Docker Desktop from the official Docker website: https://www.docker.com/products/docker-desktop/ 

After installation:

- Open Docker Desktop. If it is not opening, then please refer to this youtube link https://www.youtube.com/watch?v=uv9Le1THeeY to resolve this issue.


- Wait until Docker shows:
        Docker is running


Step 1: Clone the GitHub Repository

Run  git clone https://github.com/currish/Sales-data-pipeline.git in cmd or simply go to the above link and download the zip file by clicking on code, which is the Green button. Then extract the zip file and open it using visual studio code 
                          
![alt text](image-7.png)


Step 2: Navigate to the Project Folder in the terminal then type cd Sales-data-pipeline-main. The output should look like this in the terminal:-

![alt text](image-8.png)





Step 3: Verify Docker Installation

Run on terminal inside visual studio code: docker --version

![alt text](image-9.png)
  



Step 4: Install Python Dependencies

Run on terminal inside visual studio code:  pip install -r requirements.txt

![alt text](image-10.png)

Step 5: Run the container inside the docker

Go inside docker using cd docker from the present path and run docker-compose up -d to start the container sales_db inside the docker

![alt text](image-13.png)

Step 6:  Run the Pipeline.py

Do cd.. to return to the previous path (Sales-data-pipeline-main path) and run inside terminal python src/pipeline.py

![alt text](image-11.png)


Step 7: Validate Output Tables

- Make sure you are in the Sales-data-pipeline-main path. Run on terminal inside visual studio code from Sales-data-pipeline-main path :docker ps

![alt text](image-12.png)

- Then run docker exec -it sales_db psql -U postgres -d sales from the same path

![alt text](image-22.png)

- You will be present inside the database called as sales as shown below

![alt text](image-15.png)

- Then enter \dt to see the Expected tables: sales_raw ,daily_sales, monthly_sales and top_items

![alt text](image-16.png)
        
- Then Run inside the sales database

  Run : select * from sales_raw;

![alt text](image-18.png)

  Run : select * from daily_sales;

![alt text](image-19.png)  

  Run : select * from monthly_sales;

![alt text](image-20.png)  

  Run : select * from top_items;

![alt text](image-21.png)  

- As you can see, we can see the analytical datasets in the output, which means pipelining process has been done successfully !


## test_connection.py

I just created a test_connection.py to basically validate that PostgreSQL is connected with the python code before running the pipeline properly. 
The code is as shown below:-

                from sqlalchemy import create_engine

                engine = create_engine("postgresql://postgres:postgres@localhost:5432/sales")

                try:
                        conn = engine.connect()
                        print("Connection successful!")
                        conn.close()

                except Exception as e:
                        print("Connection Failed:", e)



I ran it and here it is showing the output

![alt text](image.png)

This means that the connection is successful and we are now ready to create the pipeline and run it !

## Pipeline Creation and Execution

Before creating the pipeline , it is important for us to first load the assignment dataset and clean it first

Thats why examine  clean.py first.

### Clean.py
What this clean.py is reponsible is :-

- Loading the datset inside the function clean_data(path)
        print("\nReading CSV Data")
    
        df = pd.read_csv(path)

- Handling Duplicates if it exists, there wasnt any duplicate rows though 
print("\nChecking Duplicate Rows")
    
        duplicate_rows = df.duplicated().sum()
        print("Total exact duplicate rows:", duplicate_rows)

- Check number of null values in each of the columns in this dataset. we found out Category and Discount had lot of null values    
    
        null_counts = df.isnull().sum()
        print("Total number of null countts are:",null_counts)

-  Replaced null values in Category with category mapping ie for item_names Laptop, TV, Phone, we replaced thier null values with Electronics. Similarly for item_names Chair and Table, we replaced their null values with Furniture. We also Standardized the values so that any lower case (electronics) is replaced with  Electronics respectively.

        df.loc[df["category"].isna(), "category"] = df["item_name"].map(category_map)
        df["category"] = df["category"].str.strip().str.title()

- Replaced Negative values in quantity with 0 as shown below
    
        df["quantity"] = df["quantity"].clip(lower=0)
        print(df["quantity"])

- Calculated total_amount_Corrected column which is Unit Price * quantity. Since Quantity does not have any negative values and its lowest value is 0, I have created a new column called  total_amount_Corrected and it does not have any negative values, its lowest values is 0

        df["total_amount_corrected"] = (df["quantity"] * df["unit_price"] -df["discount"]).clip(lower=0)

- Calculated Gross Revenue column which is basically quantity * unit price for each of the items in the dataset
        
        df["gross_revenue"] = df["unit_price"] * df["quantity"]

-  I also used print(df.dtypes) to check what the datatypes of each of the columns are. I noticed that billing_date column had string datatype instead of Datetime format. So, used the below code to convert it into a datetime format in dd-mm-yyyy format
        
        df["billing_date"] = pd.to_datetime(df["billing_date"],
        dayfirst = True)

So basically, this function will be called in pipeline.py and first step of data cleaning process will be performed        

After examining clean.py, we examine load.py

        from sqlalchemy import create_engine

        def load_data(df):
            engine = create_engine("postgresql://postgres:postgres@localhost:5432/sales")

            print("\n Loading data into Postgres")
            df.to_sql("sales_raw", engine, if_exists="replace", index=False)

            print("Data successfully loaded into sales_raw table")

What this code does is it basically creates engine to connect to postgres in port 5432 in Docker, which contains the sales database inside sales_db container.

Then it will load the cleaned dataset df (which was cleaned before in clean.py) in the Sales database and sales_raw table will be created and used to store this cleaned dataset

### Transform.sql

Transform.sql is just used as a sql query notebook, which will be used inside the postgres to query raw_sales table inside the Sales database in Sales_Db container
    
        -- Daily Sales
        Drop table if exists daily_sales;

        create table daily_sales as 
        select 
        billing_date as date,
        sum(gross_revenue) as total_revenue,
        sum(total_amount_corrected) AS total_corrected_amount
        from sales_raw
        group by billing_date;    

The above query basically creates daily_sales table from sales_raw, where it aggregates gross_revenue and total_amount_Corrected columns grouped by billing_date

        -- Monthly Sales
        drop table if exists monthly_sales;

        create table monthly_sales as 
        select date_trunc('month', billing_date) as month,
        sum(gross_revenue) as total_revenue,
        sum(total_amount_corrected) AS total_corrected_amount
        from sales_raw
        group by date_trunc('month', billing_date);


The above query basically creates monthly_sales table from sales_raw, where it aggregates gross_revenue and total_amount_Corrected columns grouped by month

        -- Top Items by Revenue
        drop table if exists top_items;

        create table top_items as 
        select item_name,
        sum(gross_revenue) as total_revenue,
        sum(total_amount_corrected) AS total_corrected_amount
        from sales_raw
        group by item_name
        order by sum(gross_revenue) desc;

The above query basically creates top_items table from sales_raw (Highest to lowest based on gross revenue), where it gross_revenue and total_amount_Corrected columns grouped by item_name and orders it by its sum of gross_revenue in the descending order

### pipeline.py
As each individual componenets are discussed, now we discuss about pipeline.py. Given below is the code:-

        from clean import clean_data
        from load import load_data
        from sqlalchemy import create_engine, text

        def run_pipeline():

            print("\nSTARTING PIPELINE")

            path = "data/assignment_dataset.csv"

            print("\nCLEANING DATA")
            df = clean_data(path)

            print("\nLOADING DATA")
            load_data(df)

            print("\nRUNNING SQL TRANSFORMATIONS")
            engine = create_engine("postgresql://postgres:postgres@localhost:5432/sales")

            with open("src/transform.sql", "r") as f:
            sql = f.read()

            with engine.begin() as conn:
            conn.execute(text(sql))

            print("\nPIPELINE COMPLETED SUCCESSFULLY")


        if __name__ == "__main__":
            run_pipeline()

It acts as the main orchestration file for the entire pipeline. 

- It basically calls the function inside clean.py (def clean_data(path)) to clean the given dataset

- Then it calls the function inside load.py (def load_data(df)), which loads the cleaned dataset df and loads the data into the sales_raw table inside Postgres in Docker

- Then it connects to postgres inside ddocker and uses transform.sql to run sql queries to create three analytical datasets or tables as asked by this assignment, which are daily_sales, monthly_sales and top_items

This is how the output looks like:-

Daily_sales output

![alt text](image-4.png)

Monthly sales output

![alt text](image-5.png)

Top items output

![alt text](image-6.png)









