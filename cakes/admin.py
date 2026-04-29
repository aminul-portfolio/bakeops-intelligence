from django.contrib import admin

from .models import (
    Cake,
    CakeCollection,
    CakeVariant,
    LoyaltyAccount,
    Order,
    OrderItem,
    Review,
)


@admin.register(CakeCollection)
class CakeCollectionAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "icon", "is_active", "sort_order")
    list_editable = ("is_active", "sort_order")
    search_fields = ("label", "key")


class CakeVariantInline(admin.TabularInline):
    model = CakeVariant
    extra = 1
    min_num = 1
    max_num = 3
    fields = ("label", "serves_min", "serves_max", "price", "is_default")


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "occasion_type",
        "category",
        "get_collections",
        "is_active",
        "created_at",
    )
    list_filter = (
        "occasion_type",
        "category",
        "collections",
        "is_active",
        "created_at",
    )
    search_fields = ("name", "short_description", "description", "code")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [CakeVariantInline]
    filter_horizontal = ("collections",)

    def get_collections(self, obj):
        return ", ".join(c.label for c in obj.collections.all())
    get_collections.short_description = "Collections"


from django.contrib import admin

from .models import Cake, CakeCollection, CakeVariant


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("cake", "name", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating", "created_at")
    search_fields = ("cake__name", "name", "comment")


@admin.register(LoyaltyAccount)
class LoyaltyAccountAdmin(admin.ModelAdmin):
    list_display = ("user", "points", "balance_value")
    search_fields = ("user__username", "user__email")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "total_amount",
        "points_earned",
        "points_redeemed",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "user__email")
    inlines = [OrderItemInline]
