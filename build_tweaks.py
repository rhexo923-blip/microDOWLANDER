import requests
import json

def fetch_ctt_tweaks():
    url = 'https://raw.githubusercontent.com/ChrisTitusTech/winutil/main/config/tweaks.json'
    print("Fetching CTT tweaks.json...")
    r = requests.get(url, timeout=10)
    data = json.loads(r.text, strict=False)
    
    tweaks_list = []
    for k, item in data.items():
        name = item.get('Content', k)
        desc = item.get('Description', '')
        cat = item.get('category', 'General')
        reg = item.get('registry', [])
        
        tweaks_list.append({
            "id": k,
            "name": name,
            "desc": desc,
            "category": cat,
            "registry": reg
        })

    print(f"Total tweaks parsed: {len(tweaks_list)}")
    with open('tweaks.json', 'w', encoding='utf-8') as f:
        json.dump(tweaks_list, f, ensure_ascii=False, indent=2)
    print("tweaks.json created successfully!")

if __name__ == '__main__':
    fetch_ctt_tweaks()
