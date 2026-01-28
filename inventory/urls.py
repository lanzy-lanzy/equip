from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import analytics_views
from . import stock_adjustment_views

urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile_update, name="profile_update"),
    # Landing Page (no authentication required)
    path("", views.landing_page, name="landing_page"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Supply Management
    path("supplies/", views.supply_list, name="supply_list"),
    path("supplies/create/", views.supply_create, name="supply_create"),
    path("supplies/import/", views.supply_import, name="supply_import"),
    path(
        "supplies/import/process/",
        views.supply_import_process,
        name="supply_import_process",
    ),
    path(
        "supplies/bulk-delete/", views.bulk_delete_supplies, name="bulk_delete_supplies"
    ),
    path("supplies/history/", views.transaction_list, name="transaction_list"),
    path("supplies/<int:pk>/", views.supply_detail, name="supply_detail"),
    path("supplies/<int:pk>/restock/", views.supply_restock, name="supply_restock"),
    path("supplies/<int:pk>/edit/", views.supply_edit, name="supply_edit"),
    path("supplies/<int:pk>/delete/", views.supply_delete, name="supply_delete"),
    path(
        "supplies/<int:pk>/generate-qr/",
        views.generate_qr_code,
        name="generate_qr_code",
    ),
    path("supplies/<int:pk>/qr/", views.get_qr_code, name="get_qr_code"),
    path(
        "supplies/generate-qr-bulk/",
        views.generate_qr_codes_bulk,
        name="generate_qr_codes_bulk",
    ),
    # Equipment Instances
    path(
        "supplies/<int:pk>/instances/",
        views.equipment_instance_list,
        name="equipment_instance_list",
    ),
    path(
        "supplies/<int:pk>/instances/create/",
        views.equipment_instance_create,
        name="equipment_instance_create",
    ),
    path(
        "supplies/<int:pk>/instances/bulk-create/",
        views.equipment_instance_bulk_create,
        name="equipment_instance_bulk_create",
    ),
    path(
        "instances/<int:pk>/",
        views.equipment_instance_detail,
        name="equipment_instance_detail",
    ),
    path(
        "instances/<int:pk>/qr/",
        views.get_instance_qr_code,
        name="get_instance_qr_code",
    ),
    path(
        "instances/<int:pk>/edit/",
        views.equipment_instance_edit,
        name="equipment_instance_edit",
    ),
    path(
        "instances/<int:pk>/return/",
        views.return_instance,
        name="return_instance",
    ),
    # Category Management
    path("categories/", views.category_list, name="category_list"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path(
        "categories/bulk-delete/",
        views.bulk_delete_categories,
        name="bulk_delete_categories",
    ),
    path(
        "api/categories/create/", views.create_category_api, name="create_category_api"
    ),
    path("api/categories/list/", views.get_categories_api, name="get_categories_api"),
    path(
        "api/categories/<int:pk>/supplies/",
        views.get_category_supplies_api,
        name="get_category_supplies_api",
    ),
    # Supply Suggestions (AI)
    path(
        "api/supply-suggestions/",
        views.get_supply_suggestions,
        name="get_supply_suggestions",
    ),
    # Request Management
    path("requests/", views.request_list, name="request_list"),
    path("requests/create/", views.request_create, name="request_create"),
    path(
        "requests/bulk-create/", views.bulk_request_create, name="bulk_request_create"
    ),
    path("requests/<int:pk>/", views.request_detail, name="request_detail"),
    path("requests/<int:pk>/approve/", views.request_approve, name="request_approve"),
    path("requests/<int:pk>/reject/", views.request_reject, name="request_reject"),
    path("requests/<int:pk>/release/", views.request_release, name="request_release"),
    # Bulk actions
    path(
        "requests/bulk/<str:group_id>/approve/",
        views.bulk_approve_request,
        name="bulk_approve_request",
    ),
    path(
        "requests/bulk/<str:group_id>/reject/",
        views.bulk_reject_request,
        name="bulk_reject_request",
    ),
    path(
        "requests/bulk/<str:group_id>/release/",
        views.bulk_release_request,
        name="bulk_release_request",
    ),
    path(
        "requests/bulk/<str:group_id>/return/",
        views.bulk_return_request,
        name="bulk_return_request",
    ),
    path(
        "requests/bulk/<str:group_id>/download/",
        views.download_batch_qrcodes,
        name="download_batch_qrcodes",
    ),
    # Department Request History
    path(
        "department/request-history/",
        views.department_request_history,
        name="department_request_history",
    ),
    # Borrowing Management
    path("borrow/request/", views.request_borrow_item, name="request_borrow_item"),
    path(
        "borrow/request/batch/", views.request_borrow_batch, name="request_borrow_batch"
    ),
    path(
        "borrow/approve/<int:pk>/",
        views.approve_borrow_request,
        name="approve_borrow_request",
    ),
    # QR Code Scanner
    path("qr-scanner/", views.qr_scanner, name="qr_scanner"),
    path("qr-scan/process/", views.process_qr_scan, name="process_qr_scan"),
    path("qr-scan/recent/", views.get_recent_scans, name="get_recent_scans"),
    # Borrowed Items
    path("borrowed-items/", views.borrowed_items_list, name="borrowed_items_list"),
    path(
        "borrowed-items/<int:pk>/",
        views.manage_borrowed_item,
        name="manage_borrowed_item",
    ),
    path(
        "borrowed-items/bulk-delete/",
        views.bulk_delete_borrowed_items,
        name="bulk_delete_borrowed_items",
    ),
    path(
        "borrowed-items/export/csv/",
        views.export_borrowed_items_csv,
        name="export_borrowed_items_csv",
    ),
    path(
        "borrowed-items/export/pdf/",
        views.export_borrowed_items_pdf,
        name="export_borrowed_items_pdf",
    ),
    path(
        "borrowed-items/batch-return/<str:batch_group_id>/",
        views.batch_return_items,
        name="batch_return_items",
    ),
    # Notifications
    path(
        "notifications/mark-all-read/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read",
    ),
    # Reports
    path("reports/", views.reports, name="reports"),
    path(
        "reports/export/supplies/",
        views.export_supplies_csv,
        name="export_supplies_csv",
    ),
    path(
        "reports/export/requests/",
        views.export_requests_csv,
        name="export_requests_csv",
    ),
    path(
        "reports/export/transactions/",
        views.export_transactions_csv,
        name="export_transactions_csv",
    ),
    path(
        "reports/export/supplies/pdf/",
        views.export_supplies_pdf,
        name="export_supplies_pdf",
    ),
    path(
        "reports/export/requests/pdf/",
        views.export_requests_pdf,
        name="export_requests_pdf",
    ),
    path(
        "reports/export/transactions/pdf/",
        views.export_transactions_pdf,
        name="export_transactions_pdf",
    ),
    # User Management
    path("user-management/", views.user_management, name="user_management"),
    path(
        "user-management/approve/<int:user_id>/",
        views.approve_user,
        name="approve_user",
    ),
    path(
        "user-management/toggle/<int:user_id>/",
        views.toggle_user_active,
        name="toggle_user_active",
    ),
    path(
        "user-management/export/csv/",
        views.export_users_csv,
        name="export_users_csv",
    ),
    path(
        "user-management/export/pdf/",
        views.export_users_pdf,
        name="export_users_pdf",
    ),
    # Analytics & Tracking
    path(
        "analytics/requestor-borrower/",
        analytics_views.requestor_borrower_tracking,
        name="requestor_borrower_tracking",
    ),
    path(
        "analytics/user/<int:user_id>/",
        analytics_views.user_analytics_detail,
        name="user_analytics_detail",
    ),
    path(
        "analytics/user/<int:user_id>/modal/",
        analytics_views.user_analytics_modal,
        name="user_analytics_modal",
    ),
    path(
        "analytics/most-requested/",
        analytics_views.most_requested_items,
        name="most_requested_items",
    ),
    path(
        "analytics/export/<int:user_id>/",
        analytics_views.export_user_analytics,
        name="export_user_analytics",
    ),
    # Stock Adjustments (Lost/Damaged Items)
    path(
        "stock-adjustments/",
        stock_adjustment_views.stock_adjustment_list,
        name="stock_adjustment_list",
    ),
    path(
        "stock-adjustments/create/",
        stock_adjustment_views.stock_adjustment_create,
        name="stock_adjustment_create",
    ),
    path(
        "stock-adjustments/<int:pk>/",
        stock_adjustment_views.stock_adjustment_detail,
        name="stock_adjustment_detail",
    ),
]
