import urllib.request
import os
import json
from time import sleep
import difflib
from mymail import send_mail

def request_website_content(url, encode):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            context = response.read()
            body = context.decode(encode, "ignore")
        return body
    except urllib.error.URLError as e:
        print(e.reason)

def get_website_diff(curr_website, prev_website):
    result = ""
    diff = difflib.Differ()
    output_diff = diff.compare(curr_website.split(), prev_website.split())
    for str_line in output_diff :
        # 引っかかりそうなところを入れる
        if 'content="?st=1' in str_line or 'value="' in str_line or "index.php" in str_line \
            or "shop.php" in str_line or "data:{stock_lst:stock_lst," in str_line \
            or '{"isTestserver":false,"isLcJimdoCom":false' in str_line \
            or 'class="maker_count">' in str_line:
            continue 
        if str_line.startswith(('+', '-')) :
            result += str_line + "\n"
    return result

def save_website(curr_website, name):
    with open(f"data/{name}.html", mode="w") as f:
        f.write(curr_website)

def load_website(name):
    filepath = f"data/{name}.html"
    
    if not os.path.exists(filepath):
        return ""

    with open(filepath, mode="r") as f:
        content = f.read()
    return content

def load_website_info():
    with open('url.json') as f:
        url_list = json.load(f)
    return url_list

def check_update(info):
    
    url = info["url"]
    name = info["name"]
    encode = info["encode"]
    
    print(f"try:{name}")
    content = request_website_content(url, encode)
    
    if content is None:
        print("error")
        return

    prev_content = load_website(name)
    diff = get_website_diff(content, prev_content)
    if diff != "":
        print("update")
        #print(diff)
        send_mail(name, diff, encode)
        save_website(prev_content, name+"_old")
        save_website(content, name)
    else:
        print("same")

def main():
    while True:
        url_list = load_website_info()
        for info in url_list:
            check_update(info)
        sleep(60*60)
    
if __name__ == "__main__":
    main()