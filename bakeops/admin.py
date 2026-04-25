from django.contrib import admin

from .models import (
    BakeryMetricRunLog,
    BakeryOrder,
    BakeryOrderItem,
    BatchAllocation,
    CakeReview,
    Customer,
    CustomerLoyaltySnapshot,
    DailyBakeryMetric,
    DataQualityIssue,
    DeliverySlot,
    Ingredient,
    IngredientLot,
    IngredientUsageSnapshot,
    LoyaltyAccount,
    OccasionDemandSnapshot,
    OccasionType,
    ProductPerformanceSnapshot,
    ProductionBatch,
    ProductionBatchLine,
    Recipe,
    RecipeLine,
    StaffMember,
    Supplier,
    WasteRecord,
    Workspace,
)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "legal_name",
        "city",
        "country",
        "currency",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "country", "currency")
    search_fields = ("name", "legal_name", "email", "phone", "city")
    readonly_fields = ("created_at",)


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "workspace",
        "role",
        "email",
        "is_active",
        "joined_on",
    )
    list_filter = ("workspace", "role", "is_active")
    search_fields = ("full_name", "email", "workspace__name")
    list_select_related = ("workspace", "user")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "workspace",
        "email",
        "phone",
        "postcode",
        "is_repeat_customer",
        "created_at",
    )
    list_filter = ("workspace", "is_repeat_customer", "created_at")
    search_fields = ("full_name", "email", "phone", "postcode", "workspace__name")
    list_select_related = ("workspace",)
    readonly_fields = ("created_at",)


@admin.register(LoyaltyAccount)
class LoyaltyAccountAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "workspace",
        "points_balance",
        "lifetime_points_earned",
        "lifetime_points_redeemed",
        "joined_on",
        "is_active",
    )
    list_filter = ("workspace", "is_active", "joined_on")
    search_fields = ("customer__full_name", "customer__email", "workspace__name")
    list_select_related = ("workspace", "customer")


@admin.register(OccasionType)
class OccasionTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "workspace", "is_active")
    list_filter = ("workspace", "is_active")
    search_fields = ("name", "description", "workspace__name")
    list_select_related = ("workspace",)


@admin.register(CakeReview)
class CakeReviewAdmin(admin.ModelAdmin):
    list_display = (
        "cake",
        "variant",
        "customer",
        "workspace",
        "rating",
        "review_date",
        "is_verified_purchase",
    )
    list_filter = ("workspace", "rating", "is_verified_purchase", "review_date")
    search_fields = (
        "cake__name",
        "variant__name",
        "customer__full_name",
        "title",
        "comment",
        "workspace__name",
    )
    list_select_related = ("workspace", "cake", "variant", "customer")


@admin.register(DeliverySlot)
class DeliverySlotAdmin(admin.ModelAdmin):
    list_display = (
        "slot_date",
        "start_time",
        "end_time",
        "workspace",
        "capacity_orders",
        "booked_orders",
        "is_active",
    )
    list_filter = ("workspace", "slot_date", "is_active")
    search_fields = ("workspace__name",)
    list_select_related = ("workspace",)


class BakeryOrderItemInline(admin.TabularInline):
    model = BakeryOrderItem
    extra = 0
    fields = (
        "cake",
        "variant",
        "quantity",
        "unit_price",
        "line_total",
        "special_instructions",
    )


@admin.register(BakeryOrder)
class BakeryOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "workspace",
        "customer",
        "occasion",
        "order_date",
        "required_date",
        "status",
        "channel",
        "total_amount",
    )
    list_filter = (
        "workspace",
        "status",
        "channel",
        "occasion",
        "order_date",
        "required_date",
    )
    search_fields = (
        "order_number",
        "customer__full_name",
        "customer__email",
        "workspace__name",
        "notes",
    )
    list_select_related = ("workspace", "customer", "occasion", "delivery_slot")
    inlines = [BakeryOrderItemInline]


