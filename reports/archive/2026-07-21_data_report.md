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
- snapshot_id: cnsvdata-2026-07-21-689cfae1b68c
- latest_trade_date: 2026-07-21
- generated_at: 2026-07-21 20:04:46
- file_count: 14

## Loaded Data
- daily_rows: 3861
- one_min_rows: 7230
- moneyflow_rows: 3861
- latest_trade_date: 2026-07-21

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-21', 'latest_open': 33.7, 'latest_high': 33.7, 'latest_low': 32.54, 'latest_close': 32.96, 'latest_pre_close': 33.01, 'latest_pct_chg': -0.1515, 'latest_volume': 932800.69, 'latest_amount': 3072219.854, 'ma5': 33.124, 'ma10': 34.268, 'ma20': 34.7905, 'ma60': 36.982000000000006, 'ret_1d': -0.0015146925174188697, 'ret_3d': -0.00121212121212122, 'ret_5d': -0.023985786200769965, 'ret_10d': -0.1170640235735333, 'ret_20d': -0.0795867076235689, 'ret_60d': -0.0964912280701753, 'volume_ma5': 1017611.186, 'volume_ma20': 1244774.1275000002, 'volume_ratio_5d': 0.8234984025361105, 'volume_ratio_20d': 0.739974070631243, 'amount_ma5': 3370886.4176, 'amount_ma20': 4357363.5904, 'amount_ratio_5d': 0.8135309486842008, 'amount_ratio_20d': 0.693137464821447, 'price_position_20d': 0.1396103896103896, 'price_position_60d': 0.0759717314487632, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-21', 'latest_intraday_open': 33.7, 'latest_intraday_high': 33.7, 'latest_intraday_low': 32.54, 'latest_intraday_close': 32.96, 'intraday_range_pct': 0.03519417475728166, 'close_position_in_day_range': 0.3620689655172417, 'morning_return': -0.03204747774480732, 'afternoon_return': 0.010423053341508393, 'last_30min_return': 0.0018237082066869803, 'last_60min_return': 0.0015192950470983568, 'morning_volume_ratio': 0.6636206497660287, 'afternoon_volume_ratio': 0.3363793502339712, 'last_30min_volume_ratio': 0.12209257692551664, 'last_60min_volume_ratio': 0.17732989670065533, 'intraday_volume_sum': 93280069.0, 'intraday_amount_sum': 3072219849.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -36341.43, 'net_mf_ratio': -0.011829046008111632, 'small_order_net': -3558.5199999999895, 'medium_order_net': -655.0099999999948, 'large_order_net': -2986.9000000000015, 'extra_large_order_net': 7200.419999999998, 'main_force_net': 4213.519999999997, 'main_force_ratio': 0.0013714903881354831, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-21', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -10.45755561997615, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 3, 'flow_reversal_1d': True, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
