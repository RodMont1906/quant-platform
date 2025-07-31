-- Drop and re-create the daily aggregate
DROP MATERIALIZED VIEW IF EXISTS daily_ohlcv CASCADE;

CREATE MATERIALIZED VIEW daily_ohlcv WITH (timescaledb.continuous) AS
SELECT
  symbol,
  time_bucket('1 day', timestamp) AS day,
  first(open, timestamp) AS open,
  max(high) AS high,
  min(low) AS low,
  last(close, timestamp) AS close,
  sum(volume) AS volume
FROM market_data
GROUP BY symbol, day
WITH NO DATA;

-- Valid refresh policy (covers 3 buckets)
SELECT add_continuous_aggregate_policy('daily_ohlcv',
  start_offset => INTERVAL '3 days',
  end_offset => INTERVAL '0 hours',
  schedule_interval => INTERVAL '1 hour');