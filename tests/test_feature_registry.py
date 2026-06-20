from cnsv.features.feature_registry import build_feature_registry


def test_feature_registry_contains_required_fields():
    registry = build_feature_registry()
    assert registry
    required = {"feature_name", "category", "description", "source", "formula", "required", "used_in_v1_1"}
    assert required.issubset(registry[0])
    assert any(item["feature_name"] == "flow_strength_score" for item in registry)
