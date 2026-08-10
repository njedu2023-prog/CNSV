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
- snapshot_id: cnsvdata-2026-08-10-24f43be9527f
- latest_trade_date: 2026-08-10
- generated_at: 2026-08-10 20:05:56
- file_count: 14

## Loaded Data
- daily_rows: 3875
- one_min_rows: 10604
- moneyflow_rows: 3875
- latest_trade_date: 2026-08-10

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-10', 'latest_open': 34.77, 'latest_high': 35.28, 'latest_low': 34.63, 'latest_close': 34.83, 'latest_pre_close': 34.85, 'latest_pct_chg': -0.0574, 'latest_volume': 818317.06, 'latest_amount': 2855422.063, 'ma5': 34.852, 'ma10': 34.739000000000004, 'ma20': 34.00750000000001, 'ma60': 35.54116666666666, 'ret_1d': -0.0005738880918222389, 'ret_3d': -0.010511363636363735, 'ret_5d': -0.007692307692307776, 'ret_10d': 0.03877124962719947, 'ret_20d': 0.01812335574393442, 'ret_60d': -0.1410604192355117, 'volume_ma5': 839878.6940000001, 'volume_ma20': 949594.9014999999, 'volume_ratio_5d': 1.0155929725042678, 'volume_ratio_20d': 0.8046544237742891, 'amount_ma5': 2926376.9242, 'amount_ma20': 3219644.8352499995, 'amount_ratio_5d': 1.017207394407399, 'amount_ratio_20d': 0.8274653025677798, 'price_position_20d': 0.8374233128834352, 'price_position_60d': 0.3230769230769229, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-10', 'latest_intraday_open': 34.77, 'latest_intraday_high': 35.28, 'latest_intraday_low': 34.63, 'latest_intraday_close': 34.83, 'intraday_range_pct': 0.018662072925638776, 'close_position_in_day_range': 0.3076923076923018, 'morning_return': -0.0005752085130861229, 'afternoon_return': 0.002302158273381316, 'last_30min_return': -0.000860585197934638, 'last_60min_return': 0.002590673575129321, 'morning_volume_ratio': 0.5966642196118946, 'afternoon_volume_ratio': 0.4033357803881053, 'last_30min_volume_ratio': 0.1541036429082879, 'last_60min_volume_ratio': 0.265753203287733, 'intraday_volume_sum': 81831706.0, 'intraday_amount_sum': 2855422066.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -35002.42, 'net_mf_ratio': -0.012258229861551643, 'small_order_net': 23254.9, 'medium_order_net': 8598.5, 'large_order_net': -7348.830000000002, 'extra_large_order_net': -24504.559999999998, 'main_force_net': -31853.39, 'main_force_ratio': -0.0111554051545479, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-10', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -23.41363501609954, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
