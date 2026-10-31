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
- snapshot_id: cnsvdata-2026-10-30-e4b07ef535de
- latest_trade_date: 2026-10-30
- generated_at: 2026-10-31 23:41:38
- file_count: 14

## Loaded Data
- daily_rows: 3928
- one_min_rows: 23377
- moneyflow_rows: 3928
- latest_trade_date: 2026-10-30

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-30', 'latest_open': 33.8, 'latest_high': 34.05, 'latest_low': 33.13, 'latest_close': 33.39, 'latest_pre_close': 33.86, 'latest_pct_chg': -1.3881, 'latest_volume': 698965.21, 'latest_amount': 2343287.997, 'ma5': 34.166, 'ma10': 34.660000000000004, 'ma20': 36.378, 'ma60': 36.1355, 'ret_1d': -0.013880685174246898, 'ret_3d': -0.0360854503464203, 'ret_5d': -0.04871794871794877, 'ret_10d': -0.066536203522505, 'ret_20d': -0.12339196639537942, 'ret_60d': -0.03580710366734052, 'volume_ma5': 742436.968, 'volume_ma20': 893966.6475, 'volume_ratio_5d': 0.8878422078675535, 'volume_ratio_20d': 0.7843408129875322, 'amount_ma5': 2537581.8532, 'amount_ma20': 3275517.4148000004, 'amount_ratio_5d': 0.8665400109994382, 'amount_ratio_20d': 0.7140750031599009, 'price_position_20d': 0.03132530120481905, 'price_position_60d': 0.0904977375565608, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-30', 'latest_intraday_open': 33.8, 'latest_intraday_high': 34.05, 'latest_intraday_low': 33.13, 'latest_intraday_close': 33.39, 'intraday_range_pct': 0.027553159628631165, 'close_position_in_day_range': 0.2826086956521734, 'morning_return': -0.0062130177514790885, 'afternoon_return': -0.005954153021732744, 'last_30min_return': -0.004472271914132353, 'last_60min_return': -0.01213017751479284, 'morning_volume_ratio': 0.5282947344403593, 'afternoon_volume_ratio': 0.47170526555964065, 'last_30min_volume_ratio': 0.19150478176159869, 'last_60min_volume_ratio': 0.27030525596545785, 'intraday_volume_sum': 69896521.0, 'intraday_amount_sum': 2343287997.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -15375.89, 'net_mf_ratio': -0.00656167317874927, 'small_order_net': -1533.8600000000006, 'medium_order_net': -3607.199999999997, 'large_order_net': 8522.159999999996, 'extra_large_order_net': -3381.109999999997, 'main_force_net': 5141.049999999999, 'main_force_ratio': 0.0021939471403352217, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-30', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -4.367726038414048, 'flow_continuity_3d': -3, 'flow_continuity_5d': -5, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 0, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
