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
- snapshot_id: cnsvdata-2026-10-09-40921c8e48c9
- latest_trade_date: 2026-10-09
- generated_at: 2026-10-10 23:50:11
- file_count: 14

## Loaded Data
- daily_rows: 3913
- one_min_rows: 19762
- moneyflow_rows: 3913
- latest_trade_date: 2026-10-09

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-09', 'latest_open': 39.99, 'latest_high': 40.47, 'latest_low': 38.18, 'latest_close': 38.54, 'latest_pre_close': 39.81, 'latest_pct_chg': -3.1902, 'latest_volume': 1056024.09, 'latest_amount': 4087925.871, 'ma5': 38.896, 'ma10': 39.17700000000001, 'ma20': 39.0345, 'ma60': 35.698499999999996, 'ret_1d': -0.03190153227832215, 'ret_3d': -0.010526315789473828, 'ret_5d': 0.011814124442110607, 'ret_10d': -0.010780287474332684, 'ret_20d': 0.12296037296037299, 'ret_60d': 0.06877426511369933, 'volume_ma5': 1013756.186, 'volume_ma20': 1337238.289, 'volume_ratio_5d': 1.1341959581825563, 'volume_ratio_20d': 0.7911287989757292, 'amount_ma5': 3962154.0741999997, 'amount_ma20': 5197154.25085, 'amount_ratio_5d': 1.1238463936927816, 'amount_ratio_20d': 0.7911668202452629, 'price_position_20d': 0.5829725829725829, 'price_position_60d': 0.690246516613076, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-09', 'latest_intraday_open': 39.99, 'latest_intraday_high': 40.47, 'latest_intraday_low': 38.18, 'latest_intraday_close': 38.54, 'intraday_range_pct': 0.05941878567721846, 'close_position_in_day_range': 0.1572052401746723, 'morning_return': -0.04026006501625401, 'afternoon_return': 0.004168837936425085, 'last_30min_return': -0.00025940337224383825, 'last_60min_return': 0.004168837936425085, 'morning_volume_ratio': 0.6366625689381764, 'afternoon_volume_ratio': 0.3633374310618236, 'last_30min_volume_ratio': 0.09733497651554521, 'last_60min_volume_ratio': 0.180823119290773, 'intraday_volume_sum': 105602409.0, 'intraday_amount_sum': 4087925869.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -32222.16, 'net_mf_ratio': -0.007882276004216713, 'small_order_net': 2674.2199999999866, 'medium_order_net': 3559.5399999999936, 'large_order_net': 18151.92, 'extra_large_order_net': -24385.67, 'main_force_net': -6233.75, 'main_force_ratio': -0.001524917573535912, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-09', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -9.407193577752624, 'flow_continuity_3d': -1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 5, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
