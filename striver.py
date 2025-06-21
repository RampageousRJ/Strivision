import requests
import json
import os

common_headers = json.loads(open(os.path.join(os.getcwd(),"static","json","headers.json"), "r").read())

def get_login_token(email, password):
    url = "https://backend.takeuforward.org/api/auth/login"
    payload = {
        "loginCred":
        {
            "email": email,
            "password": password
        }
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("token"), response.json().get("username")
    else:
        raise Exception("Failed to get login token: " + response.text)
    
def get_entire_sheet(email, token):
    url = "https://backend.takeuforward.org/api/sheets/double/strivers_a2z_sheet"

    headers = common_headers

    cookies = {
        "_ga": "GA1.1.509925093.1738125927",
        "_ga_51P1R4XNJ0": "GS2.1.s1750086593$o12$g0$t1750086593$j60$l0$h0",
        "takeuforward": token
    }

    # Technically not standard, but possible: using data/body with GET
    payload = {
        "email": email
    }

    response = requests.get(url, headers=headers, cookies=cookies, json=payload).json()

    with open(os.path.join(os.getcwd(),"static","json","striver_sheet.json"), "w") as file:
        json.dump(response, file, indent=4)

def get_starred_questions(email, token):
    url = "https://backend.takeuforward.org/api/profile/get/revision"

    headers = common_headers

    cookies = {
        "_ga": "GA1.1.509925093.1738125927",
        "_ga_51P1R4XNJ0": "GS2.1.s1750086593$o12$g0$t1750086593$j60$l0$h0",
        "takeuforward": token
    }

    # Technically not standard, but possible: using data/body with GET
    payload = {
        "email": email
    }

    response = requests.post(url, headers=headers, cookies=cookies, json=payload).json()
    return response

def fetch_user_data(email, token):
    user_data = []
    data = json.loads(open(os.path.join(os.getcwd(),"static","json","striver_sheet.json"), "r").read())
    starred_questions = get_starred_questions(email ,token)['result']
    for item in data:
        for steps in item.get('sub_steps'):
            for topic in steps.get('topics'):
                if topic['id'] in starred_questions:
                    user_data.append({
                        'id' : topic['id'],
                        'title': topic['question_title'],
                        'striver_link': topic['post_link'],
                        'youtube_link': topic['yt_link'],
                        'leetcode_link': topic['lc_link'],
                        'striver_editorial_link': topic['editorial_link'],
                        'difficulty': topic['difficulty']
                    })
    return user_data

def get_user_stats(username, token):
    url = f"https://backend.takeuforward.org/api/profile/user/progress/{username}"
    headers = common_headers
    cookies = {
        "_ga": "GA1.1.509925093.1738125927",
        "_ga_51P1R4XNJ0": "GS2.1.s1750086593$o12$g0$t1750086593$j60$l0$h0",
        "takeuforward": token
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Failed to fetch user stats: " + response.text)
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")
    
def unstar_question(token, email, question_id):
    url = "https://backend.takeuforward.org/api/profile/update/revision"

    headers = common_headers

    cookies = {
        "_ga": "GA1.1.345481477.1750156769",
        "_ga_51P1R4XNJ0": "GS2.1.s1750485247$o10$g1$t1750485251$j56$l0$h0",
        "takeuforward": token,
        "undefined": '""'
    }

    payload = {
        "email": email,
        "q_id": question_id,
        "q_data": 0
    }

    try:
        response = requests.put(url, headers=headers, cookies=cookies, json=payload).json()
        return response['success']
    except Exception as e:
        print(f"Error unstarring question {question_id}: {e}")
        return False

if __name__ == "__main__":
    email = os.getenv('STRIVER_EMAIL')
    password = os.getenv('STRIVER_PASSWORD')
    try:
        token, username = get_login_token(email, password)
        # get_entire_sheet(email, token)
        unstar_question(token, email, 'implmnttri2prfixtr')
        # fetch_user_data(email,token)
        # get_user_stats(username, token)
    except Exception as e:
        print("Error:", e)