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
- snapshot_id: cnsvdata-2026-09-09-8eaa1bf1aff6
- latest_trade_date: 2026-09-09
- generated_at: 2026-09-09 22:23:39
- file_count: 14

## Loaded Data
- daily_rows: 3897
- one_min_rows: 15906
- moneyflow_rows: 3897
- latest_trade_date: 2026-09-09

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-09-09', 'latest_open': 38.84, 'latest_high': 39.69, 'latest_low': 38.45, 'latest_close': 39.53, 'latest_pre_close': 39.08, 'latest_pct_chg': 1.1515, 'latest_volume': 1193542.24, 'latest_amount': 4688484.622, 'ma5': 37.756, 'ma10': 36.052, 'ma20': 34.821000000000005, 'ma60': 34.788000000000004, 'ret_1d': 0.011514841351074834, 'ret_3d': 0.05497731518548177, 'ret_5d': 0.16504568228706162, 'ret_10d': 0.15889768396364712, 'ret_20d': 0.16642077308940695, 'ret_60d': 0.0983606557377048, 'volume_ma5': 1879003.7920000001, 'volume_ma20': 958784.4715, 'volume_ratio_5d': 0.6696540329941963, 'volume_ratio_20d': 1.283343602182896, 'amount_ma5': 7052086.602, 'amount_ma20': 3419556.55185, 'amount_ratio_5d': 0.710608867935514, 'amount_ratio_20d': 1.425310922090409, 'price_position_20d': 0.9774647887323948, 'price_position_60d': 0.9789196310935446, 'new_high_20d': True, 'new_low_20d': False, 'new_high_60d': True, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-09-09', 'latest_intraday_open': 38.84, 'latest_intraday_high': 39.69, 'latest_intraday_low': 38.45, 'latest_intraday_close': 39.53, 'intraday_range_pct': 0.031368580824689976, 'close_position_in_day_range': 0.8709677419354861, 'morning_return': 0.01287332646755912, 'afternoon_return': 0.0048296898830706425, 'last_30min_return': 0.0, 'last_60min_return': 0.002536139994927744, 'morning_volume_ratio': 0.6155645651887444, 'afternoon_volume_ratio': 0.38443543481125564, 'last_30min_volume_ratio': 0.11814509388457002, 'last_60min_volume_ratio': 0.2117855250770178, 'intraday_volume_sum': 119354224.0, 'intraday_amount_sum': 4688484629.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 41016.62, 'net_mf_ratio': 0.008748374647009774, 'small_order_net': 1992.9600000000064, 'medium_order_net': -5284.580000000002, 'large_order_net': 9034.740000000005, 'extra_large_order_net': -5743.12999999999, 'main_force_net': 3291.610000000015, 'main_force_ratio': 0.0007020626631800467, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-09-09', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 9.45043731018982, 'flow_continuity_3d': 1, 'flow_continuity_5d': 3, 'flow_continuity_10d': 2, 'positive_flow_days_5d': 4, 'positive_flow_days_10d': 6, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
