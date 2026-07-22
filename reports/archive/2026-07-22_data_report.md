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
- snapshot_id: cnsvdata-2026-07-22-cd0574e42525
- latest_trade_date: 2026-07-22
- generated_at: 2026-07-22 20:04:45
- file_count: 14

## Loaded Data
- daily_rows: 3862
- one_min_rows: 7471
- moneyflow_rows: 3862
- latest_trade_date: 2026-07-22

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-22', 'latest_open': 32.88, 'latest_high': 33.8, 'latest_low': 32.67, 'latest_close': 33.02, 'latest_pre_close': 32.96, 'latest_pct_chg': 0.182, 'latest_volume': 1083698.09, 'latest_amount': 3604353.059, 'ma5': 32.866, 'ma10': 33.971999999999994, 'ma20': 34.674, 'ma60': 36.889, 'ret_1d': 0.001820388349514701, 'ret_3d': 0.021026592455163806, 'ret_5d': -0.037598367822792134, 'ret_10d': -0.0822679266259031, 'ret_20d': -0.06591230551626581, 'ret_60d': -0.14455958549222792, 'volume_ma5': 1035308.216, 'volume_ma20': 1256320.399, 'volume_ratio_5d': 1.0649431776195117, 'volume_ratio_20d': 0.8705981800702232, 'amount_ma5': 3414152.5716, 'amount_ma20': 4385302.42315, 'amount_ratio_5d': 1.0692597176164196, 'amount_ratio_20d': 0.8271866655656167, 'price_position_20d': 0.1493506493506497, 'price_position_60d': 0.08127208480565386, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-22', 'latest_intraday_open': 32.88, 'latest_intraday_high': 33.8, 'latest_intraday_low': 32.67, 'latest_intraday_close': 33.02, 'intraday_range_pct': 0.0342216838279829, 'close_position_in_day_range': 0.30973451327433876, 'morning_return': 0.014607425441266031, 'afternoon_return': -0.00959808038392318, 'last_30min_return': 0.0027330701488006426, 'last_60min_return': 0.0, 'morning_volume_ratio': 0.6854670473766361, 'afternoon_volume_ratio': 0.31453295262336395, 'last_30min_volume_ratio': 0.09958859482718106, 'last_60min_volume_ratio': 0.17235714607561964, 'intraday_volume_sum': 108369809.0, 'intraday_amount_sum': 3604353046.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -3732.16, 'net_mf_ratio': -0.0010354590515712296, 'small_order_net': -404.75, 'medium_order_net': -563.1999999999971, 'large_order_net': -2345.350000000006, 'extra_large_order_net': 3313.300000000003, 'main_force_net': 967.9499999999971, 'main_force_ratio': 0.00026855027355964607, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-22', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -0.7669087780115833, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
