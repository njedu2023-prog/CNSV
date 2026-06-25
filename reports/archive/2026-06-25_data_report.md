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
- snapshot_id: cnsvdata-2026-06-25-813c4c0ad64f
- latest_trade_date: 2026-06-25
- generated_at: 2026-06-25 23:24:42
- file_count: 14

## Loaded Data
- daily_rows: 3843
- one_min_rows: 2892
- moneyflow_rows: 3843
- latest_trade_date: 2026-06-25

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-25', 'latest_open': 35.09, 'latest_high': 35.96, 'latest_low': 34.77, 'latest_close': 35.33, 'latest_pre_close': 35.35, 'latest_pct_chg': -0.0566, 'latest_volume': 921557.61, 'latest_amount': 3257080.223, 'ma5': 35.992, 'ma10': 35.835, 'ma20': 36.04050000000001, 'ma60': 36.33266666666667, 'ret_1d': -0.0005657708628006297, 'ret_3d': -0.053576212161800196, 'ret_5d': -0.04899057873485868, 'ret_10d': 0.007701083856246349, 'ret_20d': -0.07075223566543931, 'ret_60d': 0.15194000652103012, 'volume_ma5': 1097993.9100000001, 'volume_ma20': 919746.0709999999, 'volume_ratio_5d': 0.8083065602799293, 'volume_ratio_20d': 0.9870167577931784, 'amount_ma5': 3978884.3772, 'amount_ma20': 3323878.4383500004, 'amount_ratio_5d': 0.7832985158167335, 'amount_ratio_20d': 0.9602091733590569, 'price_position_20d': 0.3090507726269312, 'price_position_60d': 0.3971684053651265, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-25', 'latest_intraday_open': 35.09, 'latest_intraday_high': 35.96, 'latest_intraday_low': 34.77, 'latest_intraday_close': 35.33, 'intraday_range_pct': 0.033682422870082024, 'close_position_in_day_range': 0.4705882352941145, 'morning_return': 0.014534055286406389, 'afternoon_return': -0.007584269662921472, 'last_30min_return': 0.0022695035460993385, 'last_60min_return': 0.007701083856246349, 'morning_volume_ratio': 0.6285929319166492, 'afternoon_volume_ratio': 0.3714070680833508, 'last_30min_volume_ratio': 0.10145750953106447, 'last_60min_volume_ratio': 0.19087693280510157, 'intraday_volume_sum': 92155761.0, 'intraday_amount_sum': 3257080221.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -14970.1, 'net_mf_ratio': -0.004596171716707513, 'small_order_net': -2146.459999999992, 'medium_order_net': 2423.0899999999965, 'large_order_net': 2100.720000000001, 'extra_large_order_net': -2377.3600000000006, 'main_force_net': -276.6399999999994, 'main_force_ratio': -8.493496661411505e-05, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-25', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -4.681106683321628, 'flow_continuity_3d': -3, 'flow_continuity_5d': -3, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 4, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
