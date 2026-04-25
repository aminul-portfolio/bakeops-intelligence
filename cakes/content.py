from decimal import Decimal

from .models import CakeCollection, Cake, CakeVariant


# ---------------------------
# 1) Collections
# ---------------------------
collections_data = [
    {"key": "birthday", "label": "Birthday Zone", "icon": "🎂", "sort_order": 10},
    {"key": "kids", "label": "Kids Collection", "icon": "🧸", "sort_order": 20},
    {"key": "chocolate", "label": "Chocolate Collection", "icon": "🍫", "sort_order": 30},
]


# ---------------------------
# 2) Cakes (+ variants)
#   image paths assume: MEDIA_ROOT / "cakes/..."
#   e.g. media/cakes/banana_cloud.jpg
# ---------------------------
cakes_data = [
    # -----------------------
    # ANNIVERSARY / LOVE
    # -----------------------
    {
        "name": "Blush Photo Celebration Cake",
        "slug": "blush-photo-celebration-cake",
        "occasion_type": "anniversary",   # 💞
        "category": "Photo Cake",
        "short": "Soft vanilla sponge with cream and your own photo printed on top.",
        "description": (
            "Soft vanilla layers with light whipped cream and a fully edible photo topper. "
            "Perfect for birthdays and anniversaries where you want your favourite photo "
            "to be the star."
        ),
        "image": "cakes/an01.jpg",
        "collections": ["birthday"],
        "variants": [
            {
                "label": '8" • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "29.90",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Strawberry Biscoff Heart Cake",
        "slug": "strawberry-biscoff-heart-cake",
        "occasion_type": "anniversary",
        "category": "Chocolate & Strawberry",
        "short": "Chocolate sponge with Biscoff cream and fresh strawberries.",
        "description": (
            "Decadent chocolate sponge filled with Biscoff cream and topped with "
            "fresh strawberries, biscuits and a soft heart silhouette. Ideal for "
            "anniversaries, proposals and romantic birthdays."
        ),
        "image": "cakes/an02.jpg",
        "collections": ["birthday", "chocolate"],
        "variants": [
            {
                "label": '8" • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "32.50",
                "is_default": True,
            },
        ],
    },

    # -----------------------
    # EVERYDAY / TEA CAKES
    # -----------------------
    {
        "name": "Carrot Walnut Glow Cake",
        "slug": "carrot-walnut-glow-cake",
        "occasion_type": "other",
        "category": "Carrot & Nut",
        "short": "Moist carrot sponge with cream cheese frosting and toasted walnuts.",
        "description": (
            "A moist carrot sponge with warm spices, layered with light cream cheese "
            "frosting and finished with toasted walnuts for crunch. A cosy everyday "
            "cake that still feels special on the table."
        ),
        "image": "cakes/carrot_walnut.jpg",
        "collections": [],
        "variants": [
            {
                "label": '6" • serves 6–8',
                "serves_min": 6,
                "serves_max": 8,
                "price": "19.90",
                "is_default": True,
            },
            {
                "label": '8" • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "27.90",
                "is_default": False,
            },
        ],
    },
    {
        "name": "Lemon Poppy Seed Sunshine Cake",
        "slug": "lemon-poppy-seed-sunshine-cake",
        "occasion_type": "other",
        "category": "Citrus",
        "short": "Zesty lemon sponge with crunchy poppy seeds and lemon cream.",
        "description": (
            "Bright lemon sponge soaked in light lemon syrup, speckled with poppy seeds "
            "and finished with a silky lemon cream topping. A fresh, uplifting cake "
            "for afternoon tea, office treats and light celebrations."
        ),
        "image": "cakes/lemon_poppy.jpg",
        "collections": [],
        "variants": [
            {
                "label": '7" • serves 8–10',
                "serves_min": 8,
                "serves_max": 10,
                "price": "19.50",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Matcha Citrus Loaf",
        "slug": "matcha-citrus-loaf",
        "occasion_type": "other",
        "category": "Loaf & Tea Cake",
        "short": "Soft matcha loaf with bright lemon–orange glaze.",
        "description": (
            "Japanese-inspired matcha loaf with a bright citrus glaze and slices of "
            "lemon and orange on top. Lightly sweet, aromatic and refreshing — ideal "
            "for calm weekend mornings or gifting to tea lovers."
        ),
        "image": "cakes/matcha_citrus.jpg",
        "collections": [],
        "variants": [
            {
                "label": "Loaf • serves 6–8",
                "serves_min": 6,
                "serves_max": 8,
                "price": "17.40",
                "is_default": True,
            },
        ],
    },

    # -----------------------
    # CHOCOLATE SHOWSTOPPERS
    # -----------------------
    {
        "name": "Dark Choco Berry Indulgence",
        "slug": "dark-choco-berry-indulgence",
        "occasion_type": "party",
        "category": "Chocolate",
        "short": "Rich dark chocolate layers with silky ganache and berries.",
        "description": (
            "Rich 70% cocoa sponge layered with lighter ganache and topped with "
            "fresh seasonal berries. A bold centrepiece for birthdays and parties "
            "when everyone wants a proper chocolate cake."
        ),
        "image": "cakes/dark_choco.jpg",
        "collections": ["birthday", "chocolate"],
        "variants": [
            {
                "label": '7" • serves 8–10',
                "serves_min": 8,
                "serves_max": 10,
                "price": "22.50",
                "is_default": True,
            },
            {
                "label": '9" • serves 14–16',
                "serves_min": 14,
                "serves_max": 16,
                "price": "32.50",
                "is_default": False,
            },
        ],
    },
    {
        "name": "Tall Chocolate Drip Birthday Cake",
        "slug": "tall-chocolate-drip-birthday-cake",
        "occasion_type": "birthday",
        "category": "Chocolate Drip",
        "short": "Tall chocolate sponge with ganache drip and loaded toppings.",
        "description": (
            "A tall, layered chocolate sponge finished with a glossy chocolate drip, "
            "swirls of buttercream and crunchy toppings. Designed as a modern "
            "birthday showstopper for chocolate lovers."
        ),
        "image": "cakes/bd04.jpg",
        "collections": ["birthday", "chocolate"],
        "variants": [
            {
                "label": '7" tall • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "34.90",
                "is_default": True,
            },
            {
                "label": '9" tall • serves 16–20',
                "serves_min": 16,
                "serves_max": 20,
                "price": "46.90",
                "is_default": False,
            },
        ],
    },
    {
        "name": "Chocolate Strawberry Party Sheet Cake",
        "slug": "chocolate-strawberry-party-sheet-cake",
        "occasion_type": "party",
        "category": "Chocolate Sheet",
        "short": "Large chocolate tray bake topped with cream and strawberries.",
        "description": (
            "A generous chocolate sponge baked in a large tray, topped with whipped "
            "cream, chocolate drizzle and fresh strawberries. Ideal for office "
            "celebrations, school parties and big family gatherings."
        ),
        "image": "cakes/pt02.jpg",
        "collections": ["birthday", "chocolate"],
        "variants": [
            {
                "label": "Party tray • serves 20–24",
                "serves_min": 20,
                "serves_max": 24,
                "price": "49.00",
                "is_default": True,
            },
        ],
    },

    # -----------------------
    # BANANA / SOFT FLAVOURS
    # -----------------------
    {
        "name": "Banana Cloud Layer Cake",
        "slug": "banana-cloud-layer-cake",
        "occasion_type": "birthday",
        "category": "Banana",
        "short": "Fluffy banana sponge with vanilla cream and banana slices.",
        "description": (
            "Ripe banana sponge layered with yogurt vanilla cream, finished with "
            "banana slices and soft piping. A light, comforting cake that kids "
            "love and adults always come back for a second slice."
        ),
        "image": "cakes/banana_cloud.jpg",
        "collections": ["kids", "birthday"],
        "variants": [
            {
                "label": '6" • serves 6–8',
                "serves_min": 6,
                "serves_max": 8,
                "price": "18.90",
                "is_default": True,
            },
            {
                "label": '8" • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "26.90",
                "is_default": False,
            },
        ],
    },

    # -----------------------
    # BIRTHDAY CLASSICS (bd01–bd05)
    # -----------------------
    {
        "name": "Pastel Sprinkle Birthday Cake",
        "slug": "pastel-sprinkle-birthday-cake",
        "occasion_type": "birthday",
        "category": "Birthday Classic",
        "short": "Vanilla sponge with pastel buttercream and rainbow sprinkles.",
        "description": (
            "A classic vanilla birthday cake covered in smooth pastel buttercream "
            "and finished with rainbow sprinkles. Simple, pretty and perfect for "
            "all ages and themes."
        ),
        "image": "cakes/bd01.jpg",
        "collections": ["birthday"],
        "variants": [
            {
                "label": '6" • serves 6–8',
                "serves_min": 6,
                "serves_max": 8,
                "price": "21.90",
                "is_default": True,
            },
            {
                "label": '8" • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "29.90",
                "is_default": False,
            },
        ],
    },
    {
        "name": "Pink Swirl Celebration Cake",
        "slug": "pink-swirl-celebration-cake",
        "occasion_type": "birthday",
        "category": "Birthday Classic",
        "short": "Soft vanilla sponge with pink swirls and piped rosettes.",
        "description": (
            "Light vanilla layers coated in pink buttercream swirls and rosettes. "
            "A sweet, feminine design that works beautifully for milestone birthdays "
            "and baby showers."
        ),
        "image": "cakes/bd02.jpg",
        "collections": ["birthday"],
        "variants": [
            {
                "label": '6" • serves 6–8',
                "serves_min": 6,
                "serves_max": 8,
                "price": "22.90",
                "is_default": True,
            },
            {
                "label": '8" • serves 10–12',
                "serves_min": 10,
                "serves_max": 12,
                "price": "31.90",
                "is_default": False,
            },
        ],
    },
    {
        "name": "Ombre Rosette Birthday Cake",
        "slug": "ombre-rosette-birthday-cake",
        "occasion_type": "birthday",
        "category": "Rosette Buttercream",
        "short": "Buttercream rosettes fading from pale to deep pink.",
        "description": (
            "A layered vanilla sponge decorated with full buttercream rosettes "
            "in an ombre gradient. Perfect when you want something elegant but still "
            "playful for the birthday table."
        ),
        "image": "cakes/bd03.jpg",
        "collections": ["birthday"],
        "variants": [
            {
                "label": '7" • serves 8–10',
                "serves_min": 8,
                "serves_max": 10,
                "price": "27.90",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Confetti Sprinkle Celebration Cake",
        "slug": "confetti-sprinkle-celebration-cake",
        "occasion_type": "birthday",
        "category": "Confetti",
        "short": "Funfetti sponge with colourful sprinkles inside and out.",
        "description": (
            "Soft vanilla funfetti sponge with sprinkles baked inside and scattered "
            "over the top. A bright, photogenic cake for parties, office birthdays "
            "and kids’ celebrations."
        ),
        "image": "cakes/bd05.jpg",
        "collections": ["birthday"],
        "variants": [
            {
                "label": '7" • serves 8–10',
                "serves_min": 8,
                "serves_max": 10,
                "price": "25.90",
                "is_default": True,
            },
        ],
    },

    # -----------------------
    # KIDS COLLECTION (kid01–kid05)
    # -----------------------
    {
        "name": "Unicorn Rainbow Kids Cake",
        "slug": "unicorn-rainbow-kids-cake",
        "occasion_type": "birthday",
        "category": "Kids Theme",
        "short": "Pastel rainbow kids’ cake with cute unicorn-style piping.",
        "description": (
            "A colourful kids’ cake with pastel rainbow piping and playful details, "
            "inspired by unicorn and rainbow party themes. Designed to sit right in "
            "the middle of the birthday table."
        ),
        "image": "cakes/kid01.jpg",
        "collections": ["kids", "birthday"],
        "variants": [
            {
                "label": '7" • serves 8–10',
                "serves_min": 8,
                "serves_max": 10,
                "price": "27.50",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Candy Party Kids Cake",
        "slug": "candy-party-kids-cake",
        "occasion_type": "birthday",
        "category": "Kids Theme",
        "short": "Bright buttercream cake topped with candy-style decorations.",
        "description": (
            "A bright buttercream cake loaded with colourful piping and candy-style "
            "decorations. Built for busy kids’ parties where you want big smiles in "
            "the photos and easy slicing for parents."
        ),
        "image": "cakes/kid02.jpg",
        "collections": ["kids", "birthday"],
        "variants": [
            {
                "label": '7" • serves 8–10',
                "serves_min": 8,
                "serves_max": 10,
                "price": "26.90",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Pastel Stars Kids Cake",
        "slug": "pastel-stars-kids-cake",
        "occasion_type": "birthday",
        "category": "Kids Theme",
        "short": "Soft pastel buttercream with star and sprinkle details.",
        "description": (
            "A soft pastel kids’ cake decorated with star shapes and sprinkles. "
            "Flexible enough to match many themes — from princess to space parties — "
            "with your custom message on top."
        ),
        "image": "cakes/kid03.jpg",
        "collections": ["kids", "birthday"],
        "variants": [
            {
                "label": '6" • serves 6–8',
                "serves_min": 6,
                "serves_max": 8,
                "price": "23.90",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Toy Blocks First Birthday Cake",
        "slug": "toy-blocks-first-birthday-cake",
        "occasion_type": "birthday",
        "category": "Kids Theme",
        "short": "Cute baby-style cake with toy-block inspired decorations.",
        "description": (
            "A gentle vanilla cake decorated with baby-style blocks and soft colours, "
            "perfect for first and second birthdays. Space on the top for a name and age."
        ),
        "image": "cakes/kid04.jpg",
        "collections": ["kids", "birthday"],
        "variants": [
            {
                "label": '6" • serves 6–8',
                "serves_min": 6,
                "serves_max": 8,
                "price": "24.90",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Football Pitch Party Cake",
        "slug": "football-pitch-party-cake",
        "occasion_type": "party",
        "category": "Kids Theme",
        "short": "Football pitch cake with chocolate sides and green grass piping.",
        "description": (
            "Chocolate base carved into a football pitch, finished with green buttercream "
            "grass and mini players. A dream cake for football lovers and team parties."
        ),
        "image": "cakes/kid05.jpg",
        "collections": ["kids", "birthday", "chocolate"],
        "variants": [
            {
                "label": '10" square • serves 18–24',
                "serves_min": 18,
                "serves_max": 24,
                "price": "39.90",
                "is_default": True,
            },
        ],
    },

    # -----------------------
    # PARTY TRAY CAKES (pt01–pt02)
    # -----------------------
    {
        "name": "Rose Gold Party Tray Cake",
        "slug": "rose-gold-party-tray-cake",
        "occasion_type": "party",
        "category": "Party Tray",
        "short": "Large vanilla sheet cake with rose-gold style piping.",
        "description": (
            "A generous vanilla sheet cake decorated with neat rose-gold style "
            "buttercream piping. Made for easy slicing at hen parties, office "
            "events and family celebrations."
        ),
        "image": "cakes/pt01.jpg",
        "collections": ["birthday"],
        "variants": [
            {
                "label": "Party tray • serves 20–24",
                "serves_min": 20,
                "serves_max": 24,
                "price": "45.00",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Chocolate Strawberry Party Sheet Cake",
        "slug": "chocolate-strawberry-party-sheet-cake",
        "occasion_type": "party",
        "category": "Chocolate Sheet",
        "short": "Large chocolate tray bake topped with cream and strawberries.",
        "description": (
            "A generous chocolate sponge baked in a large tray, topped with whipped "
            "cream, chocolate drizzle and fresh strawberries. Ideal for office "
            "celebrations, school parties and big family gatherings."
        ),
        "image": "cakes/pt02.jpg",
        "collections": ["birthday", "chocolate"],
        "variants": [
            {
                "label": "Party tray • serves 20–24",
                "serves_min": 20,
                "serves_max": 24,
                "price": "49.00",
                "is_default": True,
            },
        ],
    },

    # -----------------------
    # WEDDING TIERS (wd01–wd02)
    # -----------------------
    {
        "name": "Royal Blue Rose Tiered Cake",
        "slug": "royal-blue-rose-tiered-cake",
        "occasion_type": "wedding",
        "category": "Wedding Tier",
        "short": "Three-tier vanilla wedding cake with blue sugar roses.",
        "description": (
            "Elegant three-tier vanilla sponge decorated with hand-piped rosettes "
            "and royal blue sugar roses. Designed as a modern yet timeless wedding "
            "centre-piece."
        ),
        "image": "cakes/wd01.jpg",
        "collections": [],
        "variants": [
            {
                "label": "3 tiers • serves 60–70",
                "serves_min": 60,
                "serves_max": 70,
                "price": "159.00",
                "is_default": True,
            },
        ],
    },
    {
        "name": "Classic Red Rose Wedding Cake",
        "slug": "classic-red-rose-wedding-cake",
        "occasion_type": "wedding",
        "category": "Wedding Tier",
        "short": "Two-tier vanilla cake with classic red roses.",
        "description": (
            "Timeless two-tier vanilla wedding cake finished with white rosettes "
            "and fresh red roses. Perfect for intimate weddings and registry-style "
            "celebrations."
        ),
        "image": "cakes/wd02.jpg",
        "collections": [],
        "variants": [
            {
                "label": "2 tiers • serves 40–50",
                "serves_min": 40,
                "serves_max": 50,
                "price": "129.00",
                "is_default": True,
            },
        ],
    },
]


def load_initial_cakes():
    """
    One-shot loader to create collections, cakes, and variants.

    Safe to run multiple times:
    - Collections: get_or_create
    - Cakes: get_or_create by slug
    - Variants: only created when cake is first created (not on "already exists")
    """
    # 1) Collections
    col_map = {}
    for data in collections_data:
        obj, _ = CakeCollection.objects.get_or_create(
            key=data["key"],
            defaults={
                "label": data["label"],
                "icon": data["icon"],
                "sort_order": data["sort_order"],
                "is_active": True,
            },
        )
        col_map[data["key"]] = obj

    # 2) Cakes + variants
    for data in cakes_data:
        cake, created = Cake.objects.get_or_create(
            slug=data["slug"],
            defaults={
                "name": data["name"],
                "occasion_type": data["occasion_type"],
                "category": data["category"],
                "short_description": data["short"],
                "description": data["description"],
                # ImageField(upload_to="cakes/")
                "main_image": data["image"],
                "is_active": True,
            },
        )

        if created:
            # attach collections
            for key in data["collections"]:
                col = col_map.get(key)
                if col:
                    cake.collections.add(col)

            # create variants
            for v in data["variants"]:
                CakeVariant.objects.create(
                    cake=cake,
                    label=v["label"],
                    serves_min=v["serves_min"],
                    serves_max=v["serves_max"],
                    price=Decimal(v["price"]),
                    is_default=v["is_default"],
                )

            print("Created cake:", cake.slug)
        else:
            print("Already exists:", cake.slug)
