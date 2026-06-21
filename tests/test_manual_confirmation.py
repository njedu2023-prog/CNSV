from cnsv.live.manual_confirmation import build_manual_confirmation_panel
def test_manual_confirmation_panel_uses_allowed_status():
 p=build_manual_confirmation_panel("session","snapshot","review_required",[{"id":"check","required":True}])
 assert p["manual_review_status"]=="not_started"; assert p["decision_session_id"]=="session"; assert p["manual_confirmation_items"][0]["confirmed"] is False
