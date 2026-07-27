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
- snapshot_id: cnsvdata-2026-07-27-673d53156022
- latest_trade_date: 2026-07-27
- generated_at: 2026-07-27 21:16:33
- file_count: 14

## Loaded Data
- daily_rows: 3865
- one_min_rows: 8194
- moneyflow_rows: 3865
- latest_trade_date: 2026-07-27

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-07-27', 'latest_open': 33.3, 'latest_high': 33.55, 'latest_low': 32.95, 'latest_close': 33.53, 'latest_pre_close': 33.06, 'latest_pct_chg': 1.4217, 'latest_volume': 621575.92, 'latest_amount': 2070723.498, 'ma5': 33.266000000000005, 'ma10': 33.275999999999996, 'ma20': 34.5755, 'ma60': 36.586000000000006, 'ret_1d': 0.014216575922564978, 'ret_3d': 0.015445184736523343, 'ret_5d': 0.015752802181157266, 'ret_10d': -0.019877228880444298, 'ret_20d': -0.0017862459065198788, 'ret_60d': -0.1885285575992255, 'volume_ma5': 899909.184, 'volume_ma20': 1228125.4625000004, 'volume_ratio_5d': 0.6372578557268559, 'volume_ratio_20d': 0.5003472730544064, 'amount_ma5': 2991838.5942, 'amount_ma20': 4279053.23355, 'amount_ratio_5d': 0.6406128388115615, 'amount_ratio_20d': 0.47863674336108286, 'price_position_20d': 0.23214285714285723, 'price_position_60d': 0.1263250883392226, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-07-27', 'latest_intraday_open': 33.3, 'latest_intraday_high': 33.55, 'latest_intraday_low': 32.95, 'latest_intraday_close': 33.53, 'intraday_range_pct': 0.017894422904861148, 'close_position_in_day_range': 0.966666666666673, 'morning_return': -0.002702702702702564, 'afternoon_return': 0.009635651912074605, 'last_30min_return': 0.0023916292974588416, 'last_60min_return': 0.005397301349325367, 'morning_volume_ratio': 0.6047278826374097, 'afternoon_volume_ratio': 0.3952721173625902, 'last_30min_volume_ratio': 0.150022912728022, 'last_60min_volume_ratio': 0.25074632878313563, 'intraday_volume_sum': 62157592.0, 'intraday_amount_sum': 2070723492.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': 7402.44, 'net_mf_ratio': 0.0035748085184475944, 'small_order_net': -103.98999999999069, 'medium_order_net': 80.75, 'large_order_net': 635.3300000000017, 'extra_large_order_net': -612.0999999999985, 'main_force_net': 23.2300000000032, 'main_force_ratio': 1.1218301247095427e-05, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-07-27', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'positive', 'flow_strength_basic': 'positive', 'flow_strength_score': 3.5860268196946894, 'flow_continuity_3d': 1, 'flow_continuity_5d': -1, 'flow_continuity_10d': -2, 'positive_flow_days_5d': 2, 'positive_flow_days_10d': 4, 'flow_reversal_1d': True, 'flow_reversal_3d': True, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
