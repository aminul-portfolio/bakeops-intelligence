from datetime import date, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from bakeops.models import (
    BakeryOrder,
    BakeryOrderItem,
    BatchAllocation,
    CakeReview,
    Customer,
    DeliverySlot,
    Ingredient,
    IngredientLot,
    LoyaltyAccount,
    OccasionType,
    ProductionBatch,
    ProductionBatchLine,
    Recipe,
    RecipeLine,
    StaffMember,
    Supplier,
    WasteRecord,
    Workspace,
)
from cakes.models import Cake, CakeCollection, CakeVariant


class Command(BaseCommand):
    help = "Seed realistic BakeOps demo data for V1 development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing SweetCakes demo data before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self._reset_demo_data()

        today = date.today()

        workspace = self._create_workspace()
        staff_member = self._create_staff(workspace, today)
        occasions = self._create_occasions(workspace)
        customers = self._create_customers(workspace, today)
        collections = self._create_collections()
        cakes = self._create_cakes(collections)
        variants = self._create_variants(cakes)
        self._create_reviews(workspace, customers, cakes, variants, today)

        suppliers = self._create_suppliers(workspace)
        ingredients = self._create_ingredients(workspace, suppliers)
        self._create_ingredient_lots(workspace, ingredients, today)

        recipes = self._create_recipes(workspace, cakes, variants)
        self._create_recipe_lines(recipes, ingredients)

        delivery_slots = self._create_delivery_slots(workspace, today)
        orders = self._create_orders(workspace, customers, occasions, delivery_slots, today)
        order_items = self._create_order_items(orders, cakes, variants)

        batch_lines = self._create_production(
            workspace=workspace,
            staff_member=staff_member,
            recipes=recipes,
            today=today,
        )
        self._create_allocations(batch_lines, order_items)
        self._create_waste_records(workspace, cakes, variants, ingredients, batch_lines, today)

        self.stdout.write(self.style.SUCCESS("BakeOps demo data seeded successfully."))
        self.stdout.write(f"Workspace: {workspace.name}")
        self.stdout.write(f"Cakes: {Cake.objects.filter(slug__startswith='demo-').count()}")
        self.stdout.write(f"Orders: {BakeryOrder.objects.filter(workspace=workspace).count()}")
        self.stdout.write(f"Ingredients: {Ingredient.objects.filter(workspace=workspace).count()}")
        self.stdout.write(f"Waste records: {WasteRecord.objects.filter(workspace=workspace).count()}")

    def _reset_demo_data(self):
        workspace = Workspace.objects.filter(name="SweetCakes Bakery").first()

        if workspace:
            # Delete dependent operational records first.
            BatchAllocation.objects.filter(
                batch_line__batch__workspace=workspace
            ).delete()

            WasteRecord.objects.filter(workspace=workspace).delete()

            ProductionBatchLine.objects.filter(
                batch__workspace=workspace
            ).delete()

            ProductionBatch.objects.filter(workspace=workspace).delete()

            RecipeLine.objects.filter(
                recipe__workspace=workspace
            ).delete()

            Recipe.objects.filter(workspace=workspace).delete()

            BakeryOrderItem.objects.filter(
                order__workspace=workspace
            ).delete()

            BakeryOrder.objects.filter(workspace=workspace).delete()

            DeliverySlot.objects.filter(workspace=workspace).delete()

            CakeReview.objects.filter(workspace=workspace).delete()

            LoyaltyAccount.objects.filter(workspace=workspace).delete()

            Customer.objects.filter(workspace=workspace).delete()

            OccasionType.objects.filter(workspace=workspace).delete()

            IngredientLot.objects.filter(workspace=workspace).delete()

            Ingredient.objects.filter(workspace=workspace).delete()

            Supplier.objects.filter(workspace=workspace).delete()

            StaffMember.objects.filter(workspace=workspace).delete()

            Workspace.objects.filter(pk=workspace.pk).delete()

        # Delete demo catalogue records after BakeOps references are gone.
        Cake.objects.filter(slug__startswith="demo-").delete()
        CakeCollection.objects.filter(key__startswith="demo-").delete()

    def _create_workspace(self):
        workspace, _ = Workspace.objects.update_or_create(
            name="SweetCakes Bakery",
            defaults={
                "legal_name": "SweetCakes Bakery Ltd",
                "email": "ops@sweetcakes.example",
                "phone": "+44 20 0000 0000",
                "city": "Croydon",
                "country": "United Kingdom",
                "currency": "GBP",
                "is_active": True,
            },
        )
        return workspace

    def _create_staff(self, workspace, today):
        staff_member, _ = StaffMember.objects.update_or_create(
            workspace=workspace,
            full_name="Aisha Rahman",
            defaults={
                "role": StaffMember.ROLE_MANAGER,
                "email": "aisha@sweetcakes.example",
                "is_active": True,
                "joined_on": today - timedelta(days=420),
            },
        )
        return staff_member

    def _create_occasions(self, workspace):
        data = [
            ("Birthday", "Birthday cake demand and party orders."),
            ("Wedding", "Wedding and celebration cake demand."),
            ("Anniversary", "Anniversary and family celebration demand."),
            ("Everyday Treat", "Small everyday cake orders."),
        ]

        occasions = {}

        for name, description in data:
            occasion, _ = OccasionType.objects.update_or_create(
                workspace=workspace,
                name=name,
                defaults={
                    "description": description,
                    "is_active": True,
                },
            )
            occasions[name] = occasion

        return occasions

    def _create_customers(self, workspace, today):
        data = [
            ("Maya Patel", "maya@example.com", "CR0 1AA", True, 220, 310, 90),
            ("Daniel Ahmed", "daniel@example.com", "CR0 2BB", True, 140, 180, 40),
            ("Sophie Green", "sophie@example.com", "CR2 3CC", False, 30, 30, 0),
            ("Imran Chowdhury", "imran@example.com", "CR7 4DD", True, 75, 120, 45),
            ("Laura Smith", "laura@example.com", "CR8 5EE", False, 10, 10, 0),
        ]

        customers = {}

        for full_name, email, postcode, repeat, balance, earned, redeemed in data:
            customer, _ = Customer.objects.update_or_create(
                workspace=workspace,
                email=email,
                defaults={
                    "full_name": full_name,
                    "phone": "",
                    "postcode": postcode,
                    "is_repeat_customer": repeat,
                },
            )

            LoyaltyAccount.objects.update_or_create(
                workspace=workspace,
                customer=customer,
                defaults={
                    "points_balance": balance,
                    "lifetime_points_earned": earned,
                    "lifetime_points_redeemed": redeemed,
                    "joined_on": today - timedelta(days=180),
                    "is_active": True,
                },
            )

            customers[full_name] = customer

        return customers

    def _create_collections(self):
        data = [
            ("demo-birthday", "Birthday Zone", "🎂", 1),
            ("demo-wedding", "Wedding Collection", "💍", 2),
            ("demo-chocolate", "Chocolate Collection", "🍫", 3),
            ("demo-everyday", "Everyday Treats", "☕", 4),
        ]

        collections = {}

        for key, label, icon, sort_order in data:
            collection, _ = CakeCollection.objects.update_or_create(
                key=key,
                defaults={
                    "label": label,
                    "icon": icon,
                    "description": f"Demo collection for {label}.",
                    "is_active": True,
                    "sort_order": sort_order,
                },
            )
            collections[key] = collection

        return collections

    def _create_cakes(self, collections):
        data = [
            {
                "slug": "demo-birthday-classic",
                "name": "Birthday Classic",
                "occasion_type": Cake.OccasionType.PARTY,
                "category": "Birthday",
                "image": "cakes/bd01.jpg",
                "collections": ["demo-birthday"],
            },
            {
                "slug": "demo-luxury-chocolate",
                "name": "Luxury Chocolate",
                "occasion_type": Cake.OccasionType.OTHER,
                "category": "Chocolate",
                "image": "cakes/dark_choco.jpg",
                "collections": ["demo-chocolate"],
            },
            {
                "slug": "demo-wedding-rose",
                "name": "Wedding Rose",
                "occasion_type": Cake.OccasionType.WEDDING,
                "category": "Wedding",
                "image": "cakes/wd01.jpg",
                "collections": ["demo-wedding"],
            },
            {
                "slug": "demo-lemon-poppy",
                "name": "Lemon Poppy",
                "occasion_type": Cake.OccasionType.OTHER,
                "category": "Everyday",
                "image": "cakes/lemon_poppy.jpg",
                "collections": ["demo-everyday"],
            },
        ]

        cakes = {}

        for item in data:
            cake, _ = Cake.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "occasion_type": item["occasion_type"],
                    "category": item["category"],
                    "short_description": f"Demo {item['name']} cake.",
                    "description": f"Seeded demo product for BakeOps analytics: {item['name']}.",
                    "main_image": item["image"],
                    "code": item["slug"].replace("demo-", "").upper(),
                    "ingredients": "Demo ingredients for analytics testing.",
                    "allergy_advice": "Contains gluten, dairy, and may contain nuts.",
                    "nutrition_info": "Demo nutrition information.",
                    "is_active": True,
                },
            )

            cake.collections.set([collections[key] for key in item["collections"]])
            cakes[item["name"]] = cake

        return cakes

    def _create_variants(self, cakes):
        data = [
            ("Birthday Classic", '8" • serves 10–12', 10, 12, Decimal("45.00"), True),
            ("Luxury Chocolate", '6" • serves 6–8', 6, 8, Decimal("38.00"), True),
            ("Wedding Rose", '10" • serves 20–24', 20, 24, Decimal("95.00"), True),
            ("Lemon Poppy", '6" • serves 6–8', 6, 8, Decimal("28.00"), True),
        ]

        variants = {}

        for cake_name, label, serves_min, serves_max, price, is_default in data:
            variant, _ = CakeVariant.objects.update_or_create(
                cake=cakes[cake_name],
                label=label,
                defaults={
                    "serves_min": serves_min,
                    "serves_max": serves_max,
                    "price": price,
                    "is_default": is_default,
                },
            )
            variants[cake_name] = variant

        return variants

    def _create_reviews(self, workspace, customers, cakes, variants, today):
        data = [
            ("Birthday Classic", "Maya Patel", 5, "Great birthday cake"),
            ("Birthday Classic", "Daniel Ahmed", 4, "Looked amazing"),
            ("Luxury Chocolate", "Sophie Green", 5, "Rich and premium"),
            ("Wedding Rose", "Imran Chowdhury", 5, "Beautiful finish"),
            ("Lemon Poppy", "Laura Smith", 4, "Fresh and light"),
        ]

        for cake_name, customer_name, rating, title in data:
            CakeReview.objects.update_or_create(
                workspace=workspace,
                cake=cakes[cake_name],
                variant=variants[cake_name],
                customer=customers[customer_name],
                review_date=today - timedelta(days=rating * 3),
                defaults={
                    "rating": rating,
                    "title": title,
                    "comment": f"Demo review for {cake_name}.",
                    "is_verified_purchase": True,
                },
            )

    def _create_suppliers(self, workspace):
        data = [
            ("London Flour Mill", "Mina Carter", 2),
            ("Cocoa Direct", "James Brown", 4),
            ("Fresh Dairy Co", "Sarah Ali", 1),
            ("Fruit & Zest Market", "Nadia Khan", 1),
        ]

        suppliers = {}

        for name, contact_name, lead_time in data:
            supplier, _ = Supplier.objects.update_or_create(
                workspace=workspace,
                name=name,
                defaults={
                    "contact_name": contact_name,
                    "email": "",
                    "phone": "",
                    "lead_time_days": lead_time,
                    "is_active": True,
                },
            )
            suppliers[name] = supplier

        return suppliers

    def _create_ingredients(self, workspace, suppliers):
        data = [
            ("Flour", "kg", "1.20", "18.000", "10.000", "London Flour Mill"),
            ("Sugar", "kg", "0.95", "12.000", "8.000", "London Flour Mill"),
            ("Butter", "kg", "6.40", "4.000", "5.000", "Fresh Dairy Co"),
            ("Eggs", "each", "0.28", "90.000", "60.000", "Fresh Dairy Co"),
            ("Dark Chocolate", "kg", "9.50", "3.000", "4.000", "Cocoa Direct"),
            ("Fresh Cream", "l", "3.20", "5.000", "6.000", "Fresh Dairy Co"),
            ("Lemon Zest", "kg", "7.00", "0.800", "1.000", "Fruit & Zest Market"),
            ("Decorative Icing", "kg", "5.80", "2.000", "3.000", "London Flour Mill"),
        ]

        ingredients = {}

        for name, unit, cost, stock, reorder, supplier_name in data:
            ingredient, _ = Ingredient.objects.update_or_create(
                workspace=workspace,
                name=name,
                defaults={
                    "supplier": suppliers[supplier_name],
                    "unit": unit,
                    "cost_per_unit": Decimal(cost),
                    "current_stock_quantity": Decimal(stock),
                    "reorder_level_quantity": Decimal(reorder),
                    "is_active": True,
                },
            )
            ingredients[name] = ingredient

        return ingredients

    def _create_ingredient_lots(self, workspace, ingredients, today):
        data = [
            ("FLOUR-001", "Flour", -10, 45, "18.000", "18.000", "1.20"),
            ("SUGAR-001", "Sugar", -8, 90, "12.000", "12.000", "0.95"),
            ("BUTTER-001", "Butter", -4, 5, "8.000", "4.000", "6.40"),
            ("EGGS-001", "Eggs", -2, 4, "180.000", "90.000", "0.28"),
            ("CHOC-001", "Dark Chocolate", -12, 120, "6.000", "3.000", "9.50"),
            ("CREAM-001", "Fresh Cream", -1, 3, "10.000", "5.000", "3.20"),
            ("LEMON-001", "Lemon Zest", -2, 6, "2.000", "0.800", "7.00"),
            ("ICING-001", "Decorative Icing", -5, 60, "5.000", "2.000", "5.80"),
        ]

        for lot_code, ingredient_name, received_offset, expiry_offset, qty_received, qty_remaining, unit_cost in data:
            IngredientLot.objects.update_or_create(
                workspace=workspace,
                lot_code=lot_code,
                defaults={
                    "ingredient": ingredients[ingredient_name],
                    "received_date": today + timedelta(days=received_offset),
                    "expiry_date": today + timedelta(days=expiry_offset),
                    "quantity_received": Decimal(qty_received),
                    "quantity_remaining": Decimal(qty_remaining),
                    "unit_cost": Decimal(unit_cost),
                },
            )

    def _create_recipes(self, workspace, cakes, variants):
        data = [
            ("Birthday Classic Recipe", "Birthday Classic", "1.00", 55, "4.50"),
            ("Luxury Chocolate Recipe", "Luxury Chocolate", "1.00", 65, "5.50"),
            ("Wedding Rose Recipe", "Wedding Rose", "1.00", 140, "15.00"),
            ("Lemon Poppy Recipe", "Lemon Poppy", "1.00", 45, "3.50"),
        ]

        recipes = {}

        for recipe_name, cake_name, yield_qty, labour, overhead in data:
            recipe, _ = Recipe.objects.update_or_create(
                workspace=workspace,
                cake=cakes[cake_name],
                variant=variants[cake_name],
                name=recipe_name,
                defaults={
                    "expected_yield_quantity": Decimal(yield_qty),
                    "labour_minutes": labour,
                    "overhead_cost": Decimal(overhead),
                    "is_active": True,
                },
            )
            recipes[cake_name] = recipe

        return recipes

    def _create_recipe_lines(self, recipes, ingredients):
        data = {
            "Birthday Classic": [
                ("Flour", "0.750", "4.00"),
                ("Sugar", "0.420", "3.00"),
                ("Butter", "0.380", "6.00"),
                ("Eggs", "8.000", "2.00"),
                ("Fresh Cream", "0.800", "12.00"),
                ("Decorative Icing", "0.650", "18.00"),
            ],
            "Luxury Chocolate": [
                ("Flour", "0.500", "3.00"),
                ("Sugar", "0.350", "2.00"),
                ("Butter", "0.320", "4.00"),
                ("Eggs", "6.000", "2.00"),
                ("Dark Chocolate", "0.700", "5.00"),
                ("Fresh Cream", "0.350", "8.00"),
            ],
            "Wedding Rose": [
                ("Flour", "1.400", "4.00"),
                ("Sugar", "0.900", "3.00"),
                ("Butter", "0.900", "5.00"),
                ("Eggs", "18.000", "2.00"),
                ("Fresh Cream", "1.200", "8.00"),
                ("Decorative Icing", "1.500", "10.00"),
            ],
            "Lemon Poppy": [
                ("Flour", "0.420", "3.00"),
                ("Sugar", "0.240", "2.00"),
                ("Butter", "0.180", "3.00"),
                ("Eggs", "5.000", "2.00"),
                ("Lemon Zest", "0.180", "6.00"),
            ],
        }

        for cake_name, lines in data.items():
            for ingredient_name, quantity, waste_percent in lines:
                RecipeLine.objects.update_or_create(
                    recipe=recipes[cake_name],
                    ingredient=ingredients[ingredient_name],
                    defaults={
                        "quantity_required": Decimal(quantity),
                        "waste_factor_percent": Decimal(waste_percent),
                    },
                )

    def _create_delivery_slots(self, workspace, today):
        slots = {}

        for index in range(5):
            slot_date = today + timedelta(days=index)
            slot, _ = DeliverySlot.objects.update_or_create(
                workspace=workspace,
                slot_date=slot_date,
                start_time=time(10, 0),
                end_time=time(13, 0),
                defaults={
                    "capacity_orders": 8,
                    "booked_orders": 6 if index in [1, 2] else 3,
                    "is_active": True,
                },
            )
            slots[index] = slot

        return slots

    def _create_orders(self, workspace, customers, occasions, delivery_slots, today):
        data = [
            ("SC-1001", "Maya Patel", "Birthday", 0, "paid", "website", "135.00", 6, 0),
            ("SC-1002", "Daniel Ahmed", "Birthday", 0, "paid", "phone", "90.00", 4, 0),
            ("SC-1003", "Sophie Green", "Everyday Treat", 1, "paid", "website", "76.00", 3, 0),
            ("SC-1004", "Imran Chowdhury", "Wedding", 2, "paid", "in_store", "190.00", 8, 25),
            ("SC-1005", "Laura Smith", "Everyday Treat", 2, "paid", "social", "56.00", 2, 0),
            ("SC-1006", "Maya Patel", "Birthday", 3, "fulfilled", "website", "180.00", 9, 30),
            ("SC-1007", "Daniel Ahmed", "Anniversary", 4, "confirmed", "phone", "95.00", 0, 0),
        ]

        orders = {}

        for order_number, customer_name, occasion_name, slot_index, status, channel, total, earned, redeemed in data:
            order, _ = BakeryOrder.objects.update_or_create(
                workspace=workspace,
                order_number=order_number,
                defaults={
                    "customer": customers[customer_name],
                    "occasion": occasions[occasion_name],
                    "delivery_slot": delivery_slots[slot_index],
                    "order_date": today - timedelta(days=max(0, 3 - slot_index)),
                    "required_date": today + timedelta(days=slot_index),
                    "status": status,
                    "channel": channel,
                    "subtotal": Decimal(total),
                    "discount_amount": Decimal("0.00"),
                    "total_amount": Decimal(total),
                    "loyalty_points_earned": earned,
                    "loyalty_points_redeemed": redeemed,
                    "notes": "Seeded demo order for BakeOps V1.",
                },
            )
            orders[order_number] = order

        return orders

    def _create_order_items(self, orders, cakes, variants):
        data = [
            ("SC-1001", "Birthday Classic", 3, "45.00"),
            ("SC-1002", "Birthday Classic", 2, "45.00"),
            ("SC-1003", "Luxury Chocolate", 2, "38.00"),
            ("SC-1004", "Wedding Rose", 2, "95.00"),
            ("SC-1005", "Lemon Poppy", 2, "28.00"),
            ("SC-1006", "Birthday Classic", 4, "45.00"),
            ("SC-1007", "Wedding Rose", 1, "95.00"),
        ]

        order_items = {}

        for order_number, cake_name, quantity, unit_price in data:
            order = orders[order_number]
            cake = cakes[cake_name]
            variant = variants[cake_name]
            line_total = Decimal(unit_price) * Decimal(quantity)

            item, _ = BakeryOrderItem.objects.update_or_create(
                order=order,
                cake=cake,
                variant=variant,
                defaults={
                    "quantity": quantity,
                    "unit_price": Decimal(unit_price),
                    "line_total": line_total,
                    "special_instructions": "",
                },
            )
            order_items[(order_number, cake_name)] = item

        return order_items

    def _create_production(self, workspace, staff_member, recipes, today):
        batch, _ = ProductionBatch.objects.update_or_create(
            workspace=workspace,
            batch_code="BATCH-DEMO-001",
            defaults={
                "production_date": today,
                "status": ProductionBatch.STATUS_COMPLETED,
                "planned_by": staff_member,
                "notes": "Seeded production batch for BakeOps V1.",
            },
        )

        data = [
            ("Birthday Classic", "10.00", "9.00", "1.00"),
            ("Luxury Chocolate", "3.00", "3.00", "0.00"),
            ("Wedding Rose", "3.00", "3.00", "0.00"),
            ("Lemon Poppy", "3.00", "2.00", "1.00"),
        ]

        batch_lines = {}

        for cake_name, planned, produced, failed in data:
            line, _ = ProductionBatchLine.objects.update_or_create(
                batch=batch,
                recipe=recipes[cake_name],
                defaults={
                    "planned_quantity": Decimal(planned),
                    "produced_quantity": Decimal(produced),
                    "failed_quantity": Decimal(failed),
                },
            )
            batch_lines[cake_name] = line

        return batch_lines

    def _create_allocations(self, batch_lines, order_items):
        mapping = [
            ("Birthday Classic", "SC-1001", "Birthday Classic", "3.00"),
            ("Birthday Classic", "SC-1002", "Birthday Classic", "2.00"),
            ("Birthday Classic", "SC-1006", "Birthday Classic", "4.00"),
            ("Luxury Chocolate", "SC-1003", "Luxury Chocolate", "2.00"),
            ("Wedding Rose", "SC-1004", "Wedding Rose", "2.00"),
            ("Wedding Rose", "SC-1007", "Wedding Rose", "1.00"),
            ("Lemon Poppy", "SC-1005", "Lemon Poppy", "2.00"),
        ]

        for batch_cake_name, order_number, item_cake_name, quantity in mapping:
            BatchAllocation.objects.update_or_create(
                batch_line=batch_lines[batch_cake_name],
                order_item=order_items[(order_number, item_cake_name)],
                defaults={
                    "allocated_quantity": Decimal(quantity),
                },
            )

    def _create_waste_records(self, workspace, cakes, variants, ingredients, batch_lines, today):
        data = [
            (
                today,
                WasteRecord.REASON_OVERPRODUCTION,
                None,
                "Birthday Classic",
                "Birthday Classic",
                "1.000",
                "18.50",
                "Birthday Classic overproduction after large party batch.",
            ),
            (
                today,
                WasteRecord.REASON_QUALITY_ISSUE,
                None,
                "Birthday Classic",
                "Birthday Classic",
                "1.000",
                "14.25",
                "Decorative icing quality issue.",
            ),
            (
                today,
                WasteRecord.REASON_EXPIRY,
                "Fresh Cream",
                None,
                None,
                "1.200",
                "3.84",
                "Fresh cream close to expiry.",
            ),
            (
                today,
                WasteRecord.REASON_RECIPE_ERROR,
                "Lemon Zest",
                "Lemon Poppy",
                "Lemon Poppy",
                "0.200",
                "1.40",
                "Recipe measurement issue.",
            ),
        ]

        for waste_date, reason, ingredient_name, cake_name, batch_line_name, quantity, cost, notes in data:
            ingredient = ingredients.get(ingredient_name) if ingredient_name else None
            cake = cakes.get(cake_name) if cake_name else None
            variant = variants.get(cake_name) if cake_name else None
            batch_line = batch_lines.get(batch_line_name) if batch_line_name else None

            WasteRecord.objects.update_or_create(
                workspace=workspace,
                waste_date=waste_date,
                reason=reason,
                ingredient=ingredient,
                cake=cake,
                variant=variant,
                batch_line=batch_line,
                notes=notes,
                defaults={
                    "quantity": Decimal(quantity),
                    "estimated_cost": Decimal(cost),
                },
            )