import polars as pl

CSV_FILE = "data/202306-divvy-tripdate.csv"


def convert_types(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.with_columns(
        [
            pl.col("ride_id").cast(pl.Utf8),
            pl.col("rideable_type").cast(pl.Utf8),
            pl.col("started_at").str.strptime(pl.Datetime, fmt="%Y-%m-%d %H:%M:%S"),
            pl.col("ended_at").str.strptime(pl.Datetime, fmt="%Y-%m-%d %H:%M:%S"),
            pl.col("start_station_name").cast(pl.Utf8),
            pl.col("start_station_id").cast(pl.Utf8),
            pl.col("end_station_name").cast(pl.Utf8),
            pl.col("end_station_id").cast(pl.Utf8),
            pl.col("start_lat").cast(pl.Float64),
            pl.col("start_lng").cast(pl.Float64),
            pl.col("end_lat").cast(pl.Float64),
            pl.col("end_lng").cast(pl.Float64),
            pl.col("member_casual").cast(pl.Utf8),
        ]
    )


def count_rides_per_day(lf: pl.LazyFrame) -> pl.LazyFrame:
    return (
        lf.with_columns(pl.col("started_at").dt.date().alias("ride_date"))
        .groupby("ride_date")
        .agg(pl.count().alias("ride_count"))
        .sort("ride_date")
    )


def compute_weekly_stats(daily_counts: pl.LazyFrame) -> pl.LazyFrame:
    return (
        daily_counts.with_columns(
            pl.col("ride_date").dt.strftime("%Y-%U").alias("week")  # Year-week format
        )
        .groupby("week")
        .agg(
            [
                pl.mean("ride_count").alias("avg_rides"),
                pl.min("ride_count").alias("min_rides"),
                pl.max("ride_count").alias("max_rides"),
            ]
        )
        .sort("week")
    )


def compute_week_over_week_diff(daily_counts: pl.LazyFrame) -> pl.LazyFrame:
    # Add lag (7-day shift)
    return daily_counts.with_columns(
        [
            pl.col("ride_count").shift(7).alias("ride_count_last_week"),
            (pl.col("ride_count") - pl.col("ride_count").shift(7)).alias(
                "diff_vs_last_week"
            ),
        ]
    ).sort("ride_date")


def main():
    # Read CSV as LazyFrame
    lf = pl.read_csv(CSV_FILE, infer_schema_length=1000).lazy()

    # Convert columns to appropriate types
    lf = convert_types(lf)

    # Daily ride count
    daily_counts = count_rides_per_day(lf)

    # Weekly average, min, max
    weekly_stats = compute_weekly_stats(daily_counts)

    # Compare each day's count with same day last week
    week_over_week = compute_week_over_week_diff(daily_counts)

    # Execute and print results
    print("\n=== Daily Ride Counts ===")
    print(daily_counts.collect().head(10))

    print("\n=== Weekly Stats ===")
    print(weekly_stats.collect().head(10))

    print("\n=== Week-over-Week Ride Deltas ===")
    print(week_over_week.collect().head(14))


if __name__ == "__main__":
    main()
