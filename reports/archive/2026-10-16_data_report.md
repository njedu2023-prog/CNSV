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
- snapshot_id: cnsvdata-2026-10-16-28295e80612f
- latest_trade_date: 2026-10-16
- generated_at: 2026-10-16 22:43:58
- file_count: 14

## Loaded Data
- daily_rows: 3918
- one_min_rows: 20967
- moneyflow_rows: 3918
- latest_trade_date: 2026-10-16

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-16', 'latest_open': 35.41, 'latest_high': 36.45, 'latest_low': 35.41, 'latest_close': 35.77, 'latest_pre_close': 35.45, 'latest_pct_chg': 0.9027, 'latest_volume': 986563.21, 'latest_amount': 3542691.105, 'ma5': 37.29600000000001, 'ma10': 38.096, 'ma20': 38.5945, 'ma60': 35.934333333333335, 'ret_1d': 0.009026798307475215, 'ret_3d': -0.08633461047254143, 'ret_5d': -0.07187337830825102, 'ret_10d': -0.06090837490154899, 'ret_20d': -0.12371386575208221, 'ret_60d': 0.08393939393939398, 'volume_ma5': 1128426.236, 'volume_ma20': 1112118.772, 'volume_ratio_5d': 0.86364992425597, 'volume_ratio_20d': 0.8573884474697487, 'amount_ma5': 4183423.0222000005, 'amount_ma20': 4296960.65505, 'amount_ratio_5d': 0.8253269388727336, 'amount_ratio_20d': 0.7912996111135678, 'price_position_20d': 0.19373219373219458, 'price_position_60d': 0.3933547695605576, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-16', 'latest_intraday_open': 35.41, 'latest_intraday_high': 36.45, 'latest_intraday_low': 35.41, 'latest_intraday_close': 35.77, 'intraday_range_pct': 0.02907464355605273, 'close_position_in_day_range': 0.34615384615385036, 'morning_return': 0.02315730019768436, 'afternoon_return': -0.012696660226331646, 'last_30min_return': 0.003647586980920492, 'last_60min_return': -0.0008379888268155167, 'morning_volume_ratio': 0.6156781581182214, 'afternoon_volume_ratio': 0.38432184188177865, 'last_30min_volume_ratio': 0.16226509196506528, 'last_60min_volume_ratio': 0.240996813574672, 'intraday_volume_sum': 98656321.0, 'intraday_amount_sum': 3542691105.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -763.75, 'net_mf_ratio': -0.00021558470026417954, 'small_order_net': 14042.62000000001, 'medium_order_net': 18677.940000000002, 'large_order_net': -30353.04999999999, 'extra_large_order_net': -2367.5, 'main_force_net': -32720.54999999999, 'main_force_ratio': -0.009236071966257411, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-16', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -9.45165666652159, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
