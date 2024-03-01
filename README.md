# Simple Producer/Consumer Web Link Extractor

This README provides an overview of a simple implementation of a producer/consumer system for extracting hyperlinks from web pages.

## Overview

### The Producer
1. The producer receives a list of URLs, which can be provided from a file, command line, etc.
2. It extracts the markup from each URL and places the output onto a queue.

### The Consumer
1. The consumer reads the queue until it is empty and the producer is no longer extracting markup.
2. It parses the HTML and extracts hyperlinks into a list. This list is output either to a file or the command line against each parsed URL.

## Implemented Features

1. **Concurrency**: The producer and consumer run concurrently.
2. **Error Handling**: Ensures isolation - one bad fetch or parse does not affect processing of others.
3. **Unit Tests**: Unit tests have been implemented.
4. **GitHub Repository**: The project is available on GitHub.

## Additional Features

1. **Concurrent URL Fetching**: URLs are fetched concurrently.
2. **Queue Management**: Oldest queue entries are trimmed if the queue size balloons.
3. **Comprehensive Testing**: Comprehensive test coverage is ensured.
4. **Other Considerations**: Various other considerations and enhancements have been implemented.
