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
- snapshot_id: cnsvdata-2026-10-22-acf74a3708b5
- latest_trade_date: 2026-10-22
- generated_at: 2026-10-22 23:02:08
- file_count: 14

## Loaded Data
- daily_rows: 3922
- one_min_rows: 21931
- moneyflow_rows: 3922
- latest_trade_date: 2026-10-22

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-10-22', 'latest_open': 35.08, 'latest_high': 35.08, 'latest_low': 34.16, 'latest_close': 34.53, 'latest_pre_close': 34.86, 'latest_pct_chg': -0.9466, 'latest_volume': 631807.71, 'latest_amount': 2181605.315, 'ma5': 35.288000000000004, 'ma10': 36.568999999999996, 'ma20': 37.894, 'ma60': 36.09, 'ret_1d': -0.009466437177280462, 'ret_3d': -0.04242928452579042, 'ret_5d': -0.02595204513399163, 'ret_10d': -0.13262999246420504, 'ret_20d': -0.08626620799153206, 'ret_60d': 0.045729860690490565, 'volume_ma5': 703940.892, 'volume_ma20': 968074.8629999999, 'volume_ratio_5d': 0.6536858349224905, 'volume_ratio_20d': 0.6437507909744231, 'amount_ma5': 2492184.1484, 'amount_ma20': 3686533.5669, 'amount_ratio_5d': 0.6329587496292686, 'amount_ratio_20d': 0.5822025128281761, 'price_position_20d': 0.05089408528198135, 'price_position_60d': 0.21945701357466046, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-10-22', 'latest_intraday_open': 35.08, 'latest_intraday_high': 35.08, 'latest_intraday_low': 34.16, 'latest_intraday_close': 34.53, 'intraday_range_pct': 0.02664349840718221, 'close_position_in_day_range': 0.40217391304348243, 'morning_return': -0.015108323831242942, 'afternoon_return': -0.0005788712011576269, 'last_30min_return': -0.0014459224985540198, 'last_60min_return': -0.0005788712011576269, 'morning_volume_ratio': 0.486211255636624, 'afternoon_volume_ratio': 0.513788744363376, 'last_30min_volume_ratio': 0.17010480926229912, 'last_60min_volume_ratio': 0.2882874917749896, 'intraday_volume_sum': 63180771.0, 'intraday_amount_sum': 2181605318.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -18818.29, 'net_mf_ratio': -0.008625891159418999, 'small_order_net': 1815.8800000000047, 'medium_order_net': 12675.410000000003, 'large_order_net': -8018.270000000004, 'extra_large_order_net': -6473.02, 'main_force_net': -14491.290000000005, 'main_force_ratio': -0.0066424893175510095, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-10-22', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -15.268380476970007, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': -6, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 2, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
