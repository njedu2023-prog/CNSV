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
- snapshot_id: cnsvdata-2026-06-30-3b979aad980c
- latest_trade_date: 2026-06-30
- generated_at: 2026-06-30 23:41:27
- file_count: 14

## Loaded Data
- daily_rows: 3846
- one_min_rows: 3615
- moneyflow_rows: 3846
- latest_trade_date: 2026-06-30

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-30', 'latest_open': 33.3, 'latest_high': 34.36, 'latest_low': 32.86, 'latest_close': 33.79, 'latest_pre_close': 33.59, 'latest_pct_chg': 0.5954, 'latest_volume': 888221.1, 'latest_amount': 2979364.142, 'ma5': 34.292, 'ma10': 35.388000000000005, 'ma20': 35.4645, 'ma60': 36.475166666666674, 'ret_1d': 0.005954153021732633, 'ret_3d': -0.04358901783187086, 'ret_5d': -0.05640882435074013, 'ret_10d': -0.059036480089111554, 'ret_20d': -0.08029395753946655, 'ret_60d': 0.09565499351491558, 'volume_ma5': 957587.926, 'volume_ma20': 946343.168, 'volume_ratio_5d': 0.862560018796331, 'volume_ratio_20d': 0.9450312259381914, 'amount_ma5': 3286508.8792000003, 'amount_ma20': 3364699.07395, 'amount_ratio_5d': 0.8264579844131626, 'amount_ratio_20d': 0.8876416379023017, 'price_position_20d': 0.1837944664031619, 'price_position_60d': 0.26036866359447003, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-30', 'latest_intraday_open': 33.3, 'latest_intraday_high': 34.36, 'latest_intraday_low': 32.86, 'latest_intraday_close': 33.79, 'intraday_range_pct': 0.04439183190292986, 'close_position_in_day_range': 0.6199999999999998, 'morning_return': 0.026726726726726824, 'afternoon_return': -0.011699327288680839, 'last_30min_return': 0.0035640035640034373, 'last_60min_return': 0.0032660332541567527, 'morning_volume_ratio': 0.6598989936176927, 'afternoon_volume_ratio': 0.3401010063823073, 'last_30min_volume_ratio': 0.08887635071943235, 'last_60min_volume_ratio': 0.1512779306864023, 'intraday_volume_sum': 88822110.0, 'intraday_amount_sum': 2979364141.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -23117.68, 'net_mf_ratio': -0.007759266373019267, 'small_order_net': -3592.689999999988, 'medium_order_net': 1568.4599999999919, 'large_order_net': -212.68000000000757, 'extra_large_order_net': 2236.909999999996, 'main_force_net': 2024.2299999999886, 'main_force_ratio': 0.0006794167827505486, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-30', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': -7.079849590268718, 'flow_continuity_3d': -3, 'flow_continuity_5d': -5, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 0, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
