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
- snapshot_id: cnsvdata-2026-09-30-3e8a073970a3
- latest_trade_date: 2026-09-30
- generated_at: 2026-10-03 22:40:06
- file_count: 14

## Loaded Data
- daily_rows: 3911
- one_min_rows: 19280
- moneyflow_rows: 3911
- latest_trade_date: 2026-09-30

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-30', 'latest_open': 39.13, 'latest_high': 39.93, 'latest_low': 39.01, 'latest_close': 39.1, 'latest_pre_close': 38.95, 'latest_pct_chg': 0.3851, 'latest_volume': 833419.09, 'latest_amount': 3281209.191, 'ma5': 38.562, 'ma10': 39.017, 'ma20': 38.529500000000006, 'ma60': 35.593333333333334, 'ret_1d': 0.0038510911424902705, 'ret_3d': 0.026516145970070903, 'ret_5d': -0.025423728813559254, 'ret_10d': 0.0246331236897277, 'ret_20d': 0.1356375254138833, 'ret_60d': 0.04741494776319333, 'volume_ma5': 851869.4700000001, 'volume_ma20': 1308444.217, 'volume_ratio_5d': 0.9444075479719092, 'volume_ratio_20d': 0.6373693174375067, 'amount_ma5': 3295550.9978, 'amount_ma20': 5038232.1234, 'amount_ratio_5d': 0.9557953719189077, 'amount_ratio_20d': 0.6543353863661258, 'price_position_20d': 0.7208053691275171, 'price_position_60d': 0.7709251101321587, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-30', 'latest_intraday_open': 39.13, 'latest_intraday_high': 39.93, 'latest_intraday_low': 39.01, 'latest_intraday_close': 39.1, 'intraday_range_pct': 0.023529411764705924, 'close_position_in_day_range': 0.09782608695652527, 'morning_return': 0.004344492716585657, 'afternoon_return': -0.0050890585241729624, 'last_30min_return': -0.005595116988809767, 'last_60min_return': -0.004075394803871535, 'morning_volume_ratio': 0.6317667981423367, 'afternoon_volume_ratio': 0.36823320185766323, 'last_30min_volume_ratio': 0.16205145960839462, 'last_60min_volume_ratio': 0.23026055234707907, 'intraday_volume_sum': 83341909.0, 'intraday_amount_sum': 3281209181.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -4115.53, 'net_mf_ratio': -0.001254272361325956, 'small_order_net': -19808.819999999992, 'medium_order_net': 12010.899999999994, 'large_order_net': 4851.309999999998, 'extra_large_order_net': 2946.6100000000006, 'main_force_net': 7797.919999999998, 'main_force_ratio': 0.002376538509458295, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-30', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': 1.1222661481323386, 'flow_continuity_3d': 1, 'flow_continuity_5d': -1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 5, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