@admin.register(BakeryOrderItem)
class BakeryOrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "cake",
        "variant",
        "quantity",
        "unit_price",
        "line_total",
    )
    list_filter = ("order__workspace", "cake", "variant")
    search_fields = ("order__order_number", "cake__name", "variant__name")
    list_select_related = ("order", "cake", "variant")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "workspace",
        "contact_name",
        "email",
        "phone",
        "lead_time_days",
        "is_active",
    )
    list_filter = ("workspace", "is_active", "lead_time_days")
    search_fields = ("name", "contact_name", "email", "phone", "workspace__name")
    list_select_related = ("workspace",)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "workspace",
        "supplier",
        "unit",
        "cost_per_unit",
        "current_stock_quantity",
        "reorder_level_quantity",
        "is_active",
    )
    list_filter = ("workspace", "supplier", "unit", "is_active")
    search_fields = ("name", "supplier__name", "workspace__name")
    list_select_related = ("workspace", "supplier")


@admin.register(IngredientLot)
class IngredientLotAdmin(admin.ModelAdmin):
    list_display = (
        "lot_code",
        "ingredient",
        "workspace",
        "received_date",
        "expiry_date",
        "quantity_received",
        "quantity_remaining",
        "unit_cost",
    )
    list_filter = ("workspace", "ingredient", "received_date", "expiry_date")
    search_fields = ("lot_code", "ingredient__name", "workspace__name")
    list_select_related = ("workspace", "ingredient")


class RecipeLineInline(admin.TabularInline):
    model = RecipeLine
    extra = 0
    fields = ("ingredient", "quantity_required", "waste_factor_percent")
    autocomplete_fields = ("ingredient",)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "workspace",
        "cake",
        "variant",
        "expected_yield_quantity",
        "labour_minutes",
        "overhead_cost",
        "is_active",
    )
    list_filter = ("workspace", "cake", "variant", "is_active")
    search_fields = ("name", "cake__name", "variant__name", "workspace__name")
    list_select_related = ("workspace", "cake", "variant")
    inlines = [RecipeLineInline]


@admin.register(RecipeLine)
class RecipeLineAdmin(admin.ModelAdmin):
    list_display = (
        "recipe",
        "ingredient",
        "quantity_required",
        "waste_factor_percent",
    )
    list_filter = ("recipe__workspace", "ingredient")
    search_fields = ("recipe__name", "ingredient__name")
    list_select_related = ("recipe", "ingredient")


class ProductionBatchLineInline(admin.TabularInline):
    model = ProductionBatchLine
    extra = 0
    fields = (
        "recipe",
        "planned_quantity",
        "produced_quantity",
        "failed_quantity",
    )
    autocomplete_fields = ("recipe",)


@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = (
        "batch_code",
        "workspace",
        "production_date",
        "status",
        "planned_by",
    )
    list_filter = ("workspace", "status", "production_date")
    search_fields = ("batch_code", "workspace__name", "notes")
    list_select_related = ("workspace", "planned_by")
    inlines = [ProductionBatchLineInline]


@admin.register(ProductionBatchLine)
class ProductionBatchLineAdmin(admin.ModelAdmin):
    list_display = (
        "batch",
        "recipe",
        "planned_quantity",
        "produced_quantity",
        "failed_quantity",
    )
    list_filter = ("batch__workspace", "batch__status", "batch__production_date")
    search_fields = ("batch__batch_code", "recipe__name")
    list_select_related = ("batch", "recipe")


@admin.register(BatchAllocation)
class BatchAllocationAdmin(admin.ModelAdmin):
    list_display = (
        "batch_line",
        "order_item",
        "allocated_quantity",
    )
    list_filter = ("batch_line__batch__workspace",)
    search_fields = (
        "batch_line__batch__batch_code",
        "order_item__order__order_number",
        "order_item__cake__name",
    )
    list_select_related = ("batch_line", "order_item")


@admin.register(WasteRecord)
class WasteRecordAdmin(admin.ModelAdmin):
    list_display = (
        "waste_date",
        "workspace",
        "reason",
        "ingredient",
        "cake",
        "variant",
        "quantity",
        "estimated_cost",
    )
    list_filter = (
        "workspace",
        "reason",
        "waste_date",
        "ingredient",
        "cake",
        "variant",
    )
    search_fields = (
        "ingredient__name",
        "cake__name",
        "variant__name",
        "notes",
        "workspace__name",
    )
    list_select_related = (
        "workspace",
        "ingredient",
        "cake",
        "variant",
        "batch_line",
    )


