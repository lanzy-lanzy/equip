from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    Supply,
    SupplyCategory,
    SupplyRequest,
    QRScanLog,
    InventoryTransaction,
    BorrowedItem,
    Notification,
    EquipmentInstance,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        "username",
        "email",
        "role",
        "department",
        "approval_status",
        "is_active",
    ]
    list_filter = ["role", "approval_status", "is_active", "department"]
    search_fields = ["username", "email", "first_name", "last_name"]
    actions = ["approve_users", "reject_users"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {"fields": ("role", "department", "phone", "approval_status")},
        ),
    )

    def approve_users(self, request, queryset):
        updated = queryset.update(approval_status="approved")
        self.message_user(request, f"{updated} users were successfully approved.")

    approve_users.short_description = "Approve selected users"

    def reject_users(self, request, queryset):
        updated = queryset.update(approval_status="rejected")
        self.message_user(request, f"{updated} users were successfully rejected.")

    reject_users.short_description = "Reject selected users"


@admin.register(SupplyCategory)
class SupplyCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "is_material", "description", "created_at"]
    list_filter = ["is_material"]
    search_fields = ["name"]


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "quantity",
        "min_stock_level",
        "unit",
        "stock_status",
        "location",
    ]
    list_filter = ["category", "location"]
    search_fields = ["name", "description"]
    readonly_fields = ["qr_code"]

    def stock_status(self, obj):
        return obj.stock_status.replace("_", " ").title()

    stock_status.short_description = "Stock Status"


@admin.register(SupplyRequest)
class SupplyRequestAdmin(admin.ModelAdmin):
    list_display = [
        "request_id",
        "user",
        "supply",
        "quantity_requested",
        "status",
        "created_at",
    ]
    list_filter = ["status", "created_at"]
    search_fields = ["request_id", "user__username", "supply__name"]
    readonly_fields = ["request_id", "created_at"]


@admin.register(QRScanLog)
class QRScanLogAdmin(admin.ModelAdmin):
    list_display = ["supply", "scanned_by", "action", "location", "timestamp"]
    list_filter = ["action", "timestamp"]
    search_fields = ["supply__name", "scanned_by__username"]
    readonly_fields = ["timestamp"]


@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "supply",
        "transaction_type",
        "quantity",
        "previous_quantity",
        "new_quantity",
        "performed_by",
        "created_at",
    ]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["supply__name", "performed_by__username"]
    readonly_fields = ["created_at"]


@admin.register(BorrowedItem)
class BorrowedItemAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "supply",
        "borrower",
        "borrowed_date",
        "return_deadline",
        "is_overdue",
        "is_returned",
        "borrowed_quantity",
        "return_status",
    ]
    list_filter = ["return_status", "borrowed_date", "return_deadline", "returned_at"]
    search_fields = ["supply__name", "borrower__username", "notes"]
    readonly_fields = ["borrowed_at"]

    def is_overdue(self, obj):
        return obj.is_overdue

    is_overdue.boolean = True
    is_overdue.short_description = "Overdue"

    def is_returned(self, obj):
        return obj.is_returned

    is_returned.boolean = True
    is_returned.short_description = "Returned"

    def changelist_view(self, request, extra_context=None):
        from django.utils import timezone
        from datetime import timedelta

        if "overdue" in request.GET:
            today = timezone.now().date()
            qs = self.get_queryset(request)
            qs = qs.filter(returned_at__isnull=True, return_deadline__lt=today)
            request.GET = request.GET.copy()
            del request.GET["overdue"]
            return self.get_changelist_instance(request).queryset.filter(
                pk__in=qs.values_list("pk", flat=True)
            )
        return super().changelist_view(request, extra_context)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["id", "recipient", "title", "level", "is_read", "created_at"]
    list_filter = ["level", "is_read", "created_at"]
    search_fields = ["title", "message", "recipient__username"]
    readonly_fields = ["created_at"]


@admin.register(EquipmentInstance)
class EquipmentInstanceAdmin(admin.ModelAdmin):
    list_display = [
        "instance_code",
        "supply",
        "brand",
        "model_name",
        "serial_number",
        "status",
        "created_at",
    ]
    list_filter = ["status", "supply__category", "created_at"]
    search_fields = ["instance_code", "brand", "model_name", "serial_number", "supply__name"]
    readonly_fields = ["qr_code", "created_at", "updated_at"]
