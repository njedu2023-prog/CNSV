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
- snapshot_id: cnsvdata-2026-10-15-f461297b8d39
- latest_trade_date: 2026-10-15
- generated_at: 2026-10-15 22:51:03
- file_count: 14

## Loaded Data
- daily_rows: 3917
- one_min_rows: 20726
- moneyflow_rows: 3917
- latest_trade_date: 2026-10-15

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-15', 'latest_open': 37.2, 'latest_high': 37.73, 'latest_low': 34.41, 'latest_close': 35.45, 'latest_pre_close': 38.11, 'latest_pct_chg': -6.9798, 'latest_volume': 1944758.91, 'latest_amount': 6954077.083, 'ma5': 37.85, 'ma10': 38.328, 'ma20': 38.847, 'ma60': 35.88816666666666, 'ret_1d': -0.06979795329309879, 'ret_3d': -0.06710526315789467, 'ret_5d': -0.10952022104998738, 'ret_10d': -0.0813682301114278, 'ret_20d': -0.10321274981027062, 'ret_60d': 0.033226464587583715, 'volume_ma5': 1142318.412, 'volume_ma20': 1150660.7219999998, 'volume_ratio_5d': 1.9429144003282197, 'volume_ratio_20d': 1.74715578547109, 'amount_ma5': 4292469.9754, 'amount_ma20': 4477054.0200499995, 'amount_ratio_5d': 1.7830918809158882, 'amount_ratio_20d': 1.5935922553147515, 'price_position_20d': 0.14814814814814897, 'price_position_60d': 0.35905680600214385, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-15', 'latest_intraday_open': 37.2, 'latest_intraday_high': 37.73, 'latest_intraday_low': 34.41, 'latest_intraday_close': 35.45, 'intraday_range_pct': 0.09365303244005642, 'close_position_in_day_range': 0.3132530120481946, 'morning_return': -0.0317204301075269, 'afternoon_return': -0.0158245419211549, 'last_30min_return': 0.016050444253367768, 'last_60min_return': 0.02634626519976857, 'morning_volume_ratio': 0.4439103662468887, 'afternoon_volume_ratio': 0.5560896337531114, 'last_30min_volume_ratio': 0.10670271720210296, 'last_60min_volume_ratio': 0.203769443071995, 'intraday_volume_sum': 194475891.0, 'intraday_amount_sum': 6954077100.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -76592.89, 'net_mf_ratio': -0.011014098504493095, 'small_order_net': 49965.140000000014, 'medium_order_net': 52103.370000000024, 'large_order_net': -12335.329999999987, 'extra_large_order_net': -89733.20000000001, 'main_force_net': -102068.53, 'main_force_ratio': -0.014677509147765656, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-15', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -25.69160765225875, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
