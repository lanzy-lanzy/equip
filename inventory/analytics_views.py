"""
Analytics and Tracking Views for Requestor/Borrower Management
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, Sum, F, Value
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from django.utils import timezone
from datetime import timedelta, datetime
import csv
import json
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

from .models import (
    User,
    Supply,
    SupplyRequest,
    BorrowedItem,
    RequestorBorrowerAnalytics,
    UserActivityLog,
    MostRequestedItem,
)


@login_required
def requestor_borrower_tracking(request):
    """
    Main tracking dashboard for requestors and borrowers - GSO/Admin only
    """
    if request.user.role not in ["admin", "gso_staff"]:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard")

    # Get all users (requestors/borrowers) with real-time annotations
    users_queryset = (
        User.objects.filter(role="department_user")
        .select_related("analytics")
        .annotate(
            unreturned_count=Count(
                "borrowed_items", filter=Q(borrowed_items__returned_at__isnull=True)
            ),
            overdue_count=Count(
                "borrowed_items",
                filter=Q(
                    borrowed_items__returned_at__isnull=True,
                    borrowed_items__return_deadline__lt=timezone.now().date(),
                ),
            ),
        )
        .order_by("username")
    )

    # Calculate summary statistics from annotated queryset
    users_list = list(users_queryset)
    total_users = len(users_list)
    active_borrowers = sum(1 for u in users_list if u.unreturned_count > 0)
    unreturned_items = sum(u.unreturned_count for u in users_list)
    overdue_items = sum(u.overdue_count for u in users_list)

    # Debug output - remove after testing
    print(f"DEBUG: Total users={total_users}, Active borrowers={active_borrowers}")
    for u in users_list[:5]:
        print(
            f"  {u.username}: total_borrowings={u.analytics.total_borrowings if u.analytics else 0}, unreturned={u.unreturned_count}"
        )

    total_requests = SupplyRequest.objects.count()

    context = {
        "users": users_list,
        "total_users": total_users,
        "page_title": "Requestor & Borrower Tracking",
        "active_borrowers": active_borrowers,
        "total_requests": total_requests,
        "overdue_items": overdue_items,
        "unreturned_items": unreturned_items,
    }

    return render(
        request, "inventory/tracking/requestor_borrower_tracking.html", context
    )


@login_required
def user_analytics_detail(request, user_id):
    """
    Detailed analytics for a specific user with filters
    """
    if request.user.role not in ["admin", "gso_staff"]:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard")

    user = get_object_or_404(User, pk=user_id, role="department_user")

    # Get date range filters
    date_filter = request.GET.get(
        "date_filter", "all"
    )  # all, today, week, month, year, custom
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    search = request.GET.get("search", "").strip()

    # Calculate date range
    now = timezone.now()
    if date_filter == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "year":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "custom" and start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = end.replace(hour=23, minute=59, second=59)
            start = timezone.make_aware(start) if timezone.is_naive(start) else start
            end = timezone.make_aware(end) if timezone.is_naive(end) else end
        except:
            start = now - timedelta(days=30)
            end = now
    else:
        start = None
        end = None

    # Get requests
    requests = SupplyRequest.objects.filter(user=user)
    if start and end:
        requests = requests.filter(created_at__gte=start, created_at__lte=end)
    if search:
        requests = requests.filter(
            Q(request_id__icontains=search)
            | Q(supply__name__icontains=search)
            | Q(purpose__icontains=search)
        )
    requests = requests.order_by("-created_at")

    # Get borrowed items
    borrowed_items = BorrowedItem.objects.filter(borrower=user)
    if start and end:
        borrowed_items = borrowed_items.filter(
            borrowed_at__gte=start, borrowed_at__lte=end
        )
    borrowed_items = borrowed_items.order_by("-borrowed_at")

    # Get activity logs
    activity_logs = UserActivityLog.objects.filter(user=user)
    if start and end:
        activity_logs = activity_logs.filter(timestamp__gte=start, timestamp__lte=end)
    activity_logs = activity_logs.order_by("-timestamp")

    # Statistics
    total_requests = requests.count()
    approved_requests = requests.filter(status="approved").count()
    released_requests = requests.filter(status="released").count()
    rejected_requests = requests.filter(status="rejected").count()
    pending_requests = requests.filter(status="pending").count()

    # Calculate approval rate
    if total_requests > 0:
        approval_rate = int(
            (approved_requests + released_requests) / total_requests * 100
        )
    else:
        approval_rate = 0

    total_borrowed = borrowed_items.count()
    returned_items = borrowed_items.filter(returned_at__isnull=False).count()
    unreturned_items = borrowed_items.filter(returned_at__isnull=True).count()
    overdue_items = borrowed_items.filter(
        returned_at__isnull=True, return_deadline__lt=timezone.now().date()
    ).count()

    # Most requested items by this user
    most_requested = (
        requests.values("supply")
        .annotate(count=Count("supply"), supply_name=F("supply__name"))
        .order_by("-count")[:5]
    )

    context = {
        "viewed_user": user,
        "requests": requests,
        "borrowed_items": borrowed_items,
        "activity_logs": activity_logs,
        "date_filter": date_filter,
        "start_date": start_date,
        "end_date": end_date,
        "search": search,
        "total_requests": total_requests,
        "approved_requests": approved_requests,
        "released_requests": released_requests,
        "rejected_requests": rejected_requests,
        "pending_requests": pending_requests,
        "total_borrowed": total_borrowed,
        "returned_items": returned_items,
        "unreturned_items": unreturned_items,
        "overdue_items": overdue_items,
        "most_requested": most_requested,
        "approval_rate": approval_rate,
        "page_title": f"Analytics for {user.username}",
    }

    if request.htmx:
        return render(
            request, "inventory/tracking/partials/analytics_table.html", context
        )

    return render(request, "inventory/tracking/user_analytics_detail.html", context)


@login_required
def user_analytics_modal(request, user_id):
    """
    Returns modal content with user analytics summary and key metrics
    """
    if request.user.role not in ["admin", "gso_staff"]:
        return HttpResponse("Unauthorized", status=403)

    user = get_object_or_404(User, pk=user_id, role="department_user")

    # Get requests
    requests = SupplyRequest.objects.filter(user=user).order_by("-created_at")

    # Get borrowed items
    borrowed_items = BorrowedItem.objects.filter(borrower=user).order_by("-borrowed_at")

    # Statistics
    total_requests = requests.count()
    approved_requests = requests.filter(status="approved").count()
    released_requests = requests.filter(status="released").count()
    rejected_requests = requests.filter(status="rejected").count()
    pending_requests = requests.filter(status="pending").count()

    # Calculate approval rate
    if total_requests > 0:
        approval_rate = int(
            (approved_requests + released_requests) / total_requests * 100
        )
    else:
        approval_rate = 0

    total_borrowed = borrowed_items.count()
    returned_items = borrowed_items.filter(returned_at__isnull=False).count()
    unreturned_items = borrowed_items.filter(returned_at__isnull=True).count()
    overdue_items = borrowed_items.filter(
        returned_at__isnull=True, return_deadline__lt=timezone.now().date()
    ).count()

    # Most requested items by this user
    most_requested = (
        requests.values("supply")
        .annotate(count=Count("supply"), supply_name=F("supply__name"))
        .order_by("-count")[:5]
    )

    context = {
        "viewed_user": user,
        "total_requests": total_requests,
        "approved_requests": approved_requests,
        "released_requests": released_requests,
        "rejected_requests": rejected_requests,
        "pending_requests": pending_requests,
        "total_borrowed": total_borrowed,
        "returned_items": returned_items,
        "unreturned_items": unreturned_items,
        "overdue_items": overdue_items,
        "most_requested": most_requested,
        "approval_rate": approval_rate,
        "recent_requests": requests[:5],
        "recent_borrows": borrowed_items[:5],
    }

    return render(
        request, "inventory/tracking/partials/user_analytics_modal.html", context
    )


@login_required
def most_requested_items(request):
    """
    View for most requested/borrowed items across all users
    """
    if request.user.role not in ["admin", "gso_staff"]:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("dashboard")

    date_filter = request.GET.get("date_filter", "all")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    search = request.GET.get("search", "").strip()

    # Calculate date range
    now = timezone.now()
    if date_filter == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "year":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "custom" and start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = end.replace(hour=23, minute=59, second=59)
            start = timezone.make_aware(start) if timezone.is_naive(start) else start
            end = timezone.make_aware(end) if timezone.is_naive(end) else end
        except:
            start = now - timedelta(days=30)
            end = now
    else:
        start = None
        end = None

    # Get most requested items
    requested_items = SupplyRequest.objects.filter(status__in=["approved", "released"])
    if start and end:
        requested_items = requested_items.filter(
            created_at__gte=start, created_at__lte=end
        )

    request_stats = (
        requested_items.values("supply")
        .annotate(
            request_count=Count("supply"),
            supply_name=F("supply__name"),
            supply_category=F("supply__category__name"),
            supply_quantity=F("supply__quantity"),
            total_quantity_requested=Sum("quantity_requested"),
        )
        .order_by("-request_count")
    )

    # Get most borrowed items
    borrowed_items_qs = BorrowedItem.objects.all()
    if start and end:
        borrowed_items_qs = borrowed_items_qs.filter(
            borrowed_at__gte=start, borrowed_at__lte=end
        )

    borrow_stats = (
        borrowed_items_qs.values("supply")
        .annotate(
            borrow_count=Count("supply"),
            supply_name=F("supply__name"),
            supply_category=F("supply__category__name"),
            total_quantity_borrowed=Sum("borrowed_quantity"),
        )
        .order_by("-borrow_count")
    )

    # Combine stats
    all_supplies = {}
    for item in request_stats:
        supply_id = item["supply"]
        all_supplies[supply_id] = {
            "supply_id": supply_id,
            "name": item["supply_name"],
            "category": item["supply_category"],
            "current_quantity": item["supply_quantity"],
            "request_count": item["request_count"],
            "total_quantity_requested": item["total_quantity_requested"] or 0,
            "borrow_count": 0,
            "total_quantity_borrowed": 0,
        }

    for item in borrow_stats:
        supply_id = item["supply"]
        if supply_id in all_supplies:
            all_supplies[supply_id]["borrow_count"] = item["borrow_count"]
            all_supplies[supply_id]["total_quantity_borrowed"] = (
                item["total_quantity_borrowed"] or 0
            )
        else:
            all_supplies[supply_id] = {
                "supply_id": supply_id,
                "name": item["supply_name"],
                "category": item["supply_category"],
                "current_quantity": 0,
                "request_count": 0,
                "total_quantity_requested": 0,
                "borrow_count": item["borrow_count"],
                "total_quantity_borrowed": item["total_quantity_borrowed"] or 0,
            }

    # Sort by total activity
    sorted_supplies = sorted(
        all_supplies.values(),
        key=lambda x: (x["request_count"] + x["borrow_count"]),
        reverse=True,
    )

    # Apply search filter
    if search:
        sorted_supplies = [
            s
            for s in sorted_supplies
            if search.lower() in s["name"].lower()
            or search.lower() in (s["category"] or "").lower()
        ]

    context = {
        "items": sorted_supplies,
        "date_filter": date_filter,
        "start_date": start_date,
        "end_date": end_date,
        "search": search,
        "page_title": "Most Requested & Borrowed Items",
    }

    if request.htmx:
        return render(
            request, "inventory/tracking/partials/most_requested_table.html", context
        )

    return render(request, "inventory/tracking/most_requested_items.html", context)


@login_required
def export_user_analytics(request, user_id):
    """
    Export user analytics to CSV
    """
    if request.user.role not in ["admin", "gso_staff"]:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    user = get_object_or_404(User, pk=user_id, role="department_user")
    format_type = request.GET.get("format", "csv")  # csv or pdf

    # Get filters from request
    date_filter = request.GET.get("date_filter", "all")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    # Calculate date range
    now = timezone.now()
    if date_filter == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "year":
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif date_filter == "custom" and start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            end = end.replace(hour=23, minute=59, second=59)
            start = timezone.make_aware(start) if timezone.is_naive(start) else start
            end = timezone.make_aware(end) if timezone.is_naive(end) else end
        except:
            start = now - timedelta(days=30)
            end = now
    else:
        start = None
        end = None

    # Get data
    requests = SupplyRequest.objects.filter(user=user)
    borrowed_items = BorrowedItem.objects.filter(borrower=user)

    if start and end:
        requests = requests.filter(created_at__gte=start, created_at__lte=end)
        borrowed_items = borrowed_items.filter(
            borrowed_at__gte=start, borrowed_at__lte=end
        )

    if format_type == "csv":
        return export_analytics_csv(user, requests, borrowed_items, date_filter)
    else:
        return export_analytics_pdf(user, requests, borrowed_items, date_filter)


def export_analytics_csv(user, requests, borrowed_items, date_filter):
    """Export analytics as CSV"""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="analytics_{user.username}_{date_filter}.csv"'
    )

    writer = csv.writer(response)

    # Requests section
    writer.writerow(["SUPPLY REQUESTS"])
    writer.writerow(
        ["Request ID", "Supply", "Quantity", "Status", "Purpose", "Created Date"]
    )

    for req in requests.order_by("-created_at"):
        writer.writerow(
            [
                req.request_id,
                req.supply.name,
                req.quantity_requested,
                req.get_status_display(),
                req.purpose[:50],
                req.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            ]
        )

    writer.writerow([])

    # Borrowed items section
    writer.writerow(["BORROWED ITEMS"])
    writer.writerow(
        [
            "Supply",
            "Quantity",
            "Borrowed Date",
            "Return Deadline",
            "Status",
            "Returned Date",
        ]
    )

    for item in borrowed_items.order_by("-borrowed_at"):
        status = (
            "Returned"
            if item.is_returned
            else ("Overdue" if item.is_overdue else "Active")
        )
        writer.writerow(
            [
                item.supply.name,
                item.borrowed_quantity,
                item.borrowed_date.strftime("%Y-%m-%d"),
                item.return_deadline.strftime("%Y-%m-%d")
                if item.return_deadline
                else "N/A",
                status,
                item.returned_at.strftime("%Y-%m-%d") if item.returned_at else "N/A",
            ]
        )

    writer.writerow([])

    # Summary stats
    writer.writerow(["SUMMARY"])
    writer.writerow(["Metric", "Count"])
    writer.writerow(["Total Requests", requests.count()])
    writer.writerow(["Approved", requests.filter(status="approved").count()])
    writer.writerow(["Released", requests.filter(status="released").count()])
    writer.writerow(["Rejected", requests.filter(status="rejected").count()])
    writer.writerow(["Pending", requests.filter(status="pending").count()])
    writer.writerow(["Total Borrowed Items", borrowed_items.count()])
    writer.writerow(
        ["Returned Items", borrowed_items.filter(returned_at__isnull=False).count()]
    )
    writer.writerow(
        ["Unreturned Items", borrowed_items.filter(returned_at__isnull=True).count()]
    )
    writer.writerow(
        [
            "Overdue Items",
            borrowed_items.filter(
                returned_at__isnull=True, return_deadline__lt=timezone.now().date()
            ).count(),
        ]
    )

    return response


def export_analytics_pdf(user, requests, borrowed_items, date_filter):
    """Export analytics as PDF"""
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="analytics_{user.username}_{date_filter}.pdf"'
    )

    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(letter),
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30,
    )
    elements = []
    styles = getSampleStyleSheet()

    # Add Logos
    import os
    from django.conf import settings

    logo_jh = os.path.join(settings.BASE_DIR, "static", "img", "jh_logo.png")
    logo_it = os.path.join(settings.BASE_DIR, "static", "img", "it_logo.jpg")

    header_row = []

    if os.path.exists(logo_jh):
        im_jh = Image(logo_jh)
        # Calculate aspect ratio from original image dimensions
        original_width = float(im_jh.drawWidth)
        original_height = float(im_jh.drawHeight)
        aspect_ratio = original_width / original_height
        # Set height and calculate width based on aspect ratio
        im_jh.drawHeight = 1.2 * inch
        im_jh.drawWidth = im_jh.drawHeight * aspect_ratio
        header_row.append(im_jh)
    else:
        header_row.append("")

    if os.path.exists(logo_it):
        im_it = Image(logo_it)
        im_it.drawHeight = 1.0 * inch
        im_it.drawWidth = 1.0 * inch  # Make it perfectly round
        header_row.append(im_it)
    else:
        header_row.append("")

    if header_row:
        header_table = Table([header_row], colWidths=[2.0 * inch, 2.0 * inch])
        header_table.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        elements.append(header_table)
        elements.append(Spacer(1, 0.1 * inch))

    # Institution Header Style
    institution_style = ParagraphStyle(
        "InstitutionTitle",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#1B5E20"),  # Dark green
        spaceAfter=0,
        alignment=1,  # Center alignment
        fontName="Helvetica-Bold",
    )

    # Campus Style
    campus_style = ParagraphStyle(
        "CampusTitle",
        parent=styles["Normal"],
        fontSize=13,
        textColor=colors.HexColor("#2E7D32"),  # Medium green
        spaceAfter=5,
        alignment=1,
        fontName="Helvetica-Bold",
    )

    # Add Institution Name
    institution = Paragraph("J.H. CERILLES STATE COLLEGE", institution_style)
    elements.append(institution)

    # Add Campus Location
    campus = Paragraph("Dumingag Campus", campus_style)
    elements.append(campus)

    # Add Separator line
    from reportlab.platypus import Table as RLTable

    separator_style = [("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor("#1B5E20"))]
    separator = RLTable([[""]], colWidths=[7.4 * inch], style=separator_style)
    elements.append(separator)
    elements.append(Spacer(1, 0.15 * inch))

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=14,
        textColor=colors.HexColor("#1B5E20"),
        spaceAfter=12,
        alignment=1,
        fontName="Helvetica-Bold",
    )

    # Title
    elements.append(Paragraph(f"User Analytics Report - {user.username}", title_style))
    elements.append(Spacer(1, 12))

    # Requests table
    elements.append(Paragraph("Supply Requests", styles["Heading2"]))
    request_data = [["Request ID", "Supply", "Qty", "Price", "Total", "Status", "Date"]]
    for req in requests.order_by("-created_at")[:20]:
        total_price = req.quantity_requested * req.supply.cost_per_unit
        request_data.append(
            [
                req.request_id,
                req.supply.name[:30],
                str(req.quantity_requested),
                f"₱{req.supply.cost_per_unit:.2f}",
                f"₱{total_price:.2f}",
                req.get_status_display(),
                req.created_at.strftime("%Y-%m-%d"),
            ]
        )

    request_table = Table(
        request_data,
        colWidths=[
            1.8 * inch,
            2.2 * inch,
            0.7 * inch,
            0.9 * inch,
            0.9 * inch,
            1.1 * inch,
            1.1 * inch,
        ],
    )
    request_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#343131")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F5F5F5")],
                ),
                ("WORDWRAP", (0, 0), (-1, -1), True),
            ]
        )
    )
    elements.append(request_table)
    elements.append(Spacer(1, 12))

    # Borrowed items table
    elements.append(Paragraph("Borrowed Items", styles["Heading2"]))
    borrow_data = [
        ["Supply", "Qty", "Price", "Total Value", "Borrowed", "Return By", "Status"]
    ]
    for item in borrowed_items.order_by("-borrowed_at")[:20]:
        status = (
            "Returned"
            if item.is_returned
            else ("Overdue" if item.is_overdue else "Active")
        )
        total_value = item.borrowed_quantity * item.supply.cost_per_unit
        borrow_data.append(
            [
                item.supply.name[:30],
                str(item.borrowed_quantity),
                f"₱{item.supply.cost_per_unit:.2f}",
                f"₱{total_value:.2f}",
                item.borrowed_date.strftime("%Y-%m-%d"),
                item.return_deadline.strftime("%Y-%m-%d")
                if item.return_deadline
                else "N/A",
                status,
            ]
        )

    borrow_table = Table(
        borrow_data,
        colWidths=[
            2.2 * inch,
            0.7 * inch,
            0.9 * inch,
            0.9 * inch,
            1.1 * inch,
            1.1 * inch,
            1.1 * inch,
        ],
    )
    borrow_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#343131")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#F5F5F5")],
                ),
                ("WORDWRAP", (0, 0), (-1, -1), True),
            ]
        )
    )
    elements.append(borrow_table)

    doc.build(elements)
    return response
