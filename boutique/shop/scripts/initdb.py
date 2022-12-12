import csv
from shop.models import Item, Category, User

FNAME = "seeddata/items.csv"

def run():
    print(f'Reading file: {FNAME}')
    with open(FNAME) as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f'Processsing: {row}')
            user = User.objects.get(username=row["User"])
            title = row["Title"]
            description = row["Description"]
            price = row["Price"]
            categories = row["Categories"]
            image = row["Image"]

            if categories == 'Blue Cheese':
                c, _ = Category.objects.get_or_create(name=categories, image='media/images/Blue_Cheese.jpg')
            if categories == 'Alpine':
                c, _ = Category.objects.get_or_create(name=categories, image='media/images/Alpine.jpg')
            if categories == 'Hard Cheese':
                c, _ = Category.objects.get_or_create(name=categories, image='media/images/Hard_Cheese.jpg')
            if categories == 'Washed Rinds':
                c, _ = Category.objects.get_or_create(name=categories, image='media/images/Washed_Rinds.jpg')
            if categories == 'Bloomy Rinds':
                c, _ = Category.objects.get_or_create(name=categories, image='media/images/Bloomy_Rinds.jpg')


            item, _ = Item.objects.get_or_create(user=user, title=title, description=description, price=price, image=image)

            item.categories.add(c)