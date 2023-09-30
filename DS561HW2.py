from google.cloud import storage
import re
import statistics
from concurrent.futures import ThreadPoolExecutor
#import networkx as nx
#import matplotlib.pyplot as plt

def compute_statistics(incoming_links):
    lengths = [len(sublist) for sublist in incoming_links]

    average = statistics.mean(lengths)
    median = statistics.median(lengths)
    file_max = max(lengths)
    file_min = min(lengths)
    quintiles = statistics.quantiles(lengths, n=5)

    print(average, median, file_max, file_min, quintiles)

def compute_pagerank(incoming_links, outgoing_links, threshold=0.005):
    pageranks = [0.15 for _ in range(10000)]
    iterator = 0

    while (True and iterator<1000):
        sum_pageranks = sum(pageranks)
        total_change = 0

        for i in range(10000):
            change = 0
            for link in incoming_links[i]:
                change += 0.85 * (pageranks[link] / len(outgoing_links[link]))
            pageranks[i] += change
            total_change += change
        if total_change/sum_pageranks > threshold:
                break
        iterator+= 1
    
    return pageranks

links = re.compile(r'<a\s+HREF="([^"]+)"', re.IGNORECASE)
numbers = re.compile(r'(\d+)\.html')

bucket_name = "bhiraoka-hw2-bucket"
directory = "hw2-files/"

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)

blobs = bucket.list_blobs(prefix=directory)

incoming_links = [[] for _ in range(10000)]
outgoing_links = [[] for _ in range(10000)]

def process_blob(blob):
    file_name = blob.name[8:]
    file_index = int(numbers.search(file_name).group(1))
    info = blob.download_as_text()

    values = links.findall(info)

    for value in values:
        match = numbers.search(value)
        page_index = int(match.group(1))

        incoming_links[page_index].append(file_index)
        outgoing_links[file_index].append(value)

print("running")
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = []
    iterator = 0
    for blob in blobs:
        iterator += 1
        futures.append(executor.submit(process_blob, blob=blob))

        if iterator % 1000 == 0:
            print("processed 1000")

print("done")
# print(incoming_links)
compute_statistics(incoming_links)
compute_statistics(outgoing_links)
print(sorted(compute_pagerank(incoming_links, outgoing_links))[0:5])