@admin.register(DailyBakeryMetric)
class DailyBakeryMetricAdmin(admin.ModelAdmin):
    list_display = (
        "metric_date",
        "workspace",
        "revenue",
        "paid_orders",
        "average_order_value",
        "gross_margin",
        "waste_cost",
        "waste_adjusted_margin",
        "waste_adjusted_margin_percent",
    )
    list_filter = ("workspace", "metric_date")
    search_fields = ("workspace__name",)
    list_select_related = ("workspace",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProductPerformanceSnapshot)
class ProductPerformanceSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "snapshot_date",
        "workspace",
        "cake",
        "variant",
        "revenue",
        "quantity_sold",
        "revenue_rank",
        "waste_adjusted_margin_rank",
        "waste_adjusted_margin",
        "action_flag",
    )
    list_filter = (
        "workspace",
        "snapshot_date",
        "action_flag",
        "cake",
        "variant",
    )
    search_fields = (
        "cake__name",
        "variant__name",
        "action_reason",
        "workspace__name",
    )
    list_select_related = ("workspace", "cake", "variant")
    readonly_fields = ("created_at",)


@admin.register(IngredientUsageSnapshot)
class IngredientUsageSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "snapshot_date",
        "workspace",
        "ingredient",
        "quantity_used",
        "quantity_wasted",
        "ingredient_cost",
        "waste_cost",
        "stock_risk_level",
        "near_expiry_lot_count",
        "nearest_expiry_date",
    )
    list_filter = (
        "workspace",
        "snapshot_date",
        "stock_risk_level",
        "nearest_expiry_date",
    )
    search_fields = ("ingredient__name", "workspace__name")
    list_select_related = ("workspace", "ingredient")
    readonly_fields = ("created_at",)


@admin.register(OccasionDemandSnapshot)
class OccasionDemandSnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "snapshot_date",
        "workspace",
        "occasion",
        "order_count",
        "quantity_sold",
        "revenue",
        "gross_margin",
        "upcoming_order_count",
        "delivery_slot_pressure_count",
    )
    list_filter = ("workspace", "snapshot_date", "occasion")
    search_fields = ("occasion__name", "workspace__name")
    list_select_related = ("workspace", "occasion")
    readonly_fields = ("created_at",)


@admin.register(CustomerLoyaltySnapshot)
class CustomerLoyaltySnapshotAdmin(admin.ModelAdmin):
    list_display = (
        "snapshot_date",
        "workspace",
        "customer",
        "total_orders",
        "total_revenue",
        "average_order_value",
        "loyalty_points_earned",
        "loyalty_points_redeemed",
        "current_points_balance",
        "is_repeat_customer",
    )
    list_filter = ("workspace", "snapshot_date", "is_repeat_customer")
    search_fields = ("customer__full_name", "customer__email", "workspace__name")
    list_select_related = ("workspace", "customer")
    readonly_fields = ("created_at",)


@admin.register(BakeryMetricRunLog)
class BakeryMetricRunLogAdmin(admin.ModelAdmin):
    list_display = (
        "command_name",
        "workspace",
        "status",
        "started_at",
        "finished_at",
        "duration_seconds",
        "rows_processed",
        "metrics_created",
        "snapshots_created",
        "issues_created",
    )
    list_filter = ("workspace", "status", "command_name", "started_at", "finished_at")
    search_fields = (
        "command_name",
        "workspace__name",
        "error_message",
        "notes",
    )
    list_select_related = ("workspace",)
    readonly_fields = ("started_at",)


@admin.register(DataQualityIssue)
class DataQualityIssueAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "workspace",
        "issue_type",
        "severity",
        "status",
        "detected_at",
        "resolved_at",
    )
    list_filter = (
        "workspace",
        "issue_type",
        "severity",
        "status",
        "detected_at",
        "resolved_at",
    )
    search_fields = (
        "title",
        "description",
        "suggested_action",
        "resolution_notes",
        "workspace__name",
    )
    list_select_related = ("workspace", "affected_content_type")
    readonly_fields = ("detected_at", "affected_object")