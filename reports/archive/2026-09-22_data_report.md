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
- snapshot_id: cnsvdata-2026-09-22-211484174936
- latest_trade_date: 2026-09-22
- generated_at: 2026-09-22 22:39:45
- file_count: 14

## Loaded Data
- daily_rows: 3906
- one_min_rows: 18075
- moneyflow_rows: 3906
- latest_trade_date: 2026-09-22

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-22', 'latest_open': 40.86, 'latest_high': 41.1, 'latest_low': 39.78, 'latest_close': 40.12, 'latest_pre_close': 41.02, 'latest_pct_chg': -2.1941, 'latest_volume': 986462.83, 'latest_amount': 3968264.199, 'ma5': 39.472, 'ma10': 39.459999999999994, 'ma20': 37.485, 'ma60': 35.407666666666664, 'ret_1d': -0.021940516821063016, 'ret_3d': 0.02977412731006157, 'ret_5d': 0.05136268343815509, 'ret_10d': 0.026612077789150534, 'ret_20d': 0.18557919621749397, 'ret_60d': 0.18733353063036406, 'volume_ma5': 1106440.702, 'volume_ma20': 1275471.0055, 'volume_ratio_5d': 0.8557302632135843, 'volume_ratio_20d': 0.7908125821319923, 'amount_ma5': 4346395.5, 'amount_ma20': 4832072.2195999995, 'amount_ratio_5d': 0.8840265724826488, 'amount_ratio_20d': 0.8433325586561901, 'price_position_20d': 0.8597883597883595, 'price_position_60d': 0.8832599118942729, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-22', 'latest_intraday_open': 40.86, 'latest_intraday_high': 41.1, 'latest_intraday_low': 39.78, 'latest_intraday_close': 40.12, 'intraday_range_pct': 0.032901296111665014, 'close_position_in_day_range': 0.25757575757575474, 'morning_return': -0.021542227662178726, 'afternoon_return': 0.0037528146109582217, 'last_30min_return': -0.0012447099825741992, 'last_60min_return': -0.004713470602828229, 'morning_volume_ratio': 0.683020474273724, 'afternoon_volume_ratio': 0.31697952572627597, 'last_30min_volume_ratio': 0.09719277511956533, 'last_60min_volume_ratio': 0.1515730602844914, 'intraday_volume_sum': 98646283.0, 'intraday_amount_sum': 3968264194.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -43547.16, 'net_mf_ratio': -0.010973856027775031, 'small_order_net': 7818.889999999999, 'medium_order_net': 11747.820000000007, 'large_order_net': -4089.720000000001, 'extra_large_order_net': -15476.990000000005, 'main_force_net': -19566.710000000006, 'main_force_ratio': -0.004930798207672464, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-22', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -15.904654235447495, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 5, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
