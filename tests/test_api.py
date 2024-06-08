import requests
from colorama import Fore, Style
from tabulate import tabulate
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://localhost:8000"
CORRECT_USERNAME = os.getenv("ADMIN_USERNAME")
CORRECT_PASSWORD = os.getenv("ADMIN_PASSWORD")
INCORRECT_USERNAME = "baduser"
INCORRECT_PASSWORD = "badpass"

def make_request(method, url, auth=None, data=None, params=None):
    try:
        headers = {'Content-Type': 'application/json'}
        if method == 'GET':
            response = requests.get(url, auth=auth, params=params, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, auth=auth, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, auth=auth, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, auth=auth, headers=headers)
        else:
            response = None
        return response.status_code, response.json() if response and response.content else {}
    except Exception as e:
        return None, str(e)

def test_endpoints():
    results = []

    # Security Test: Login with correct and incorrect credentials
    print("Testing POST /room with Correct Credentials...")
    minimal_room_data = {
        "name": "Basic Room",
        "description": "A simple test room.",
        "room_url": "https://tryhackme.com/room/basicroom",
        "tags": ["test"],
        "tasks": [
            {
                "title": "Task 1",
                "description": "A simple test task.",
                "questions": [
                    {"number": 1, "question": "What is the task?", "solution": "Just a simple task."}
                ]
            }
        ]
    }
    status, content = make_request('POST', f"{BASE_URL}/room", auth=(CORRECT_USERNAME, CORRECT_PASSWORD), data=minimal_room_data)
    post_room_result = "Success" if status != 422 else "Fail"
    results.append(["POST /room", "Create Room with Correct Credentials", status, post_room_result])
    print(Fore.GREEN + "✅ Test Passed: POST /room with Correct Credentials" if status != 422 else Fore.RED + f"❌ Test Failed: POST /room - {content}")

    # Test POST request with Incorrect Credentials
    print("Testing POST /room with Incorrect Credentials...")
    status, _ = make_request('POST', f"{BASE_URL}/room", auth=(INCORRECT_USERNAME, INCORRECT_PASSWORD), data=minimal_room_data)
    post_room_incorrect_result = "Success" if status == 401 else "Fail"
    results.append(["POST /room", "Create Room with Incorrect Credentials", status, post_room_incorrect_result])
    print(Fore.GREEN + "✅ Test Passed: POST /room with Incorrect Credentials" if status == 401 else Fore.RED + "❌ Test Failed: POST /room with Incorrect Credentials")


    # Test Search Functionality
    print("Testing GET /search...")
    status, content = make_request('GET', f"{BASE_URL}/search", params={'keyword': 'web'})
    search_result = "Success" if status == 200 and 'web' in str(content).lower() else "Fail"
    results.append(["GET /search", "Search Keyword: web", status, search_result])
    print(Fore.GREEN + "✅ Test Passed: GET /search" if status == 200 and 'web' in str(content).lower() else Fore.RED + "❌ Test Failed: GET /search")

    # Test Room Retrieval by URL
    test_url = "https://tryhackme.com/room/advancedwebsecurity"
    print("Testing GET /room_by_url...")
    status, content = make_request('GET', f"{BASE_URL}/room_by_url", params={'room_url': test_url})
    room_by_url_result = "Success" if status == 200 and content.get('room_url') == test_url else "Fail"
    results.append(["GET /room_by_url", "URL: " + test_url, status, room_by_url_result])
    print(Fore.GREEN + "✅ Test Passed: GET /room_by_url" if status == 200 and content.get('room_url') == test_url else Fore.RED + "❌ Test Failed: GET /room_by_url")

    # Test Update Room
    updated_data = {
        "name": "Advanced Web Security Updated",
        "description": "An intermediate room with updated content on web security vulnerabilities.",
        "room_url": "https://tryhackme.com/room/advancedwebsecurityupdated",
        "tags": ["intermediate", "web_security", "update"],
        "tasks": [
            {
                "title": "Task 1 Updated",
                "description": "Updated description for SQL Injection.",
                "questions": [
                    {"number": 1, "question": "How can you detect SQL Injection?", "solution": "Using error-based or union-based SQL injection techniques."},
                    {"number": 2, "question": "What is the payload used?", "solution": "' OR '1'='1'"}
                ]
            },
            {
                "title": "Task 2 Updated",
                "description": "Updated description for XSS Attack.",
                "questions": [
                    {"number": 1, "question": "What type of XSS attack is demonstrated?", "solution": "Stored XSS."},
                    {"number": 2, "question": "What payload was used?", "solution": "<script>alert('XSS')</script>"}
                ]
            }
        ],
        "writeups": [{"title": "Updated Writeup", "url": "https://example.com/updated_writeup"}],
        "videos": [{"title": "Updated Video", "url": "https://example.com/updated_video"}]
    }
    print("Testing PUT /room/{name}...")
    status, content = make_request('PUT', f"{BASE_URL}/room/advancedwebsecurity", auth=(CORRECT_USERNAME, CORRECT_PASSWORD), data=updated_data)
    update_result = "Success" if status == 200 else "Fail"
    results.append(["PUT /room/{name}", "Update Room", status, update_result])
    print(Fore.GREEN + "✅ Test Passed: PUT /room/advancedwebsecurity" if status == 200 else Fore.RED + f"❌ Test Failed: PUT /room/advancedwebsecurity - {content}")

    # Test Delete Room
    print("Testing DELETE /room/{name}...")
    status, _ = make_request('DELETE', f"{BASE_URL}/room/advancedwebsecurity", auth=(CORRECT_USERNAME, CORRECT_PASSWORD))
    delete_result = "Success" if status == 200 else "Fail"
    results.append(["DELETE /room/{name}", "Delete Room", status, delete_result])
    print(Fore.GREEN + "✅ Test Passed: DELETE /room/advancedwebsecurity" if status == 200 else Fore.RED + "❌ Test Failed: DELETE /room/advancedwebsecurity")

    # Rate Limit Test - Send multiple requests quickly
    print("Testing Rate Limit...")
    for _ in range(7):  
        status, _ = make_request('GET', f"{BASE_URL}/rooms")
    rate_limit_status, _ = make_request('GET', f"{BASE_URL}/rooms")
    rate_limit_result = "Success" if rate_limit_status == 429 else "Fail"
    results.append(["GET /rooms Rate Limit", "None", rate_limit_status, rate_limit_result])
    print(Fore.GREEN + "✅ Test Passed: GET /rooms Rate Limit" if rate_limit_status == 429 else Fore.RED + f"❌ Test Failed: GET /rooms Rate Limit - Expected 429, got {rate_limit_status}")

    
    headers = ["Endpoint", "Details", "Status Code", "Result"]
    print("\n" + Fore.WHITE + tabulate(results, headers=headers, tablefmt="grid") + Style.RESET_ALL)
    for result in results:
        if result[-1] == "Success":
            print(Fore.GREEN + "✅ Test Passed: " + result[0] + Style.RESET_ALL)
        else:
            print(Fore.RED + "❌ Test Failed: " + result[0] + Style.RESET_ALL)

if __name__ == "__main__":
    print(Fore.YELLOW + "Running API Tests..." + Style.RESET_ALL)
    test_endpoints()
