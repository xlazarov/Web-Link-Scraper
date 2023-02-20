import queue
import threading
import requests
from bs4 import BeautifulSoup


def extract_markup(url):
    try:
        response = requests.get(url)
        markup = response.content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        markup = None
    return markup


def add_to_queue(queue, item):
    if queue.full():
        # Remove oldest item
        queue.get_nowait()
    queue.put(item)


class Producer:
    def __init__(self, urls, queue):
        self.urls = urls
        self.queue = queue
        self.threads = []

    def produce(self):
        for url in self.urls:
            t = threading.Thread(target=self.fetch_url, args=(url,))
            t.start()
            self.threads.append(t)

        for t in self.threads:
            t.join()

        # Signal the end of the queue
        add_to_queue(self.queue, None)

    def fetch_url(self, url):
        markup = extract_markup(url)
        if markup:
            add_to_queue(self.queue, markup)


def extract_links(markup):
    soup = BeautifulSoup(markup, 'html.parser')
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    return links


class Consumer:
    def __init__(self, queue, output_file):
        self.queue = queue
        self.output_file = output_file

    def consume(self):
        with open(self.output_file, 'w') as f:
            while True:
                markup = self.queue.get()
                if markup is None:
                    break
                url_links = extract_links(markup)
                for links in url_links:
                    f.write(f"{links}\n")


def main():
    urls = ['https://stackoverflow.com', 'https://www.google.com', 'https://www.ebay.com']

    q = queue.Queue(maxsize=2)
    producer = Producer(urls, q)
    consumer = Consumer(q, "output.txt")

    pt = threading.Thread(target=producer.produce)
    ct = threading.Thread(target=consumer.consume)
    pt.start()
    ct.start()
    pt.join()
    ct.join()


if __name__ == '__main__':
    main()
