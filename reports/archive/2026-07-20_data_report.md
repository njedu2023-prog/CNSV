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
- snapshot_id: cnsvdata-2026-07-20-151a7e16dce5
- latest_trade_date: 2026-07-20
- generated_at: 2026-07-20 20:23:17
- file_count: 14

## Loaded Data
- daily_rows: 3860
- one_min_rows: 6989
- moneyflow_rows: 3860
- latest_trade_date: 2026-07-20

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-20', 'latest_open': 32.28, 'latest_high': 33.16, 'latest_low': 32.1, 'latest_close': 33.01, 'latest_pre_close': 31.98, 'latest_pct_chg': 3.2208, 'latest_volume': 998987.69, 'latest_amount': 3273581.711, 'ma5': 33.286, 'ma10': 34.705000000000005, 'ma20': 34.933, 'ma60': 37.04066666666667, 'ret_1d': 0.020717377860234754, 'ret_3d': -0.03788982803847285, 'ret_5d': -0.03507746273019596, 'ret_10d': -0.12300743889479282, 'ret_20d': -0.11572461826948832, 'ret_60d': -0.09113436123348029, 'volume_ma5': 1132729.204, 'volume_ma20': 1260585.6435, 'volume_ratio_5d': 0.7312518777081394, 'volume_ratio_20d': 0.7836075743807689, 'amount_ma5': 3776401.9414, 'amount_ma20': 4432338.4753, 'amount_ratio_5d': 0.7089643273967154, 'amount_ratio_20d': 0.7268184783522246, 'price_position_20d': 0.14772727272727226, 'price_position_60d': 0.080388692579505, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': True}
- minute_structure: {'latest_intraday_date': '2026-07-20', 'latest_intraday_open': 32.28, 'latest_intraday_high': 33.16, 'latest_intraday_low': 32.1, 'latest_intraday_close': 33.01, 'intraday_range_pct': 0.032111481369281894, 'close_position_in_day_range': 0.8584905660377365, 'morning_return': 0.015179677819083137, 'afternoon_return': 0.007323771742447249, 'last_30min_return': 0.006402439024390194, 'last_60min_return': 0.008246792913866763, 'morning_volume_ratio': 0.5535314654377773, 'afternoon_volume_ratio': 0.4464685345622227, 'last_30min_volume_ratio': 0.12589905887629105, 'last_60min_volume_ratio': 0.20670083532260541, 'intraday_volume_sum': 99898769.0, 'intraday_amount_sum': 3273581700.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 37498.44, 'net_mf_ratio': 0.011454866049011844, 'small_order_net': 3813.1800000000076, 'medium_order_net': 4049.8600000000006, 'large_order_net': -1493.75, 'extra_large_order_net': -6369.290000000001, 'main_force_net': -7863.040000000001, 'main_force_ratio': -0.0024019684535682576, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-20', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': 9.052897595443588, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
