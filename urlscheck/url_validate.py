#!/usr/bin/python

import csv
import human_curl as hurl
import numpy as np


INPUT_FILE = "urls.txt"
HTTP_OK = 200
OUTPUT_FILE = "valid_urls.csv"
LINE_TERMINATOR = "\n"


def read_urls(urls, file_name):
    print("Reading URLs from %s ..." % file_name)
    with open(file_name, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.rstrip('\n')
            urls.append(line)


def validate_urls(url_result, current_urls):
    print("Validating URLs ...")
    for current_url in current_urls:
        validate_url(url_result, current_url)


def validate_url(url_result, url):
    print("Validating %s" % url)
    try:
        r = hurl.get(url)
        if r.status_code != HTTP_OK:
            valid_url = r.headers.get("location")
            url_result.append([r.status_code, url, valid_url])
    except hurl.CurlError as e:
        print("Error: %s" % e)


def write_csv_file(file_name, content):
    print("Writing to %s ..." % file_name)
    with open(file_name, 'wb') as f:
        writer = csv.writer(f, lineterminator=LINE_TERMINATOR, quoting=csv.QUOTE_ALL)
        writer.writerows(content)



urls = []
read_urls(urls, INPUT_FILE)
print("URLs count = %d" % len(urls))
# print("URLs = %s" % urls)

url_result = []
validate_urls(url_result, urls)
print("Validation results count = %d" % len(url_result))
# print("Validation results = %d, %s, %s" % (url_result[0][0], url_result[0][1], url_result[0][2]))

write_csv_file(OUTPUT_FILE, url_result)
