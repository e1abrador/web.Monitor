<h1 align="center">
 web.Monitor
<br>
</h1>

<pre align="center">
<b>
   Fast & user-friendly web change tracking tool.
</b>
</pre>

![image](https://github.com/e1abrador/web.Monitor/assets/74373745/dd13f17f-3364-4d25-92fa-6f1924b0acdf)

## Why?

**Continuous Monitoring:** The script can automatically check web pages at regular intervals to detect any changes.

**Flexible Setup:** You can add individual URLs or load a list of URLs from a file.

**Persistent Storage:** It uses sqlite module to store the web data in a database file, allowing persistence across runs.

**Detailed Logging:** It doesn't just check if the page is up, but also logs the HTTP code, content length, and the page title.

**Notifications:** Upon detecting a change, the script not only prints it on the console but can also send out a notification.

**Change Visualization:** Provides functionality to view all recorded changes for a specific domain or URL, aiding in historical tracking.

**Domain Filtering:** If you're only interested in checking URLs of a specific domain, the script allows you to filter and only check those domains.

**Automation:** With the hour-based repetition option, the script can operate in a loop, checking web pages every set number of hours.

**Customization and Extension:** Being an open-source script, you can tailor it to your needs or add more functionalities.

## Features
- **Fast**
- **Easy to use**
- **Easy to install**
- **Continuously save new changes in the local database (with the possibility of dumping them all)**
- **Telegram/slack/discord notifications**

## Help Menu
**web.Monitor** flags:

````console
options:
  -h, --help            show this help message and exit
  --add ADD             Add a URL to monitor.
  --add-urls ADD_URLS   Add URLs from a file to monitor.
  --check               Check all the websites for changes.
  -D DOMAIN, --domain DOMAIN
                        Check websites for a specific root domain.
  -df DOMAIN_FILE, --domain-file DOMAIN_FILE
                        Check websites for root domains specified in a file.
  --show-changes        Show changes for the specified domain or URL.
  -H HOURS, --hours HOURS
                        Repeat the website check every X hours.
  -url URL, --url URL   Show changes for a specific URL.
````

## Previous needed configurations

  You need to write the configuration (api) path files into **config.ini** file.
  
- [Httpx](https://github.com/projectdiscovery/httpx) binary.
- [Notify](https://github.com/owasp-amass/amass/blob/master/examples/config.ini) binary.
- Notify api configuration file.

## Work plan

``IMPORTANT``: I had to change from shelve library to sqlite3 because I had some problems with my VPS. It was generating different database files (I don't really know why, on my local machine was working correctly).

First of all, is needed to add a URL (or URLs) to the database:

````console
python3 web.monitor.py --add-urls urls.txt
python3 web.monitor.py --add http://example.com:81
````

Now, you can start scanning. It's important to note that the first result will be saved on the database but you won't receive a notification, the script will start sending notifications after the first scan.

Once all the URLs are on the database, you can start scanning with the following command:

````console
python3 web.monitor.py -df roots.txt --check -H 1
python3 web.monitor.py -D example.com --check -H 1
````

The ``-df`` flag is used to scan all URLs from a root domain, for example, if the URL ``admin.example.com`` and ``admin.example2.com`` are on the database and the ``roots.txt`` file has only ``*.example.com`` will be scanned. The ``-D`` flag scans only ``*.example.com`` URLs. The ``-H`` flag is used to specify the domain that each 1 hour will be performed a scan, of course, you can customize that, in any case, I recommend scanning each 12 or 24 hours.

If you want to dump all URLs from a given domain you can use:

````console
➜  python3 web.monitor.py -D example.com --show-changes

               _     __  __             _ _
              | |   |  \/  |           (_) |
 __      _____| |__ | \  / | ___  _ __  _| |_ ___  _ __
 \ \ /\ / / _ \ '_ \| |\/| |/ _ \| '_ \| | __/ _ \| '__|
  \ V  V /  __/ |_) | |  | | (_) | | | | | || (_) | |
   \_/\_/ \___|_.__/|_|  |_|\___/|_| |_|_|\__\___/|_|

                        github.com/e1abrador/web.Monitor

example.com:81/
[2023-09-10 00:58:16.694612] http://example.com:81/ [200] [3463] [Test 1]
[2023-09-10 00:58:25.382700] http://example.com:81/ [200] [39386] [Test 1]

example.com:82/
[2023-09-10 00:56:42.354195] http://example.com:82/ [200] [3463] [Test 2]
[2023-09-10 00:57:27.545999] http://example.com:82/ [200] [39386] [Test 2]
[2023-09-10 00:57:38.478968] http://example.com:82/ [200] [2666] [Test 2]
````

You can check 1 single URL with ``--url`` flag too:

````console
python3 web.monitor.py --url http://example.com:81 --show-changes

               _     __  __             _ _
              | |   |  \/  |           (_) |
 __      _____| |__ | \  / | ___  _ __  _| |_ ___  _ __
 \ \ /\ / / _ \ '_ \| |\/| |/ _ \| '_ \| | __/ _ \| '__|
  \ V  V /  __/ |_) | |  | | (_) | | | | | || (_) | |
   \_/\_/ \___|_.__/|_|  |_|\___/|_| |_|_|\__\___/|_|

                        github.com/e1abrador/web.Monitor

[2023-09-10 21:51:46.626917] http://example.com:81 [200] [21535] [Test 1]
[2023-09-10 21:51:53.748105] http://example.com:81 [200] [2666] [Test 2]
[2023-09-10 21:58:25.827493] http://example.com:81 [200] [35127] [Test 3]
````



Note that when using the above command, every URL that contains the domain used in ``-D`` flag will be used, in this example the script will show *.example.com.

  ## Thanks
  
  Thanks to:
  
  - Projectdiscovery for creating [httpx](https://github.com/projectdiscovery/httpx) and [notify](https://github.com/projectdiscovery/notify)!.

If you have any idea of some new functionality open a PR at https://github.com/e1abrador/web.Monitor/pulls.

Good luck and good hunting!
If you really love the tool (or any others), or they helped you find an awesome bounty, consider [BUYING ME A COFFEE!](https://www.buymeacoffee.com/e1abrador) ☕ (I could use the caffeine!)

⚪ e1abrador

Twitter: https://twitter.com/C4yyyy

<a href='https://www.buymeacoffee.com/e1abrador' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi2.png?v=3' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>
