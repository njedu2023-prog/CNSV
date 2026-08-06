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
- snapshot_id: cnsvdata-2026-08-06-b35a41d86792
- latest_trade_date: 2026-08-06
- generated_at: 2026-08-06 20:08:44
- file_count: 14

## Loaded Data
- daily_rows: 3873
- one_min_rows: 10122
- moneyflow_rows: 3873
- latest_trade_date: 2026-08-06

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-06', 'latest_open': 34.9, 'latest_high': 35.12, 'latest_low': 34.54, 'latest_close': 34.9, 'latest_pre_close': 35.2, 'latest_pct_chg': -0.8523, 'latest_volume': 678005.44, 'latest_amount': 2359365.26, 'ma5': 34.971999999999994, 'ma10': 34.42999999999999, 'ma20': 34.086000000000006, 'ma60': 35.72599999999999, 'ret_1d': -0.008522727272727404, 'ret_3d': -0.005698005698005826, 'ret_5d': 0.007796708056598156, 'ret_10d': 0.03376777251184837, 'ret_20d': -0.0321686078757627, 'ret_60d': -0.16447210916926036, 'volume_ma5': 811344.534, 'volume_ma20': 1066540.508, 'volume_ratio_5d': 0.8151469300651528, 'volume_ratio_20d': 0.6220347880283488, 'amount_ma5': 2825922.0554, 'amount_ma20': 3646175.1602000007, 'amount_ratio_5d': 0.8157242640954854, 'amount_ratio_20d': 0.6321527973105955, 'price_position_20d': 0.4545454545454543, 'price_position_60d': 0.2886597938144328, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-06', 'latest_intraday_open': 34.9, 'latest_intraday_high': 35.12, 'latest_intraday_low': 34.54, 'latest_intraday_close': 34.9, 'intraday_range_pct': 0.01661891117478505, 'close_position_in_day_range': 0.6206896551724146, 'morning_return': -0.00859598853868182, 'afternoon_return': 0.00867052023121384, 'last_30min_return': 0.0014347202295552641, 'last_60min_return': 0.0057636887608067955, 'morning_volume_ratio': 0.6812540471651672, 'afternoon_volume_ratio': 0.3187459528348327, 'last_30min_volume_ratio': 0.09340897028790801, 'last_60min_volume_ratio': 0.19224704155766065, 'intraday_volume_sum': 67800544.0, 'intraday_amount_sum': 2359365259.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -31521.39, 'net_mf_ratio': -0.013360114491132247, 'small_order_net': 19805.25, 'medium_order_net': 9521.300000000003, 'large_order_net': -5287.240000000005, 'extra_large_order_net': -24039.32, 'main_force_net': -29326.560000000005, 'main_force_ratio': -0.01242985157796212, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-06', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -25.789966069094366, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
