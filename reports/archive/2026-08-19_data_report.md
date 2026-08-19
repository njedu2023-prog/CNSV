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
- snapshot_id: cnsvdata-2026-08-19-d140bde463c5
- latest_trade_date: 2026-08-19
- generated_at: 2026-08-19 20:05:47
- file_count: 14

## Loaded Data
- daily_rows: 3882
- one_min_rows: 12291
- moneyflow_rows: 3882
- latest_trade_date: 2026-08-19

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-08-19', 'latest_open': 33.43, 'latest_high': 33.43, 'latest_low': 32.94, 'latest_close': 33.14, 'latest_pre_close': 33.49, 'latest_pct_chg': -1.0451, 'latest_volume': 641601.34, 'latest_amount': 2124149.401, 'ma5': 33.496, 'ma10': 33.992000000000004, 'ma20': 34.153999999999996, 'ma60': 35.001, 'ret_1d': -0.010450880859958267, 'ret_3d': -0.00837821663674454, 'ret_5d': -0.022130421953378554, 'ret_10d': -0.05852272727272734, 'ret_20d': 0.003634161114475898, 'ret_60d': -0.14344791935900747, 'volume_ma5': 617232.4099999999, 'volume_ma20': 800862.385, 'volume_ratio_5d': 1.047367737099833, 'volume_ratio_20d': 0.7796195552612059, 'amount_ma5': 2070187.2584, 'amount_ma20': 2735887.1336, 'amount_ratio_5d': 1.029832811616938, 'amount_ratio_20d': 0.755952677888541, 'price_position_20d': 0.17164179104477645, 'price_position_60d': 0.13181242078580468, 'new_high_20d': False, 'new_low_20d': False, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-08-19', 'latest_intraday_open': 33.43, 'latest_intraday_high': 33.43, 'latest_intraday_low': 32.94, 'latest_intraday_close': 33.14, 'intraday_range_pct': 0.014785757392878756, 'close_position_in_day_range': 0.40816326530612657, 'morning_return': -0.008973975471133655, 'afternoon_return': 0.0003018412315121122, 'last_30min_return': 0.003026634382566673, 'last_60min_return': 0.004851425106125129, 'morning_volume_ratio': 0.5514394810958468, 'afternoon_volume_ratio': 0.44856051890415316, 'last_30min_volume_ratio': 0.1676973586121251, 'last_60min_volume_ratio': 0.25218714474629994, 'intraday_volume_sum': 64160134.0, 'intraday_amount_sum': 2124149404.0, 'late_session_strength': False, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -26278.14, 'net_mf_ratio': -0.01237113547080486, 'small_order_net': 25552.810000000005, 'medium_order_net': 7409.489999999998, 'large_order_net': -10831.809999999998, 'extra_large_order_net': -22130.5, 'main_force_net': -32962.31, 'main_force_ratio': -0.015517886823065322, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-08-19', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -27.889022293870184, 'flow_continuity_3d': -1, 'flow_continuity_5d': -3, 'flow_continuity_10d': -8, 'positive_flow_days_5d': 1, 'positive_flow_days_10d': 1, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': True, 'price_flow_divergence': False, 'volume_flow_confirm': 'outflow_confirmed', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
