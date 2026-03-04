"""
Tests for CropGuard Ghana — Chatbot API endpoints.
"""

import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from app import app, process_message, DISEASE_KB


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ── Health ──────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_ok(self, client):
        r = client.get('/health')
        assert r.status_code == 200

    def test_health_has_disease_count(self, client):
        d = client.get('/health').get_json()
        assert d['diseases_in_kb'] == len(DISEASE_KB)
        assert d['status'] == 'healthy'


# ── Disease API ──────────────────────────────────────────────────────────────

class TestDiseaseAPI:
    def test_list_all_diseases(self, client):
        d = client.get('/api/diseases').get_json()
        assert d['status'] == 'success'
        assert d['count'] == len(DISEASE_KB)

    def test_filter_by_crop_maize(self, client):
        d = client.get('/api/diseases?crop=maize').get_json()
        assert all(v['crop'] == 'maize' for v in d['diseases'].values())
        assert d['count'] >= 3

    def test_get_disease_by_name(self, client):
        r = client.get('/api/diseases/fall-armyworm')
        assert r.status_code == 200
        d = r.get_json()
        assert d['disease'] == 'fall armyworm'
        assert 'symptoms' in d['data']
        assert 'treatment' in d['data']

    def test_get_unknown_disease_404(self, client):
        r = client.get('/api/diseases/alien-rot')
        assert r.status_code == 404

    def test_all_diseases_have_required_fields(self, client):
        d = client.get('/api/diseases').get_json()
        for name, info in d['diseases'].items():
            for field in ['crop', 'severity', 'season']:
                assert field in info, f"{name} missing field: {field}"


# ── Chat API ─────────────────────────────────────────────────────────────────

class TestChatAPI:
    def test_chat_endpoint_ok(self, client):
        r = client.post('/api/chat', json={'message': 'hello'})
        assert r.status_code == 200

    def test_chat_returns_response_object(self, client):
        d = client.post('/api/chat', json={'message': 'hello'}).get_json()
        assert 'response' in d
        assert 'message' in d['response']
        assert 'type' in d['response']

    def test_empty_message_returns_400(self, client):
        r = client.post('/api/chat', json={'message': ''})
        assert r.status_code == 400

    def test_no_body_returns_400(self, client):
        r = client.post('/api/chat', json={})
        assert r.status_code == 400

    def test_greeting_detected(self, client):
        d = client.post('/api/chat', json={'message': 'hello'}).get_json()
        assert d['response']['type'] == 'greeting'

    def test_akwaaba_greeting(self, client):
        d = client.post('/api/chat', json={'message': 'akwaaba'}).get_json()
        assert d['response']['type'] == 'greeting'

    def test_farewell_detected(self, client):
        d = client.post('/api/chat', json={'message': 'thank you bye'}).get_json()
        assert d['response']['type'] == 'farewell'

    def test_help_detected(self, client):
        d = client.post('/api/chat', json={'message': 'help'}).get_json()
        assert d['response']['type'] == 'help'

    def test_list_crops_detected(self, client):
        d = client.post('/api/chat', json={'message': 'list crops'}).get_json()
        assert d['response']['type'] == 'crop_list'

    def test_crop_query_maize(self, client):
        d = client.post('/api/chat', json={'message': 'what diseases affect maize'}).get_json()
        assert d['response']['type'] == 'crop_diseases'
        assert d['response']['crop'] == 'maize'

    def test_crop_query_cocoa(self, client):
        d = client.post('/api/chat', json={'message': 'diseases in cocoa'}).get_json()
        assert d['response']['type'] == 'crop_diseases'

    def test_disease_match_fall_armyworm(self, client):
        d = client.post('/api/chat', json={'message': 'tell me about fall armyworm'}).get_json()
        assert d['response']['type'] == 'disease_info'
        assert 'fall armyworm' in d['response']['disease']

    def test_disease_match_black_pod(self, client):
        d = client.post('/api/chat', json={'message': 'black pod disease cocoa'}).get_json()
        assert d['response']['type'] == 'disease_info'

    def test_alias_match_msv(self, client):
        d = client.post('/api/chat', json={'message': 'my maize has msv'}).get_json()
        assert d['response']['type'] == 'disease_info'

    def test_not_found_returns_helpful_message(self, client):
        d = client.post('/api/chat', json={'message': 'xyzzy random gibberish'}).get_json()
        assert d['response']['type'] == 'not_found'
        assert len(d['response']['message']) > 0


# ── Process message unit tests ────────────────────────────────────────────────

class TestProcessMessage:
    def test_greeting_variants(self):
        for g in ['hello', 'hi', 'hey', 'good morning', 'akwaaba']:
            r = process_message(g)
            assert r['type'] == 'greeting', f"Failed for: {g}"

    def test_disease_response_has_symptoms(self):
        r = process_message('fall armyworm')
        assert r['type'] == 'disease_info'
        assert 'Symptoms' in r['message'] or 'symptoms' in r['message'].lower()

    def test_disease_response_has_treatment(self):
        r = process_message('black pod disease')
        assert 'Treatment' in r['message'] or 'treatment' in r['message'].lower()

    def test_10_diseases_supported(self):
        assert len(DISEASE_KB) >= 10

    def test_all_5_crops_covered(self):
        crops = {v['crop'] for v in DISEASE_KB.values()}
        assert 'maize' in crops
        assert 'cocoa' in crops
        assert 'cassava' in crops
        assert 'tomato' in crops
        assert 'yam' in crops
