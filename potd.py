import requests
import time

def get_leetcode_daily_challenge():
    url = "https://leetcode.com/graphql/"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "",
        "baggage": "sentry-environment=production,sentry-release=42c5231b,sentry-transaction=%2Fproblemset%2F%5B%5B...slug%5D%5D,sentry-public_key=2a051f9838e2450fbdd5a77eb62cc83c,sentry-trace_id=db36b9fff3594c4091f41d4cc57c69a4,sentry-sample_rate=0.03",
        "content-type": "application/json",
        "origin": "https://leetcode.com",
        "priority": "u=1, i",
        "random-uuid": "6d8eb486-0704-50fc-ee0a-72a772d1ba75",
        "referer": "https://leetcode.com/problemset/",
        "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sentry-trace": "db36b9fff3594c4091f41d4cc57c69a4-bc87f4ded7ea8744-0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "uuuserid": "1fef38dc3b70bcc9ab1a4f5dac6730ff",
        "x-csrftoken": "qOAA0aU6rUb2q2hkgLRYwaGc0nkVdbn58xjamhb7NvggQaNZjB3y6Am9FltH1McT"
    }

    cookies = {
        "INGRESSCOOKIE": "92b3c654f5c1e32481309253f54bb2d5|8e0876c7c1464cc0ac96bc2edceabd27",
        "csrftoken": "qOAA0aU6rUb2q2hkgLRYwaGc0nkVdbn58xjamhb7NvggQaNZjB3y6Am9FltH1McT",
        "ip_check": '(false, "103.186.68.3")',
        "_gid": "GA1.2.2049718146.1750168133",
        "_gat": "1",
        "_ga": "GA1.1.603530957.1750168133",
        "_ga_CDRWKZTDEX": "GS2.1.s1750168134$o1$g0$t1750168165$j29$l0$h0"
    }

    payload = {
        "query": """
        query dailyCodingQuestionRecords($year: Int!, $month: Int!) {
        dailyCodingChallengeV2(year: $year, month: $month) {
            challenges {
            date
            userStatus
            link
            question {
                questionFrontendId
                title
                titleSlug
            }
            }
            weeklyChallenges {
            date
            userStatus
            link
            question {
                questionFrontendId
                title
                titleSlug
                isPaidOnly
            }
            }
        }
        }
        """,
        "variables": {
            "year": time.localtime().tm_year,
            "month": time.localtime().tm_mon
        },
        "operationName": "dailyCodingQuestionRecords"
    }
    try:
        response = requests.post(url, headers=headers, cookies=cookies, json=payload).json()
        return "https://leetcode.com"+response['data']['dailyCodingChallengeV2']['challenges'][-1]['link']
    except Exception as e:
        print(f"Error fetching LeetCode daily challenge: {e}")
        return None

def get_gfg_daily_challenge():
    url = "https://practiceapi.geeksforgeeks.org/api/vr/problems-of-day/problem/today/"
    try:
        response = requests.get(url)
        data = response.json()
        return data['problem_url']
    except Exception as e:
        print(f"Error fetching GFG daily challenge: {e}")
        return None

if __name__=='__main__':
    print(get_leetcode_daily_challenge())
    print(get_gfg_daily_challenge())
    
