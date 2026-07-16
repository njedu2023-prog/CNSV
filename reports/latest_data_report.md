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
- snapshot_id: cnsvdata-2026-07-16-58bda63e40be
- latest_trade_date: 2026-07-16
- generated_at: 2026-07-17 01:14:46
- file_count: 14

## Loaded Data
- daily_rows: 3858
- one_min_rows: 6507
- moneyflow_rows: 3858
- latest_trade_date: 2026-07-16

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-16', 'latest_open': 34.01, 'latest_high': 34.05, 'latest_low': 32.95, 'latest_close': 33.0, 'latest_pre_close': 34.31, 'latest_pct_chg': -3.8181, 'latest_volume': 1221496.3, 'latest_amount': 4070749.544, 'ma5': 34.466, 'ma10': 35.648999999999994, 'ma20': 35.339, 'ma60': 37.14483333333333, 'ret_1d': -0.038181288254153345, 'ret_3d': -0.03536977491961413, 'ret_5d': -0.08485856905158073, 'ret_10d': -0.03958090803259606, 'ret_20d': -0.11170928667563929, 'ret_60d': -0.0009082652134423386, 'volume_ma5': 1567556.4319999998, 'volume_ma20': 1286988.7570000002, 'volume_ratio_5d': 0.7867343336415559, 'volume_ratio_20d': 0.9524184618498481, 'amount_ma5': 5456988.0564, 'amount_ma20': 4567168.840600001, 'amount_ratio_5d': 0.7456824355211239, 'amount_ratio_20d': 0.8905006950382164, 'price_position_20d': 0.02592592592592604, 'price_position_60d': 0.013257575757575808, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-16', 'latest_intraday_open': 34.01, 'latest_intraday_high': 34.05, 'latest_intraday_low': 32.95, 'latest_intraday_close': 33.0, 'intraday_range_pct': 0.03333333333333316, 'close_position_in_day_range': 0.045454545454543104, 'morning_return': -0.01852396354013508, 'afternoon_return': -0.011384062312762233, 'last_30min_return': -0.0006056935190794643, 'last_60min_return': -0.0066225165562913135, 'morning_volume_ratio': 0.532226769741341, 'afternoon_volume_ratio': 0.46777323025865897, 'last_30min_volume_ratio': 0.12731484327869025, 'last_60min_volume_ratio': 0.24246556457027335, 'intraday_volume_sum': 122149630.0, 'intraday_amount_sum': 4070749551.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -104896.45, 'net_mf_ratio': -0.025768337959924364, 'small_order_net': -7496.540000000008, 'medium_order_net': -2419.6300000000047, 'large_order_net': -3733.6399999999994, 'extra_large_order_net': 13649.819999999996, 'main_force_net': 9916.179999999997, 'main_force_ratio': 0.002435959248491657, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-16', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -23.332378711432707, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
