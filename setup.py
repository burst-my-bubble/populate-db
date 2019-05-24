from pymongo import MongoClient
client = MongoClient()
db = client["burstMyBubble"]

for source in open("data/sources.txt"):
  title, url, slug = source[:-1].split(", ")
  data = {"title":title, "url": url, "slug": slug}
  db.sources.update_one({"slug": slug}, {"$set": data}, upsert=True)

for category in open("data/categories.txt"):
  title, slug = category[:-1].split(", ")
  data = {"title":title, "slug": slug}
  db.categories.update_one({"slug": slug}, {"$set": data}, upsert=True)

for feed in open("data/feeds.txt"):
  feed = feed.strip()
  if feed == "" or feed[0] == "#":
    continue
  url, source_slug, category_slug = feed.split(", ")
  source_id = db.sources.find_one({"slug":source_slug})["_id"]
  category_id = db.categories.find_one({"slug":category_slug})["_id"]
  data = {"url":url, "source_id": source_id, "category_id": category_id}
  db.feeds.update_one({"url": url}, {"$set": data}, upsert=True)