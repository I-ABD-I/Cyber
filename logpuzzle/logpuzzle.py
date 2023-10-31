#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import os
import pathlib
import re
import sys
import urllib.request
import urllib.error

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


# dest_dir needs to be a valid path
def download_image(url, dest_dir):
    # download image from url and save it to dest_dir
    try:
        urllib.request.urlretrieve(url, dest_dir)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(e)


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # extract hostname from filename
    hostname = re.search(r"_(\S+)\.\S*", filename)
    hostname = hostname.group(1) if hostname else ""
    if not hostname:
        print("No hostname found in file name")
        return []

    # get list of paths from file
    paths: list[str] = []
    try:
        with open(filename, "r") as file:
            for line in file:
                # find path in line (searches for a http GET and a .jpg file)
                path = re.search(r"GET (\S*?\.jpg)", line)
                if (
                    path
                    and (to_add := f"http://{hostname}{path.group(1)}") not in paths
                ):
                    paths.append(to_add)
        return sorted(paths, key=lambda s: s.split("-")[-1])

    except FileNotFoundError:
        print(f"File {filename} not found")
        return []

    except Exception as e:
        print(e)
        return []
    # return paths


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # donwload images to dest_dir
    pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
    for i, url in enumerate(img_urls):
        download_image(url, f"{dest_dir}/img{i}.jpg")


def create_html(dest_dir):
    # sort function for html file
    def sort_key(s: str):
        s = "".join([c for c in s if c.isdigit()])
        return int(s) if s else 0

    # create html file with images from dest_dir
    html = "<html><body>"
    for file in sorted(os.listdir(dest_dir), key=sort_key):
        if str(file).endswith(".jpg"):
            html += f'<img src="{file}">'
    html += "</body></html>"
    return html


def main():
    args = sys.argv[1:]

    if not args:
        print("usage: [--todir dir] logfile ")
        sys.exit(1)

    todir = ""
    if args[0] == "--todir":
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
        try:
            with open(
                f"{todir}/{args[-2].split('_')[0][args[-2].rfind('/'):]}_index.html",
                "w",
            ) as file:
                file.write(create_html(todir))
        except Exception as e:
            print(e)
    else:
        print("\n".join(img_urls))


if __name__ == "__main__":
    main()
