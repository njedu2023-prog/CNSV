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
- snapshot_id: cnsvdata-2026-09-15-539278e48c30
- latest_trade_date: 2026-09-15
- generated_at: 2026-09-15 22:50:50
- file_count: 14

## Loaded Data
- daily_rows: 3901
- one_min_rows: 16870
- moneyflow_rows: 3901
- latest_trade_date: 2026-09-15

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-15', 'latest_open': 38.5, 'latest_high': 38.96, 'latest_low': 38.06, 'latest_close': 38.16, 'latest_pre_close': 38.98, 'latest_pct_chg': -2.1036, 'latest_volume': 1218124.83, 'latest_amount': 4680545.291, 'ma5': 39.44799999999999, 'ma10': 38.041999999999994, 'ma20': 35.98950000000001, 'ma60': 34.976, 'ret_1d': -0.021036428937916907, 'ret_3d': -0.0651641352278296, 'ret_5d': -0.023541453428863934, 'ret_10d': 0.10833575370316573, 'ret_20d': 0.13944461033144195, 'ret_60d': 0.06562412733873213, 'volume_ma5': 1493140.03, 'volume_ma20': 1150164.3314999999, 'volume_ratio_5d': 0.7864796436526077, 'volume_ratio_20d': 1.0933015275386246, 'amount_ma5': 5913140.5762, 'amount_ma20': 4252078.12025, 'amount_ratio_5d': 0.7614835755266075, 'amount_ratio_20d': 1.141217153899448, 'price_position_20d': 0.6484284051222347, 'price_position_60d': 0.6674008810572684, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-15', 'latest_intraday_open': 38.5, 'latest_intraday_high': 38.96, 'latest_intraday_low': 38.06, 'latest_intraday_close': 38.16, 'intraday_range_pct': 0.023584905660377322, 'close_position_in_day_range': 0.11111111111110497, 'morning_return': 0.0036363636363636598, 'afternoon_return': -0.01242236024844734, 'last_30min_return': 0.0002621231979029748, 'last_60min_return': -0.00261369576581294, 'morning_volume_ratio': 0.6227031017830906, 'afternoon_volume_ratio': 0.37729689821690937, 'last_30min_volume_ratio': 0.1361236598387047, 'last_60min_volume_ratio': 0.24108691717580374, 'intraday_volume_sum': 121812483.0, 'intraday_amount_sum': 4680545309.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -15148.9, 'net_mf_ratio': -0.0032365673352481184, 'small_order_net': 60872.17000000001, 'medium_order_net': 4266.979999999996, 'large_order_net': -7597.439999999988, 'extra_large_order_net': -57541.69999999998, 'main_force_net': -65139.13999999997, 'main_force_ratio': -0.013916998116705109, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-15', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -17.153565451953227, 'flow_continuity_3d': -3, 'flow_continuity_5d': -1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 5, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
