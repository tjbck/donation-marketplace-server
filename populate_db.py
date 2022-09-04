
from app.internal.utils import get_password_hash

from app.models.listings import Listings
from app.models.users import Users

tester = Users.insert_auth_and_user(**{
    "id": '2',
    "email": "test@test.com",
    "password": get_password_hash("test"),
    "name": 'Tester',
    "mobile": '12341234',
    "address": 'Canary Wharf, London',
    "coords": [51.50314, -0.0239],
})

tester_2 = Users.insert_auth_and_user(**{
    "id": '1',
    "email": "admin@admin.com",
    "password": get_password_hash("1234"),
    "name": 'Jaeryang Baek',
    "mobile": '12341234',
    "address": 'Canary Wharf, London',
    "coords": [51.5032, -0.0239],
})

tester_3 = Users.insert_auth_and_user(**{
    "id": '3',
    "email": "test1@test.com",
    "password": get_password_hash("1234"),
    "name": 'John Doe',
    "mobile": '12341234',
    "address": 'Canary Wharf, London',
    "coords": [51.5032, -0.0239],
})


Listings.insert_item(**{
    "user": tester_2,
    "title": 'Electric Scooter',
    "content": '''Electric Scooter with seat and charger
                for age 7 to 10 yrs
                handle a bit loose need some fixing''',
    "filename": 'placeholders/scooter.jpeg'
})

Listings.insert_item(**{
    "user": tester,
    "title": '4 Doors',
    "content": '''4 panel doors for sale like new''',
    "filename": 'placeholders/door.jpeg'
})

Listings.insert_item(**{
    "user": tester_2,
    "title": 'Solid wood dining table with 4 chairs',
    "content": '''Solid wood dining table with 4 chairs , good condition , £40

Dimensions table 47.5 inches

Collection only Oldham OL1''',
    "filename": 'placeholders/table.jpeg'
})

Listings.insert_item(**{
    "user": tester_2,
    "title": 'Lovely cactus producing lots of pups',
    "content": '''Lovely cactus with lots of pups.

please check out my other plant listings as all proceeds go towards war orphan sponsorship. Happy to do a deal.''',
    "filename": 'placeholders/cactus.jpeg'
})


Listings.insert_item(**{
    "user": tester,
    "title": '13" Touchscreen Dell XPS 13 9250 w/ Portable Charger',
    "content": '''Like new condition. No scratches on computer. Comes with case, a portable charger made specifically for the computer, and the original wall charger. Specs are in the pictures. 128 GB SDD. Message me if you have any questions! Price is negotiable.''',
    "filename": 'placeholders/dell-laptop.jpeg'
})

Listings.insert_item(**{
    "user": tester_2,
    "title": 'PS4 Console and controllers, fire struck, 2 routers',
    "content": '''PS4 Console and 2 controllers -$150 (used-like new)
Netgear R7000 -$100 (like new)
Arris surfboard sbg6580 -$80 (used-like new)
Fire stick 4k- $30 (new-open box)
Xbox controller and charging dock - $50 (used)

If it's mentioned, the item is available. Please don't ask if they are available.''',
    "filename": 'placeholders/ps4.jpeg'
})


Listings.insert_item(**{
    "user": tester_3,
    "title": '3 pieces ceramic bathroom set',
    "content": '''brand new 3 pieces ceramic bathroom set still in original packaging smoke and pet free.''',
    "filename": 'placeholders/ceramic-set.jpeg'
})

Listings.insert_item(**{
    "user": tester_3,
    "title": 'Bed from Mothercare',
    "content": '''Used but in good condition''',
    "filename": 'placeholders/baby-bed.jpeg'
})

Listings.insert_item(**{
    "user": tester_3,
    "title": 'Girls bike',
    "content": '''Only used it few times.''',
    "filename": 'placeholders/girl-bike.jpeg'
})

Listings.insert_item(**{
    "user": tester_3,
    "title": 'Echo dot',
    "content": '''Collection Norris green
Never been used boxed us been opened tho. Everything inside is till in its wrapper
Can drop off for small fee if not to far or can post for extra''',
    "filename": 'placeholders/echo-dot.jpeg'
})


Listings.insert_item(**{
    "user": tester_3,
    "title": 'Nintendo DS Lite',
    "content": '''No stylus but you can get packs off Amazon for under a fiver comes with charger''',
    "filename": 'placeholders/nintendo-ds.jpeg'
})


Listings.insert_item(**{
    "user": tester_3,
    "title": 'Plant',
    "content": '''moving out soon, someone please take my plant''',
    "filename": 'placeholders/tree.jpeg'
})
