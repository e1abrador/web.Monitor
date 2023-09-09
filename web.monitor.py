import shelve
import subprocess
import argparse
import time
from datetime import datetime
import configparser

DB_PATH = 'website_monitor.db'

config = configparser.ConfigParser()
config.read('web-monitor.ini')

def add_url(url):
    with shelve.open(DB_PATH, writeback=True) as db:
        if url not in db:
            db[url] = []

def add_urls_from_file(filename):
    with open(filename, 'r') as f:
        for url in f:
            add_url(url.strip())

def check_websites(roots=[]):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    db = shelve.open(DB_PATH, writeback=True)

    for url in db:
        if roots and not any(root in url for root in roots):
            continue

        httpx_binary = config.get('Binary paths', 'httpx')

        cmd = f'echo {url} | {httpx_binary} -silent -sc -title -cl -nc'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.strip()

        print(f"DEBUG: Result for {url}: {result}")

        if not result:
            continue

        parts = result.split()
        http_code = int(parts[1][1:-1])
        content_length = int(parts[2][1:-1])
        title = " ".join(parts[3:])[1:-1]

        stored_values = db[url]

        if not stored_values:
            stored_values.append({
                'http_code': http_code,
                'content_length': content_length,
                'title': title,
                'timestamp': current_time
            })
        else:
            if isinstance(stored_values, dict):
                stored_values = [stored_values]

            last_values = stored_values[-1]
            if (last_values['http_code'] != http_code or
                last_values['content_length'] != content_length or
                last_values['title'] != title):

                print(f"NOTIFICATION: Change detected for {url}. New values: {url} [{http_code}] [{content_length}] [{title}]")

                notify_binary = config.get('Binary paths', 'notify')
                notify_api = config.get('Apis', 'notify_api')

                cmd = f'echo "NOTIFICATION: Change detected for {url}. New values: {url} [{http_code}] [{content_length}] [{title}]" | {notify_binary} -silent -pc {notify_api}'
                subprocess.run(cmd, shell=True)
                stored_values.append({
                    'http_code': http_code,
                    'content_length': content_length,
                    'title': title,
                    'timestamp': current_time
                })

    db.close()

def show_changes_for_domain(domain):
    with shelve.open(DB_PATH) as db:
        changes = {url: data for url, data in db.items() if domain in url}
        if not changes:
            print(f"No changes recorded for {domain}.")
            return

        grouped_changes = {}
        for url, data_list in changes.items():
            key = url.split("http://")[1]
            if key not in grouped_changes:
                grouped_changes[key] = []
            grouped_changes[key].extend(data_list)

        for key, data_list in grouped_changes.items():
            print(key)
            for data in data_list:
                print(f"[{data['timestamp']}] http://{key} [{data['http_code']}] [{data['content_length']}] [{data['title']}]")
            print()

def show_changes_for_url(url):
    """Muestra los cambios de un URL específico."""
    with shelve.open(DB_PATH) as db:
        if url not in db:
            print(f"No changes recorded for {url}.")
            return

        print(url.split("http://")[1])
        for data in db[url]:
            print(f"[{data['timestamp']}] {url} [{data['http_code']}] [{data['content_length']}] [{data['title']}]")
        print()

def main():
    # Banner
    print("""
               _     __  __             _ _
              | |   |  \/  |           (_) |
 __      _____| |__ | \  / | ___  _ __  _| |_ ___  _ __
 \ \ /\ / / _ \ '_ \| |\/| |/ _ \| '_ \| | __/ _ \| '__|
  \ V  V /  __/ |_) | |  | | (_) | | | | | || (_) | |
   \_/\_/ \___|_.__/|_|  |_|\___/|_| |_|_|\__\___/|_|

                        github.com/e1abrador/web.Monitor
    """)

    parser = argparse.ArgumentParser(description="Monitor websites for changes.")
    parser.add_argument('--add', help='Add a URL to monitor.')
    parser.add_argument('--add-urls', help='Add URLs from a file to monitor.')
    parser.add_argument('--check', action='store_true', help='Check all the websites for changes.')
    parser.add_argument('-D', '--domain', help='Check websites for a specific root domain.')
    parser.add_argument('-df', '--domain-file', help='Check websites for root domains specified in a file.')
    parser.add_argument('--show-changes', action='store_true', help='Show changes for the specified domain or URL.')
    parser.add_argument('-H', '--hours', type=float, help='Repeat the website check every X hours.')
    parser.add_argument('-url', '--url', help='Show changes for a specific URL.')

    args = parser.parse_args()

    if args.add:
        add_url(args.add)

    if args.add_urls:
        add_urls_from_file(args.add_urls)

    if args.check:
        if args.hours:
            while True:
                if args.domain:
                    check_websites(roots=[args.domain])
                elif args.domain_file:
                    with open(args.domain_file, 'r') as f:
                        roots = [line.strip() for line in f]
                    check_websites(roots=roots)
                else:
                    check_websites()

                print(f"Waiting for {args.hours} hour(s) before the next check...")
                time.sleep(args.hours * 3600)
        else:
            if args.domain:
                check_websites(roots=[args.domain])
            elif args.domain_file:
                with open(args.domain_file, 'r') as f:
                    roots = [line.strip() for line in f]
                check_websites(roots=roots)
            else:
                check_websites()

    if args.domain and args.show_changes:
        show_changes_for_domain(args.domain)

    if args.url:
        show_changes_for_url(args.url)

if __name__ == "__main__":
    main()
