# E-commerce Analytics

## Language

This README is written in English. A Portuguese summary is available at the end of the document.

Este README está em inglês. Um resumo em português está disponível ao final do documento.

## Overview

This project explores transactional data from the Brazilian e-commerce marketplace **Olist**, covering orders between 2016 and 2018.

The objective is to perform an end-to-end data analysis focused on business insights, including:

* Commercial performance
* Customer behavior
* Revenue distribution
* Retention patterns

The project combines **SQL, Python, and data modeling** to simulate a real-world analytics workflow.

---

## Project Structure

```
ecommerce-analytics/
│
├── data/
│   ├── README.md
│   
│
├── notebooks/
│   ├── 01_data_validation.ipynb
│   ├── 02_commercial_analysis.ipynb
│   ├── 03_customer_behavior.ipynb
│
├── src/
│   ├── ingest.py
│
├── sql/
│   ├── schema.sql
│
├── requirements.txt
├── final_report.pdf
├── .gitignore
└── README.md
```

---

## Dataset

This project uses the **Brazilian E-Commerce Public Dataset by Olist**, available on Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce?resource=download&select=product_category_name_translation.csv

Due to file size constraints, datasets are not included in this repository.

---

## Data Modeling

A relational database was built using **PostgreSQL**, structured around the following core entities:

* `customers`
* `orders`
* `order_items`
* `products`
* `payments`
* `sellers`
* `order_reviews`

### Relationships

* customers → orders
* orders → order_items
* orders → payments
* order_items → products
* order_items → sellers

The database schema is available in:

```
sql/schema.sql
```

---

## Data Ingestion

Data ingestion was implemented in:

```
src/ingest.py
```

Although a standalone SQL schema is provided, **the full database creation and loading process is executed via Python**.

### Ingestion process includes:

* Database connection using SQLAlchemy
* Table creation (DROP + CREATE statements)
* Reading CSV files using pandas
* Data cleaning:

  * Removal of duplicate records based on primary keys
  * Removal of null values in primary key columns
* Data insertion into PostgreSQL using `to_sql`

This approach ensures a fully reproducible pipeline directly from Python.

---

## Analytical Structure

The project is divided into three main notebooks:

---

### 01_data_validation.ipynb

Initial data validation and exploration:

* Table volumes
* Data completeness
* Uniqueness checks
* Temporal coverage
* Order status distribution

Defines business rules for subsequent analyses.

---

### 02_commercial_analysis.ipynb

Focus on commercial performance:

* Total revenue
* Number of orders
* Unique customers
* Average order value (AOV)
* Monthly revenue trends
* Growth analysis (MoM)
* Rolling averages
* Revenue by category
* Revenue by state
* Top products and customers

---

### 03_customer_behavior.ipynb

Focus on customer behavior:

* Average number of orders per customer
* Purchase frequency distribution
* Time between purchases
* Customer retention (cohort analysis)

---

## Business Rules

* Revenue analysis considers only orders with `order_status = 'delivered'`

* Revenue is defined as:

  ```
  price + freight_value
  ```

* Behavioral analysis includes valid orders (excluding canceled and unavailable)

---

## Key Insights

### Commercial

* Revenue is concentrated in a small number of product categories
* Sales distribution varies significantly by region
* A small number of products and customers contribute disproportionately

---

### Customer Behavior

* Low purchase frequency across the customer base
* Majority of customers make only one purchase
* Long intervals between purchases
* Retention drops significantly after the first purchase
* Limited recurring behavior over time

---

## Technologies Used

* Python (pandas, matplotlib)
* SQL (PostgreSQL)
* SQLAlchemy
* Jupyter Notebook

---

## Outputs

Final results and summarized insights are available in:

```
final_report.pdf
```

---

## Future Improvements

* Customer segmentation (RFM)
* Predictive modeling (churn / LTV)
* Dashboard development (Power BI / Tableau)
* Data pipeline automation

---

## Notes

* Data files are not included due to size limitations
* All transformations are reproducible via the ingestion script
* SQL queries are embedded within notebooks for analytical clarity

---

## 🇧🇷 Versão em Português

Este projeto analisa dados transacionais do marketplace brasileiro Olist, com foco em desempenho comercial e comportamento dos clientes.

Foram utilizadas técnicas de SQL, Python e modelagem relacional para explorar métricas de receita, frequência de compra e retenção ao longo do tempo.

O projeto está estruturado em três etapas principais:

- Validação dos dados  
- Análise de desempenho comercial  
- Análise de comportamento dos clientes  

Os notebooks estão documentados em português, enquanto este README foi escrito em inglês para ampliar o alcance do projeto.

---

## Author

Lucas Manhães
Oceanographer transitioning into Data Analytics and Data Science
