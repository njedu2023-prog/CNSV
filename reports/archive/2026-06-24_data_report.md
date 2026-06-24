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
- snapshot_id: cnsvdata-2026-06-24-9039ab677ed3
- latest_trade_date: 2026-06-24
- generated_at: 2026-06-24 23:20:00
- file_count: 14

## Loaded Data
- daily_rows: 3842
- one_min_rows: 2651
- moneyflow_rows: 3842
- latest_trade_date: 2026-06-24

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-24', 'latest_open': 35.81, 'latest_high': 36.44, 'latest_low': 35.3, 'latest_close': 35.35, 'latest_pre_close': 35.81, 'latest_pct_chg': -1.2846, 'latest_volume': 852772.66, 'latest_amount': 3045576.404, 'ma5': 36.356, 'ma10': 35.80800000000001, 'ma20': 36.175, 'ma60': 36.254999999999995, 'ret_1d': -0.012845573862049764, 'ret_3d': -0.021859435528500226, 'ret_5d': -0.017782717421505945, 'ret_10d': 0.020202020202020332, 'ret_20d': -0.0863272163349702, 'ret_60d': 0.10989010989010994, 'volume_ma5': 1140109.0320000001, 'volume_ma20': 933679.801, 'volume_ratio_5d': 0.7564883977900357, 'volume_ratio_20d': 0.9067128135056938, 'amount_ma5': 4158159.5741999997, 'amount_ma20': 3392052.8082500002, 'amount_ratio_5d': 0.7398181809189257, 'amount_ratio_20d': 0.8884023735202121, 'price_position_20d': 0.23432343234323452, 'price_position_60d': 0.39865871833084954, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-24', 'latest_intraday_open': 35.81, 'latest_intraday_high': 36.44, 'latest_intraday_low': 35.3, 'latest_intraday_close': 35.35, 'intraday_range_pct': 0.032248939179632265, 'close_position_in_day_range': 0.043859649122810734, 'morning_return': -0.0061435353253280756, 'afternoon_return': -0.0067434672660859896, 'last_30min_return': -0.0019762845849802257, 'last_60min_return': -0.0025395033860043936, 'morning_volume_ratio': 0.6277305958659604, 'afternoon_volume_ratio': 0.37226940413403964, 'last_30min_volume_ratio': 0.12882379460898757, 'last_60min_volume_ratio': 0.20532272927230102, 'intraday_volume_sum': 85277266.0, 'intraday_amount_sum': 3045576398.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -33267.03, 'net_mf_ratio': -0.010923065320675501, 'small_order_net': -4265.040000000008, 'medium_order_net': 1247.1699999999983, 'large_order_net': 4386.069999999992, 'extra_large_order_net': -1368.2099999999991, 'main_force_net': 3017.8599999999933, 'main_force_ratio': 0.0009908994553662798, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-24', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -9.93216586530922, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
