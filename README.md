# Lazy Bike Trip Analysis with Polars

This project demonstrates how to use **Polars' LazyFrame API** to process and analyze bike trip data efficiently, especially for datasets larger than memory. It explores techniques like daily/weekly aggregations and time-based comparisons.

## 🚴 Project Summary

- 🐍 Built with Python + [Polars](https://www.pola.rs/)
- 🐢 Uses **lazy evaluation** for efficient processing
- 📆 Performs time-based aggregations (daily, weekly)
- 📈 Computes trends such as week-over-week change

## 🛠️ Tech Stack

- Python 3
- Polars
- Docker & Docker Compose

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/polars-lazy-bike-analysis.git
cd polars-lazy-bike-analysis
docker build --tag=exercise-9 .
docker-compose up
