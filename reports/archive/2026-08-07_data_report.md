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
- snapshot_id: cnsvdata-2026-08-07-b72389af014e
- latest_trade_date: 2026-08-07
- generated_at: 2026-08-07 20:05:48
- file_count: 14

## Loaded Data
- daily_rows: 3874
- one_min_rows: 10363
- moneyflow_rows: 3874
- latest_trade_date: 2026-08-07

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-07', 'latest_open': 34.9, 'latest_high': 35.35, 'latest_low': 34.58, 'latest_close': 34.85, 'latest_pre_close': 34.9, 'latest_pct_chg': -0.1433, 'latest_volume': 955452.95, 'latest_amount': 3340342.414, 'ma5': 34.906, 'ma10': 34.609, 'ma20': 33.9765, 'ma60': 35.6365, 'ret_1d': -0.0014326647564468775, 'ret_3d': 0.010730858468677607, 'ret_5d': -0.009380329732802672, 'ret_10d': 0.05414398064125825, 'ret_20d': -0.05912526997840162, 'ret_60d': -0.1335156638488314, 'volume_ma5': 805752.976, 'volume_ma20': 1016979.508, 'volume_ratio_5d': 1.1776167952836667, 'volume_ratio_20d': 0.8958430953472983, 'amount_ma5': 2807118.8616000004, 'amount_ma20': 3450805.7971, 'amount_ratio_5d': 1.182036287100348, 'amount_ratio_20d': 0.9161223109799187, 'price_position_20d': 0.5681818181818186, 'price_position_60d': 0.28765690376569053, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-07', 'latest_intraday_open': 34.9, 'latest_intraday_high': 35.35, 'latest_intraday_low': 34.58, 'latest_intraday_close': 34.85, 'intraday_range_pct': 0.022094691535150736, 'close_position_in_day_range': 0.35064935064935326, 'morning_return': 0.0031572904707233285, 'afternoon_return': -0.0028612303290415086, 'last_30min_return': 0.0011490950876185124, 'last_60min_return': 0.001436781609195581, 'morning_volume_ratio': 0.5245425638175066, 'afternoon_volume_ratio': 0.47545743618249336, 'last_30min_volume_ratio': 0.10180496067336439, 'last_60min_volume_ratio': 0.198857725019322, 'intraday_volume_sum': 95545295.0, 'intraday_amount_sum': 3340342426.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -5431.48, 'net_mf_ratio': -0.0016260249180550027, 'small_order_net': 13556.300000000003, 'medium_order_net': 2481.7699999999895, 'large_order_net': -21625.149999999994, 'extra_large_order_net': 5587.090000000004, 'main_force_net': -16038.05999999999, 'main_force_ratio': -0.004801322143736367, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-07', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -6.4273470617913695, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
