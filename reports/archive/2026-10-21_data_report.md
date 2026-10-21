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
- snapshot_id: cnsvdata-2026-10-21-6217d52db1c2
- latest_trade_date: 2026-10-21
- generated_at: 2026-10-21 23:02:14
- file_count: 14

## Loaded Data
- daily_rows: 3921
- one_min_rows: 21690
- moneyflow_rows: 3921
- latest_trade_date: 2026-10-21

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-21', 'latest_open': 35.32, 'latest_high': 35.52, 'latest_low': 34.65, 'latest_close': 34.86, 'latest_pre_close': 35.22, 'latest_pct_chg': -1.0221, 'latest_volume': 557477.38, 'latest_amount': 1951484.454, 'ma5': 35.472, 'ma10': 37.097, 'ma20': 38.057, 'ma60': 36.06483333333333, 'ret_1d': -0.010221465076660996, 'ret_3d': -0.025440313111546042, 'ret_5d': -0.08527945421149308, 'ret_10d': -0.10843989769820972, 'ret_20d': -0.08647798742138357, 'ret_60d': 0.05764563106796117, 'volume_ma5': 966531.132, 'volume_ma20': 981447.6640000001, 'volume_ratio_5d': 0.5461503581103803, 'volume_ratio_20d': 0.5495203059128901, 'amount_ma5': 3446678.5019999994, 'amount_ma20': 3747158.8784499997, 'amount_ratio_5d': 0.5284265222570759, 'amount_ratio_20d': 0.5024921372291112, 'price_position_20d': 0.06410256410256449, 'price_position_60d': 0.2567873303167417, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-21', 'latest_intraday_open': 35.32, 'latest_intraday_high': 35.52, 'latest_intraday_low': 34.65, 'latest_intraday_close': 34.86, 'intraday_range_pct': 0.0249569707401034, 'close_position_in_day_range': 0.2413793103448273, 'morning_return': -0.013016411997736288, 'afternoon_return': -0.0005733944954129377, 'last_30min_return': -0.0008598452278589797, 'last_60min_return': -0.0028604118993135197, 'morning_volume_ratio': 0.5673686168217265, 'afternoon_volume_ratio': 0.43263138317827354, 'last_30min_volume_ratio': 0.2324475479166527, 'last_60min_volume_ratio': 0.31613718569173155, 'intraday_volume_sum': 55747738.0, 'intraday_amount_sum': 1951484452.0, 'late_session_strength': False, 'late_session_weakness': True, 'intraday_reversal_flag': True}
- moneyflow: {'net_mf_amount': -16804.72, 'net_mf_ratio': -0.008611249741475011, 'small_order_net': 19126.409999999996, 'medium_order_net': 15840.169999999998, 'large_order_net': -2580.8199999999997, 'extra_large_order_net': -32385.760000000002, 'main_force_net': -34966.58, 'main_force_ratio': -0.01791793930427078, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-21', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -26.529189045745788, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
