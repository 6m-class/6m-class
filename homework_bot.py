import requests, json, base64, os, sys
from datetime import datetime, timedelta

LOGIN = os.environ.get('MESH_LOGIN', '')
PASSWORD = os.environ.get('MESH_PASSWORD', '')
TOKEN = os.environ.get('GH_TOKEN', '')
REPO = '6m-class/6m-class'
BRANCH = 'main'

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
})

def auth():
    print('🔐 Авторизация...')
    r = s.post('https://authedu.mosreg.ru/v2/auth/loginByLoginPassword',
        json={'login': LOGIN, 'password': PASSWORD}, timeout=30, allow_redirects=True)
    if r.status_code == 200:
        print('✅ OK')
        return True
    print(f'❌ {r.status_code}')
    return False

def get_homework():
    today = datetime.now()
    end = today + timedelta(days=14)
    result = []
    seen = set()

    # Получаем профиль
    person_id = ''
    try:
        r = s.get('https://school.mosreg.ru/api/persondata/v1/profiles', timeout=30)
        if r.ok:
            profiles = r.json()
            if isinstance(profiles, list) and profiles:
                person_id = str(profiles[0].get('id', ''))
    except: pass

    if not person_id:
        try:
            r = s.get('https://school.mosreg.ru/api/users/me', timeout=30)
            if r.ok:
                d = r.json()
                children = d.get('children', [])
                if children:
                    person_id = str(children[0].get('id', ''))
                elif d.get('id'):
                    person_id = str(d['id'])
        except: pass

    if not person_id:
        print('❌ Не нашли ID ученика')
        return []

    print(f'👤 ID: {person_id}')

    # Пробуем разные эндпоинты
    urls = [
        ('https://school.mosreg.ru/api/calendar/v2/diary', {
            'personId': person_id,
            'from': today.strftime('%Y-%m-%d'),
            'to': end.strftime('%Y-%m-%d'),
        }),
        ('https://api.school.mosreg.ru/v1/diary', {
            'person': person_id,
            'from': today.strftime('%Y-%m-%d'),
            'to': end.strftime('%Y-%m-%d'),
        }),
        ('https://school.mosreg.ru/api/homework/v1/homeworks', {
            'personId': person_id,
            'from': today.strftime('%Y-%m-%d'),
            'to': end.strftime('%Y-%m-%d'),
        }),
    ]

    for url, params in urls:
        print(f'📍 {url}')
        try:
            r = s.get(url, params=params, timeout=30)
            if not r.ok:
                print(f'   → {r.status_code}')
                continue
            data = r.json()
            items = data if isinstance(data, list) else (
                data.get('days', data.get('items', data.get('data', [])))
            )

            for item in items:
                if not isinstance(item, dict): continue
                lessons = item.get('lessons', item.get('items', []))
                day_date = item.get('date', item.get('day', ''))

                # Если это уже само ДЗ
                if 'subjectName' in item or 'subject_name' in item:
                    lessons = [item]

                for lesson in lessons:
                    if not isinstance(lesson, dict): continue
                    subject = lesson.get('subjectName', lesson.get('subject_name', lesson.get('subject', '')))
                    hw = lesson.get('homework', lesson.get('homeworkEntry', lesson.get('description', '')))
                    text = ''
                    due = ''

                    if isinstance(hw, dict):
                        text = hw.get('description', hw.get('text', ''))
                        due = hw.get('dueDate', hw.get('date', ''))
                    elif isinstance(hw, str):
                        text = hw
                    elif not hw:
                        text = lesson.get('description', lesson.get('text', ''))

                    if not subject and not text: continue

                    key = subject + text[:50]
                    if key in seen: continue
                    seen.add(key)

                    if due and 'T' in str(due): due = str(due).split('T')[0]
                    if due and '-' in str(due):
                        try:
                            due = datetime.strptime(due, '%Y-%m-%d').strftime('%d.%m.%Y')
                        except: pass

                    result.append({
                        'subject': subject or 'Предмет',
                        'text': text.strip() if text else '',
                        'dueDate': due or '',
                        'addedDate': today.strftime('%d.%m.%Y'),
                        'author': 'Бот МЭШ',
                        'attachments': []
                    })

            if result: break

        except Exception as e:
            print(f'   → {e}')

    # Дедупликация
    unique = []
    ukeys = set()
    for h in result:
        k = h['subject'] + h['text'][:50] + h['dueDate']
        if k not in ukeys:
            ukeys.add(k)
            unique.append(h)

    print(f'📚 Найдено: {len(unique)}')
    return unique

def push(homework):
    print('📤 Запись в GitHub...')
    url = f'https://api.github.com/repos/{REPO}/contents/data.json'
    headers = {'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/vnd.github+json'}

    r = requests.get(f'{url}?ref={BRANCH}&t={int(datetime.now().timestamp())}', headers=headers)
    if not r.ok:
        print(f'❌ data.json: {r.status_code}')
        return
    file = r.json()
    sha = file['sha']
    data = json.loads(base64.b64decode(file['content']).decode('utf-8'))

    # Не перезаписываем ДЗ от админа
    admin_hw = [h for h in data.get('homework', []) if h.get('author') != 'Бот МЭШ']
    data['homework'] = homework + admin_hw

    new = base64.b64encode(json.dumps(data, indent=2, ensure_ascii=False).encode()).decode()

    r2 = requests.put(url, headers={**headers, 'Content-Type': 'application/json'}, json={
        'message': f'Бот ДЗ: {len(homework)} заданий ({datetime.now().strftime("%d.%m %H:%M")})',
        'content': new, 'sha': sha, 'branch': BRANCH
    })

    if r2.ok:
        print(f'✅ Готово: {len(homework)} от бота + {len(admin_hw)} от админа')
    else:
        print(f'⚠ Конфликт, повтор...')
        r3 = requests.get(f'{url}?ref={BRANCH}&t={int(datetime.now().timestamp())}', headers=headers)
        if r3.ok:
            sha2 = r3.json()['sha']
            data2 = json.loads(base64.b64decode(r3.json()['content']).decode())
            data2['homework'] = homework + admin_hw
            new2 = base64.b64encode(json.dumps(data2, indent=2, ensure_ascii=False).encode()).decode()
            r4 = requests.put(url, headers={**headers, 'Content-Type': 'application/json'}, json={
                'message': f'Бот ДЗ: {len(homework)} заданий',
                'content': new2, 'sha': sha2, 'branch': BRANCH
            })
            print('✅' if r4.ok else '❌')

print('🤖 Бот ДЗ МЭШ')
if not LOGIN or not PASSWORD or not TOKEN:
    print('❌ Секреты не заданы')
    sys.exit(1)
auth()
hw = get_homework()
push(hw)
