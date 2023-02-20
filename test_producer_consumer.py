import os
import threading
from producer_consumer import Producer, Consumer
import queue
import unittest


class TestLinkExtractor(unittest.TestCase):

    def test_queue_overflow(self):
        q = queue.Queue(maxsize=3)
        producer = Producer(['https://stackoverflow.com', 'https://www.youtube.com', 'https://www.facebook.com'], q)
        producer.produce()
        self.assertEqual(q.qsize(), 3, f"Queue should have size 3 but was {q.qsize()}")

    def test_invalid_urls(self):
        q = queue.Queue()
        producer = Producer(['https://www.invalid1.com', 'https://www.invalid2.com'], q)
        producer.produce()
        self.assertIsNone(q.get(), "Queue should not contain any data")

    def test_empty_queue(self):
        q = queue.Queue()
        producer = Producer([], q)
        consumer = Consumer(q, "test_empty.txt")
        producer.produce()
        consumer.consume()
        with open("test_empty.txt", "r") as f:
            self.assertEqual(f.read(), "", "Output file should be empty")

    def test_concurrency(self):
        urls = ['https://www.google.com', 'https://www.ebay.com']
        q = queue.Queue()
        producer = Producer(urls, q)
        consumer = Consumer(q, "test_concurrency.txt")

        pt = threading.Thread(target=producer.produce)
        ct = threading.Thread(target=consumer.consume)
        pt.start()
        ct.start()
        pt.join()
        ct.join()

        self.assertTrue(os.path.exists("test_concurrency.txt"))
        with open("test_concurrency.txt", "r") as f:
            lines = f.readlines()
            self.assertTrue(len(lines) > 0)


if __name__ == '__main__':
    unittest.main()
