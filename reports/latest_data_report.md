# CNSV Data Status Report

## CNSVdata Gate
- ready: True
- status: PASS
- can_continue: True
- can_run_backtest: True
- can_use_moneyflow_as_strong_factor: True
- can_generate_formal_signal: False
- blocking_reason: None

## Data Manifest
- snapshot_id: cnsvdata-2026-06-18-0888ae563737
- latest_trade_date: 2026-06-18
- generated_at: 2026-06-19 17:32:24
- file_count: 14

## Loaded Data
- daily_rows: 3839
- one_min_rows: 1928
- moneyflow_rows: 3839
- latest_trade_date: 2026-06-18

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_close': 36.14, 'latest_pct_chg': -2.7187, 'latest_volume': 1182191.19, 'latest_amount': 4313475.328, 'ma5': 36.016, 'ma10': 35.501999999999995, 'ma20': 36.49999999999999, 'ret_1d': -0.02718707940780618, 'ret_5d': 0.049056603773584895, 'ret_20d': -0.05885416666666665, 'volume_ratio_5d': 1.2478544833680014, 'amount_ratio_5d': 1.2744407792473547}
- minute_structure: {'latest_intraday_high': 37.43, 'latest_intraday_low': 35.72, 'latest_intraday_close': 36.14, 'intraday_range_pct': 0.04731599335915885, 'close_position_in_day_range': 0.24561403508772017, 'last_30min_return': -0.0024841291747169647, 'last_60min_return': -0.0024841291747169647, 'intraday_volume_sum': 118219119.0, 'intraday_amount_sum': 4313475325.0}
- moneyflow: {'net_mf_amount': -57131.22, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-18', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
