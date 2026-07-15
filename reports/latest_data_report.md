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
- snapshot_id: cnsvdata-2026-07-15-423a7c34c060
- latest_trade_date: 2026-07-15
- generated_at: 2026-07-15 21:55:32
- file_count: 14

## Loaded Data
- daily_rows: 3857
- one_min_rows: 6266
- moneyflow_rows: 3857
- latest_trade_date: 2026-07-15

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-15', 'latest_open': 33.55, 'latest_high': 34.38, 'latest_low': 33.33, 'latest_close': 34.31, 'latest_pre_close': 33.77, 'latest_pct_chg': 1.5991, 'latest_volume': 995212.94, 'latest_amount': 3388022.289, 'ma5': 35.078, 'ma10': 35.785, 'ma20': 35.546499999999995, 'ma60': 37.14533333333334, 'ret_1d': 0.015990524133846495, 'ret_3d': -0.07370410367170621, 'ret_5d': -0.046414674819343915, 'ret_10d': -0.025007104290991622, 'ret_20d': -0.04667963323145319, 'ret_60d': 0.04859413202933993, 'volume_ma5': 1552615.982, 'volume_ma20': 1282520.6030000004, 'volume_ratio_5d': 0.6106173370714049, 'volume_ratio_20d': 0.7822827624210114, 'amount_ma5': 5459092.705, 'amount_ma20': 4571304.173800001, 'amount_ratio_5d': 0.5856929729989139, 'amount_ratio_20d': 0.745635363364127, 'price_position_20d': 0.2685185185185191, 'price_position_60d': 0.18515205724508052, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-15', 'latest_intraday_open': 33.55, 'latest_intraday_high': 34.38, 'latest_intraday_low': 33.33, 'latest_intraday_close': 34.31, 'intraday_range_pct': 0.03060332264645888, 'close_position_in_day_range': 0.9333333333333333, 'morning_return': 0.012216924910607663, 'afternoon_return': 0.010008831321754563, 'last_30min_return': 0.0005832604257802743, 'last_60min_return': 0.006748826291079979, 'morning_volume_ratio': 0.6265019624845312, 'afternoon_volume_ratio': 0.3734980375154688, 'last_30min_volume_ratio': 0.1250052074282716, 'last_60min_volume_ratio': 0.21512535799624952, 'intraday_volume_sum': 99521294.0, 'intraday_amount_sum': 3388022280.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 3187.58, 'net_mf_ratio': 0.0009408379662522344, 'small_order_net': 3842.050000000003, 'medium_order_net': -1936.9600000000064, 'large_order_net': 404.0100000000093, 'extra_large_order_net': -2309.0999999999985, 'main_force_net': -1905.0899999999892, 'main_force_ratio': -0.0005623014955318641, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-15', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'mixed', 'flow_strength_basic': 'mixed', 'flow_strength_score': 0.3785364707203702, 'flow_continuity_3d': -1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
