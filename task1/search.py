from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi


client = MongoClient(
    "mongodb+srv://alozovoy9341011:FlVgddpTvpPDuSBp@cluster0.bcfdh.mongodb.net/",
    server_api=ServerApi('1')
)
db = client.book
collection = db['cats']


def get_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"Error: {e}")


def get_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"{name} no such cat.")
    except errors.PyMongoError as e:
        print(f"Error: {e}")


def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Age for {name} changed to {new_age}.")
        else:
            print(f"No {name} such cat.")
    except errors.PyMongoError as e:
        print(f"Name error: {e}")


def add_cat_feature(name, new_feature):
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"Feature {new_feature} was added to {name}.")
        else:
            print(f"No {name} such cat.")
    except errors.PyMongoError as e:
        print(f"Eeature error: {e}")


def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Cat {name} is deleted.")
        else:
            print(f"No {name} such cat.")
    except errors.PyMongoError as e:
        print(f"Delete error {e}")


def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"All cats deleted {result.deleted_count}.")
    except errors.PyMongoError as e:
        print(f"Delete error {e}")


if __name__ == "__main__":
    get_all_cats()
    get_cat_by_name("barsik")
    update_cat_age("barsik", 5)
    add_cat_feature("barsik", "eats dust")
    delete_cat_by_name("barsik")
    delete_all_cats()