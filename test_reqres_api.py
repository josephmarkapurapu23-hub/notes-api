import requests

BASE = "https://jsonplaceholder.typicode.com"

def test_list_posts():
    r = requests.get(f"{BASE}/posts", timeout=10)
    print("Status Code:", r.status_code)
    print("Response Body:", r.text[:200])
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

if __name__ == "__main__":
    test_list_posts()
    print("Test ran!")

