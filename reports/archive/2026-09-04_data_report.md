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
- snapshot_id: cnsvdata-2026-09-04-ef09247b6aa5
- latest_trade_date: 2026-09-04
- generated_at: 2026-09-04 22:11:36
- file_count: 14

## Loaded Data
- daily_rows: 3894
- one_min_rows: 15183
- moneyflow_rows: 3894
- latest_trade_date: 2026-09-04

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-04', 'latest_open': 34.5, 'latest_high': 37.75, 'latest_low': 34.5, 'latest_close': 37.47, 'latest_pre_close': 34.32, 'latest_pct_chg': 9.1783, 'latest_volume': 3377446.91, 'latest_amount': 12392923.871, 'ma5': 34.846, 'ma10': 34.528, 'ma20': 34.106, 'ma60': 34.618, 'ret_1d': 0.09178321678321666, 'ret_3d': 0.0882950914899796, 'ret_5d': 0.07734330074755591, 'ret_10d': 0.11252969121140133, 'ret_20d': 0.07517934002869442, 'ret_60d': 0.08766328011611013, 'volume_ma5': 1360042.564, 'volume_ma20': 830183.3255, 'volume_ratio_5d': 4.130493070095279, 'volume_ratio_20d': 4.7631150671293705, 'amount_ma5': 4825379.9372, 'amount_ma20': 2869777.0322000002, 'amount_ratio_5d': 4.410764783021088, 'amount_ratio_20d': 5.127085341657201, 'price_position_20d': 0.9457364341085269, 'price_position_60d': 0.8717532467532468, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-04', 'latest_intraday_open': 34.5, 'latest_intraday_high': 37.75, 'latest_intraday_low': 34.5, 'latest_intraday_close': 37.47, 'intraday_range_pct': 0.08673605551107554, 'close_position_in_day_range': 0.9138461538461535, 'morning_return': 0.05154937735302645, 'afternoon_return': 0.031947122004957196, 'last_30min_return': -0.007417218543046333, 'last_60min_return': -0.007154213036566048, 'morning_volume_ratio': 0.4882354583036214, 'afternoon_volume_ratio': 0.5117645416963785, 'last_30min_volume_ratio': 0.11197433448332131, 'last_60min_volume_ratio': 0.22709818701487747, 'intraday_volume_sum': 337744691.0, 'intraday_amount_sum': 12392923819.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 248627.05, 'net_mf_ratio': 0.020062017050052127, 'small_order_net': -114483.09, 'medium_order_net': -92048.94999999998, 'large_order_net': 23503.940000000002, 'extra_large_order_net': 183028.09999999998, 'main_force_net': 206532.03999999998, 'main_force_ratio': 0.01666531983491759, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-04', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 36.727336884969716, 'flow_continuity_3d': 1, 'flow_continuity_5d': 1, 'flow_continuity_10d': 0, 'positive_flow_days_5d': 3, 'positive_flow_days_10d': 5, 'flow_reversal_1d': False, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'inflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
