from pymongo import MongoClient

from pprint import pprint

print('(a) Connect to MongoDB using pymongo')

client = MongoClient(
    host="127.0.0.1",
    port = 27017,
    username = "datascientest",
    password = "dst123"
)

db = client.sample

print('---------------------------------------------')

# (b) Display list of available databases
print('(b) Display list of available databases')
databases = client.list_database_names()
print("Databases:", databases)

print('---------------------------------------------')

# (c) Display list of collections in sample database
print('(c) Display list of collections in sample database')
collections = db.list_collection_names()
print("Collections:", collections)

print('---------------------------------------------')

# (d) Display one document from books collection
print('(d) Display one document from books collection')
pprint(db.books.find_one())

print('---------------------------------------------')

# (e) Display the number of documents in the books collection
print('(e) Display the number of documents in the books collection')
book_count = db.books.count_documents({})
print("Number of documents:", book_count)

print('---------------------------------------------')

# ==================
# Exploring the Database
# (a) Count books with more than 400 pages and published
print('Exploring the Database')
print('(a) Count books with more than 400 pages and published')
count_400_pages = db.books.count_documents({"pageCount": {"$gt": 400}})
print("Books with more than 400 pages:", count_400_pages)

print('---------------------------------------------')

count_400_pages_published = db.books.count_documents({"pageCount": {"$gt": 400}, "status": "PUBLISH"})
print("Published books with more than 400 pages:", count_400_pages_published)

print('---------------------------------------------')

# (b) Count books with the keyword "Android" in their description
print('(b) Count books with the keyword "Android" in their description')
android_books = db.books.count_documents({
    "$or": [
        {"shortDescription": {"$regex": "Android", "$options": "i"}},
        {"longDescription": {"$regex": "Android", "$options": "i"}}
    ]
})
print("Books mentioning Android:", android_books)

print('---------------------------------------------')

# (c) Display distinct categories using aggregation
print('(c) Display distinct categories using aggregation')

categories = db.books.aggregate([
    {"$group": {
        "_id": None,
        "categories_1": {"$addToSet": {"$arrayElemAt": ["$categories", 0]}},
        "categories_2": {"$addToSet": {"$arrayElemAt": ["$categories", 1]}}
    }}
])
for category in categories:
    pprint(category)
 
print('---------------------------------------------')   

# (d) Count books mentioning programming languages in the long description
print('(d) Count books mentioning programming languages in the long description')
language_books = db.books.count_documents({
    "$or": [
        {"longDescription": {"$regex": "Python", "$options": "i"}},
        {"longDescription": {"$regex": "Java", "$options": "i"}},
        {"longDescription": {"$regex": "C++", "$options": "i"}},
        {"longDescription": {"$regex": "Scala", "$options": "i"}}
    ]
})
print("Books mentioning programming languages:", language_books)

print('---------------------------------------------')

# (e) Statistical info on number of pages per category
print('(e) Statistical info on number of pages per category')
page_stats = db.books.aggregate([
    {"$unwind": "$categories"},
    {"$group": {
        "_id": "$categories",
        "maxPages": {"$max": "$pageCount"},
        "minPages": {"$min": "$pageCount"},
        "avgPages": {"$avg": "$pageCount"}
    }}
])
for stat in page_stats:
    pprint(stat)

print('---------------------------------------------')

# (f) Extract year, month, day from publishedDate and filter books published after 2009
print('(f) Extract year, month, day from publishedDate and filter books published after 2009')
books_after_2009 = db.books.aggregate([
    {"$project": {
        "year": {"$year": "$publishedDate"},
        "month": {"$month": "$publishedDate"},
        "day": {"$dayOfMonth": "$publishedDate"},
        "title": 1
    }},
    {"$match": {"year": {"$gt": 2009}}},
    {"$limit": 20}
])
for book in books_after_2009:
    pprint(book)

print('---------------------------------------------')

# (g) Create new author attributes and display first 20 books
print('(g) Create new author attributes and display first 20 books')
authors_list = db.books.aggregate([
    {"$project": {
        "author_1": {"$arrayElemAt": ["$authors", 0]},
        "author_2": {"$arrayElemAt": ["$authors", 1]},
        "author_3": {"$arrayElemAt": ["$authors", 2]},
        "title": 1
    }},
    {"$limit": 20}
])
for author in authors_list:
    pprint(author)

print('---------------------------------------------')

# (h) Count publications per first author and display top 10
print('(h) Count publications per first author and display top 10')
top_authors = db.books.aggregate([
    {"$group": {"_id": {"$arrayElemAt": ["$authors", 0]}, "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
])
for author in top_authors:
    pprint(author)

print('---------------------------------------------')
print('(i) Distribution of the Number of Authors')

print('Optional parts')
# (i) Distribution of the number of authors
author_distribution = db.books.aggregate([
    # Create a new field with the size of the authors array (number of authors)
    {"$project": {
        "numAuthors": {"$size": "$authors"}
    }},
    # Group by the number of authors and count the occurrences
    {"$group": {
        "_id": "$numAuthors",
        "count": {"$sum": 1}
    }},
    # Sort by the number of authors (optional, just for better readability)
    {"$sort": {"_id": 1}}
])

# Print the result
print("Distribution of the number of authors:")
for entry in author_distribution:
    pprint(entry)

print('---------------------------------------------')
# (j) Occurrence of each author according to its index in the "authors" attribute
author_occurrences = db.books.aggregate([
    # Unwind the authors array so each author is treated as a separate document
    {"$unwind": "$authors"},
    # Remove empty authors
    {"$project": {
        "author": "$authors"
    }},
    # Remove entries where the author is null or empty
    {"$match": {
        "author": {"$ne": ""}
    }},
    # Group by author and count the occurrences
    {"$group": {
        "_id": "$author",
        "count": {"$sum": 1}
    }},
    # Sort the authors by occurrence in descending order
    {"$sort": {"count": -1}},
    # Limit to top 20 authors by occurrence
    {"$limit": 20}
])

# Print the result
print("Top 20 authors by occurrence:")
for author in author_occurrences:
    pprint(author)


