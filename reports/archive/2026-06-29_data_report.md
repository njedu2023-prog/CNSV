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
- snapshot_id: cnsvdata-2026-06-29-d9c53da4c68b
- latest_trade_date: 2026-06-29
- generated_at: 2026-06-30 00:42:00
- file_count: 14

## Loaded Data
- daily_rows: 3845
- one_min_rows: 3374
- moneyflow_rows: 3845
- latest_trade_date: 2026-06-29

## Validation
- status: PASS
- failed_count: 0
- warn_count: 0

## Feature Summary
- price_volume: {'latest_trade_date': '2026-06-29', 'latest_open': 33.35, 'latest_high': 33.89, 'latest_low': 32.87, 'latest_close': 33.59, 'latest_pre_close': 33.4, 'latest_pct_chg': 0.5689, 'latest_volume': 904846.93, 'latest_amount': 3015548.313, 'ma5': 34.696, 'ma10': 35.6, 'ma20': 35.612, 'ma60': 36.426, 'ret_1d': 0.005688622754491224, 'ret_3d': -0.04978783592644975, 'ret_5d': -0.10018751674256621, 'ret_10d': -0.0372599598738893, 'ret_20d': -0.10139111824505076, 'ret_60d': 0.09950900163666132, 'volume_ma5': 1029749.9079999998, 'volume_ma20': 939885.451, 'volume_ratio_5d': 0.8183742807391806, 'volume_ratio_20d': 0.9675596916663107, 'amount_ma5': 3604979.5612000003, 'amount_ma20': 3356494.3494999995, 'amount_ratio_5d': 0.7647495086908914, 'amount_ratio_20d': 0.8979387136045913, 'price_position_20d': 0.14257425742574364, 'price_position_60d': 0.24500768049155178, 'new_high_20d': False, 'new_low_20d': True, 'new_high_60d': False, 'new_low_60d': False}
- minute_structure: {'latest_intraday_date': '2026-06-29', 'latest_intraday_open': 33.35, 'latest_intraday_high': 33.89, 'latest_intraday_low': 32.87, 'latest_intraday_close': 33.59, 'intraday_range_pct': 0.03036618041083665, 'close_position_in_day_range': 0.7058823529411802, 'morning_return': 0.004501800720288163, 'afternoon_return': 0.0035853002688976954, 'last_30min_return': 0.004185351270552973, 'last_60min_return': -0.0026722090261281917, 'morning_volume_ratio': 0.6459267646517848, 'afternoon_volume_ratio': 0.3540732353482152, 'last_30min_volume_ratio': 0.08457718920480838, 'last_60min_volume_ratio': 0.1661958227564523, 'intraday_volume_sum': 90484693.0, 'intraday_amount_sum': 3015548303.0, 'late_session_strength': True, 'late_session_weakness': False, 'intraday_reversal_flag': False}
- moneyflow: {'net_mf_amount': -5442.32, 'net_mf_ratio': -0.0018047530449232766, 'small_order_net': 3340.75, 'medium_order_net': 5662.729999999996, 'large_order_net': -3157.469999999994, 'extra_large_order_net': -5846.020000000004, 'main_force_net': -9003.489999999998, 'main_force_ratio': -0.0029856891899844675, 'main_force_available': True, 'moneyflow_latest_trade_date': '2026-06-29', 'moneyflow_lag_days': 0, 'moneyflow_strength_basic': 'negative', 'flow_strength_basic': 'negative', 'flow_strength_score': -4.790442234907744, 'flow_continuity_3d': -3, 'flow_continuity_5d': -5, 'flow_continuity_10d': -4, 'positive_flow_days_5d': 0, 'positive_flow_days_10d': 3, 'flow_reversal_1d': False, 'flow_reversal_3d': False, 'price_flow_confirm': False, 'price_flow_divergence': True, 'volume_flow_confirm': 'neutral', 'moneyflow_warning': '', 'can_use_as_strong_factor': True}

## Forbidden Actions
- formal_signal_generation
- auto_order
- broker_api

## Next Step
- Continue V1.1 feature enhancement only after V1.0 data gate remains stable.
