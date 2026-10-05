import json
import os
import uuid
from decimal import Decimal, ROUND_HALF_UP

import requests

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from paytmchecksum import PaytmChecksum

from accounts.decorators import allowed_roles

from .forms import FeeCollectionForm, FeeStructureForm
from .models import FeeCollection, FeeStructure


# ============================================================
# PAYTM CONFIGURATION
# ============================================================

PAYTM_MID = os.getenv("PAYTM_MID", "")
PAYTM_MERCHANT_KEY = os.getenv("PAYTM_MERCHANT_KEY", "")

PAYTM_ENVIRONMENT = os.getenv(
    "PAYTM_ENVIRONMENT",
    "staging",
).lower()

PAYTM_WEBSITE_NAME = os.getenv(
    "PAYTM_WEBSITE_NAME",
    "WEBSTAGING",
)

PAYTM_CALLBACK_URL = os.getenv(
    "PAYTM_CALLBACK_URL",
    "",
)


def get_paytm_domain():
    """
    Returns the correct Paytm Payment Gateway domain.

    Staging:
    https://securestage.paytmpayments.com

    Production:
    https://secure.paytmpayments.com
    """

    if PAYTM_ENVIRONMENT == "production":
        return "https://secure.paytmpayments.com"

    return "https://securestage.paytmpayments.com"


# ============================================================
# PAYTM HELPERS
# ============================================================

def normalize_amount(amount):
    """
    Convert amount into Paytm's required two-decimal string.
    Example:
        100 -> "100.00"
        100.5 -> "100.50"
    """

    value = Decimal(str(amount)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )

    return str(value)


def generate_order_id():
    """
    Generates a unique Paytm order ID.

    Paytm order IDs must be unique for every payment attempt.
    """

    return f"FEE_{uuid.uuid4().hex[:20].upper()}"


def get_paytm_callback_url(request):
    """
    Gets callback URL.

    Production/test public URL should preferably be supplied
    through PAYTM_CALLBACK_URL.

    If it is not configured, Django's current request URL is used.
    """

    if PAYTM_CALLBACK_URL:
        return PAYTM_CALLBACK_URL

    return request.build_absolute_uri(
        reverse("fee_payment_callback")
    )


def check_paytm_credentials():
    """
    Make sure Paytm credentials are configured.
    """

    if not PAYTM_MID:
        return False, "PAYTM_MID is not configured."

    if not PAYTM_MERCHANT_KEY:
        return False, "PAYTM_MERCHANT_KEY is not configured."

    return True, ""


# ============================================================
# PAYTM - CHECKOUT PAGE
# ============================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def paytm_checkout(request, student_id, fee_structure_id):

    from academics.models import Student

    student = get_object_or_404(
        Student,
        pk=student_id,
    )

    fee_structure = get_object_or_404(
        FeeStructure,
        pk=fee_structure_id,
    )

    amount = fee_structure.amount

    # --------------------------------------------------------
    # Verify student's class matches fee structure
    # --------------------------------------------------------

    if (
        fee_structure.school_class
        and student.school_class_id
        != fee_structure.school_class_id
    ):
        messages.error(
            request,
            "The selected fee structure does not belong to the student's class.",
        )

        return redirect(
            "fee_collection_list",
        )

    # --------------------------------------------------------
    # Check amount
    # --------------------------------------------------------

    if amount <= 0:

        messages.error(
            request,
            "Fee amount must be greater than zero.",
        )

        return redirect(
            "fee_collection_list",
        )

    # --------------------------------------------------------
    # Render Paytm checkout
    # --------------------------------------------------------

    return render(
        request,
        "fees/paytm_checkout.html",
        {
            "student": student,
            "fee_structure": fee_structure,
            "amount": normalize_amount(amount),
            "mid": PAYTM_MID,
        },
    )

# ============================================================
# PAYTM - CREATE TRANSACTION
# ============================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def paytm_payment_create(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "POST request required.",
            },
            status=405,
        )

    # --------------------------------------------------------
    # Check credentials
    # --------------------------------------------------------

    credentials_ok, credential_message = check_paytm_credentials()

    if not credentials_ok:
        return JsonResponse(
            {
                "success": False,
                "message": credential_message,
            },
            status=500,
        )

    # --------------------------------------------------------
    # Get submitted values
    # --------------------------------------------------------

    student_id = request.POST.get("student_id")
    fee_structure_id = request.POST.get("fee_structure_id")
    amount = request.POST.get("amount")

    if not student_id:
        return JsonResponse(
            {
                "success": False,
                "message": "Student is required.",
            },
            status=400,
        )

    if not fee_structure_id:
        return JsonResponse(
            {
                "success": False,
                "message": "Fee structure is required.",
            },
            status=400,
        )

    if not amount:
        return JsonResponse(
            {
                "success": False,
                "message": "Amount is required.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # Get student and fee structure
    # --------------------------------------------------------

    student = get_object_or_404(
        __import__(
            "academics.models",
            fromlist=["Student"],
        ).Student,
        pk=student_id,
    )

    fee_structure = get_object_or_404(
        FeeStructure,
        pk=fee_structure_id,
    )

    # --------------------------------------------------------
    # Validate amount
    # --------------------------------------------------------

    try:
        payment_amount = Decimal(str(amount))
    except Exception:
        return JsonResponse(
            {
                "success": False,
                "message": "Invalid payment amount.",
            },
            status=400,
        )

    if payment_amount <= 0:
        return JsonResponse(
            {
                "success": False,
                "message": "Payment amount must be greater than zero.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # Verify class
    # --------------------------------------------------------

    if (
        fee_structure.school_class
        and student.school_class_id
        != fee_structure.school_class_id
    ):
        return JsonResponse(
            {
                "success": False,
                "message": (
                    "The selected fee structure does not "
                    "belong to the student's class."
                ),
            },
            status=400,
        )

    # --------------------------------------------------------
    # Generate unique order ID
    # --------------------------------------------------------

    order_id = generate_order_id()

    # --------------------------------------------------------
    # Customer ID
    # --------------------------------------------------------

    customer_id = f"STUDENT_{student.id}"

    # --------------------------------------------------------
    # Customer information
    # --------------------------------------------------------

    user_info = {
        "custId": customer_id,
    }

    if student.phone:
        user_info["mobile"] = student.phone

    if student.email:
        user_info["email"] = student.email

    # --------------------------------------------------------
    # Paytm transaction body
    # --------------------------------------------------------

    body = {
        "requestType": "Payment",
        "mid": PAYTM_MID,
        "websiteName": PAYTM_WEBSITE_NAME,
        "orderId": order_id,
        "callbackUrl": get_paytm_callback_url(request),
        "txnAmount": {
            "value": normalize_amount(payment_amount),
            "currency": "INR",
        },
        "userInfo": user_info,
    }

    # --------------------------------------------------------
    # Generate checksum
    # --------------------------------------------------------

    body_json = json.dumps(body)

    signature = PaytmChecksum.generateSignature(
        body_json,
        PAYTM_MERCHANT_KEY,
    )

    payload = {
        "head": {
            "signature": signature,
        },
        "body": body,
    }

    # --------------------------------------------------------
    # Paytm API URL
    # --------------------------------------------------------

    paytm_url = (
        f"{get_paytm_domain()}"
        f"/theia/api/v1/initiateTransaction"
        f"?mid={PAYTM_MID}"
        f"&orderId={order_id}"
    )

    # --------------------------------------------------------
    # Call Paytm
    # --------------------------------------------------------

    try:

        response = requests.post(
            paytm_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
            },
            timeout=20,
        )

    except requests.RequestException as exc:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Unable to connect to Paytm Payment Gateway."
                ),
                "error": str(exc),
            },
            status=502,
        )

    # --------------------------------------------------------
    # Parse Paytm response
    # --------------------------------------------------------

    try:

        response_data = response.json()

    except ValueError:

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid response received from Paytm.",
            },
            status=502,
        )

    # --------------------------------------------------------
    # Check Paytm response
    # --------------------------------------------------------

    response_body = response_data.get(
        "body",
        {},
    )

    result_info = response_body.get(
        "resultInfo",
        {},
    )

    result_status = result_info.get(
        "resultStatus",
    )

    if response.status_code != 200:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    result_info.get(
                        "resultMsg",
                    )
                    or "Paytm transaction initiation failed."
                ),
                "order_id": order_id,
            },
            status=502,
        )

    if result_status != "S":

        return JsonResponse(
            {
                "success": False,
                "message": (
                    result_info.get(
                        "resultMsg",
                    )
                    or "Unable to initiate Paytm payment."
                ),
                "order_id": order_id,
                "result_code": result_info.get(
                    "resultCode",
                ),
            },
            status=400,
        )

    # --------------------------------------------------------
    # Get transaction token
    # --------------------------------------------------------

    txn_token = response_body.get(
        "txnToken",
    )

    if not txn_token:

        return JsonResponse(
            {
                "success": False,
                "message": (
                    "Paytm did not return a transaction token."
                ),
                "order_id": order_id,
            },
            status=502,
        )

    # --------------------------------------------------------
    # Return checkout data to frontend
    # --------------------------------------------------------

    return JsonResponse(
        {
            "success": True,
            "orderId": order_id,
            "txnToken": txn_token,
            "amount": normalize_amount(
                payment_amount,
            ),
            "mid": PAYTM_MID,
            "tokenType": "TXN_TOKEN",
        }
    )


# ============================================================
# PAYTM - CALLBACK
# ============================================================

@csrf_exempt
def fee_payment_callback(request):

    # --------------------------------------------------------
    # Read callback data
    # --------------------------------------------------------

    if request.method == "POST":

        callback_data = request.POST.dict()

    else:

        callback_data = request.GET.dict()

    if not callback_data:

        return JsonResponse(
            {
                "success": False,
                "message": "Empty Paytm callback.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # Get checksum
    # --------------------------------------------------------

    checksum = callback_data.get(
        "CHECKSUMHASH",
    )

    if not checksum:

        return JsonResponse(
            {
                "success": False,
                "message": "Paytm checksum missing.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # Verify checksum
    # --------------------------------------------------------

    verification_data = {
        key: value
        for key, value in callback_data.items()
        if key != "CHECKSUMHASH"
    }

    try:

        checksum_valid = PaytmChecksum.verifySignature(
            verification_data,
            PAYTM_MERCHANT_KEY,
            checksum,
        )

    except Exception:

        checksum_valid = False

    if not checksum_valid:

        return JsonResponse(
            {
                "success": False,
                "message": "Invalid Paytm callback checksum.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # Get order ID
    # --------------------------------------------------------

    order_id = callback_data.get(
        "ORDERID",
    )

    if not order_id:

        return JsonResponse(
            {
                "success": False,
                "message": "Order ID missing.",
            },
            status=400,
        )

    # --------------------------------------------------------
    # Verify transaction directly with Paytm
    # --------------------------------------------------------

    status_result = verify_paytm_order(
        order_id,
    )

    if not status_result["success"]:

        return JsonResponse(
            {
                "success": False,
                "message": status_result["message"],
            },
            status=502,
        )

    paytm_body = status_result["body"]

    result_info = paytm_body.get(
        "resultInfo",
        {},
    )

    transaction_status = result_info.get(
        "resultStatus",
    )

    transaction_data = paytm_body.get(
        "resultInfo",
        {},
    )

    # Paytm's order status response can contain these fields
    # directly inside body/resultInfo depending on API response.

    status_value = (
        paytm_body.get("resultInfo", {}).get("resultStatus")
        or paytm_body.get("STATUS")
    )

    # --------------------------------------------------------
    # Get transaction fields
    # --------------------------------------------------------

    txn_id = (
        paytm_body.get("txnId")
        or paytm_body.get("TXNID")
    )

    txn_amount = (
        paytm_body.get("txnAmount")
        or paytm_body.get("TXNAMOUNT")
    )

    payment_mode = (
        paytm_body.get("paymentMode")
        or paytm_body.get("PAYMENTMODE")
        or "UPI"
    )

    # --------------------------------------------------------
    # Find existing fee record by order ID
    # --------------------------------------------------------

    collection = FeeCollection.objects.filter(
        order_id=order_id,
    ).first()

    # --------------------------------------------------------
    # Successful payment
    # --------------------------------------------------------

    if status_value == "TXN_SUCCESS":

        if collection:

            collection.payment_status = "SUCCESS"

            if txn_id:
                collection.transaction_id = txn_id

            collection.gateway_name = "Paytm"

            collection.gateway_response = paytm_body

            collection.payment_date = timezone.localdate()

            collection.save(
                update_fields=[
                    "payment_status",
                    "transaction_id",
                    "gateway_name",
                    "gateway_response",
                    "payment_date",
                ]
            )

        return redirect(
            "fee_collection_list",
        )

    # --------------------------------------------------------
    # Pending payment
    # --------------------------------------------------------

    if status_value == "PENDING":

        if collection:

            collection.payment_status = "PENDING"

            collection.gateway_name = "Paytm"

            collection.gateway_response = paytm_body

            collection.save(
                update_fields=[
                    "payment_status",
                    "gateway_name",
                    "gateway_response",
                ]
            )

        return redirect(
            "fee_collection_list",
        )

    # --------------------------------------------------------
    # Failed payment
    # --------------------------------------------------------

    if collection:

        collection.payment_status = "FAILED"

        collection.gateway_name = "Paytm"

        collection.gateway_response = paytm_body

        if txn_id:
            collection.transaction_id = txn_id

        collection.save(
            update_fields=[
                "payment_status",
                "gateway_name",
                "gateway_response",
                "transaction_id",
            ]
        )

    return redirect(
        "fee_collection_list",
    )


# ============================================================
# PAYTM - ORDER STATUS VERIFICATION
# ============================================================

def verify_paytm_order(order_id):

    if not PAYTM_MID:

        return {
            "success": False,
            "message": "PAYTM_MID is not configured.",
        }

    if not PAYTM_MERCHANT_KEY:

        return {
            "success": False,
            "message": "PAYTM_MERCHANT_KEY is not configured.",
        }

    body = {
        "mid": PAYTM_MID,
        "orderId": order_id,
    }

    body_json = json.dumps(body)

    signature = PaytmChecksum.generateSignature(
        body_json,
        PAYTM_MERCHANT_KEY,
    )

    payload = {
        "head": {
            "signature": signature,
        },
        "body": body,
    }

    status_url = (
        f"{get_paytm_domain()}"
        f"/v3/order/status"
    )

    try:

        response = requests.post(
            status_url,
            json=payload,
            headers={
                "Content-Type": "application/json",
            },
            timeout=20,
        )

    except requests.RequestException as exc:

        return {
            "success": False,
            "message": (
                "Unable to connect to Paytm "
                "Transaction Status API."
            ),
            "error": str(exc),
        }

    try:

        response_data = response.json()

    except ValueError:

        return {
            "success": False,
            "message": (
                "Invalid response from Paytm "
                "Transaction Status API."
            ),
        }

    if response.status_code != 200:

        return {
            "success": False,
            "message": (
                "Paytm Transaction Status API failed."
            ),
            "body": response_data,
        }

    return {
        "success": True,
        "body": response_data.get(
            "body",
            {},
        ),
    }


# ============================================================
# PAYTM - MANUAL STATUS CHECK
# ============================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def paytm_payment_status(request, order_id):

    result = verify_paytm_order(
        order_id,
    )

    if not result["success"]:

        return JsonResponse(
            result,
            status=502,
        )

    body = result["body"]

    result_info = body.get(
        "resultInfo",
        {},
    )

    status = result_info.get(
        "resultStatus",
    )

    transaction_id = (
        body.get("txnId")
        or body.get("TXNID")
    )

    # --------------------------------------------------------
    # Find collection
    # --------------------------------------------------------

    collection = FeeCollection.objects.filter(
        order_id=order_id,
    ).first()

    if collection:

        if status == "TXN_SUCCESS":

            collection.payment_status = "SUCCESS"

        elif status == "PENDING":

            collection.payment_status = "PENDING"

        else:

            collection.payment_status = "FAILED"

        if transaction_id:

            collection.transaction_id = transaction_id

        collection.gateway_name = "Paytm"

        collection.gateway_response = body

        collection.save(
            update_fields=[
                "payment_status",
                "transaction_id",
                "gateway_name",
                "gateway_response",
            ]
        )

    return JsonResponse(
        {
            "success": True,
            "order_id": order_id,
            "status": status,
            "transaction_id": transaction_id,
            "response": body,
        }
    )


# ==========================================================
# Fee Structure
# ==========================================================

@login_required
@allowed_roles("Admin", "Principal")
def fee_structure_list(request):

    fee_structures = FeeStructure.objects.select_related(
        "school_class"
    ).all()

    search = request.GET.get(
        "search",
        "",
    )

    if search:

        fee_structures = fee_structures.filter(
            Q(
                fee_type__icontains=search
            )
            | Q(
                school_class__name__icontains=search
            )
        )

    paginator = Paginator(
        fee_structures,
        10,
    )

    page = request.GET.get(
        "page",
    )

    page_obj = paginator.get_page(
        page,
    )

    context = {
        "page_obj": page_obj,
        "fee_structures": page_obj,
        "search": search,
    }

    return render(
        request,
        "fees/fee_structure_list.html",
        context,
    )


@login_required
@allowed_roles("Admin", "Principal")
def fee_structure_create(request):

    if request.method == "POST":

        form = FeeStructureForm(
            request.POST,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee Structure added successfully.",
            )

            return redirect(
                "fee_structure_list",
            )

    else:

        form = FeeStructureForm()

    return render(
        request,
        "fees/fee_structure_form.html",
        {
            "form": form,
            "title": "Add Fee Structure",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def fee_structure_update(request, pk):

    fee_structure = get_object_or_404(
        FeeStructure,
        pk=pk,
    )

    if request.method == "POST":

        form = FeeStructureForm(
            request.POST,
            instance=fee_structure,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee Structure updated successfully.",
            )

            return redirect(
                "fee_structure_list",
            )

    else:

        form = FeeStructureForm(
            instance=fee_structure,
        )

    return render(
        request,
        "fees/fee_structure_form.html",
        {
            "form": form,
            "title": "Edit Fee Structure",
        },
    )


@login_required
@allowed_roles("Admin", "Principal")
def fee_structure_delete(request, pk):

    fee_structure = get_object_or_404(
        FeeStructure,
        pk=pk,
    )

    if request.method == "POST":

        fee_structure.delete()

        messages.success(
            request,
            "Fee Structure deleted successfully.",
        )

        return redirect(
            "fee_structure_list",
        )

    return render(
        request,
        "fees/fee_structure_delete.html",
        {
            "fee_structure": fee_structure,
        },
    )


# ==========================================================
# Fee Collection
# ==========================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def fee_collection_list(request):

    collections = FeeCollection.objects.select_related(
        "student",
        "fee_structure",
    ).all()

    search = request.GET.get(
        "search",
        "",
    )

    if search:

        collections = collections.filter(
            Q(
                receipt_number__icontains=search
            )
            | Q(
                student__first_name__icontains=search
            )
            | Q(
                student__last_name__icontains=search
            )
            | Q(
                order_id__icontains=search
            )
            | Q(
                transaction_id__icontains=search
            )
        )

    paginator = Paginator(
        collections,
        10,
    )

    page = request.GET.get(
        "page",
    )

    page_obj = paginator.get_page(
        page,
    )

    return render(
        request,
        "fees/fee_collection_list.html",
        {
            "collections": page_obj,
            "page_obj": page_obj,
            "search": search,
        },
    )


# ==========================================================
# Manual Fee Collection
# ==========================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def fee_collection_create(request):

    if request.method == "POST":

        form = FeeCollectionForm(
            request.POST,
        )

        if form.is_valid():

            collection = form.save(
                commit=False,
            )

            collection.payment_status = "SUCCESS"

            collection.save()

            messages.success(
                request,
                "Fee collected successfully.",
            )

            return redirect(
                "fee_collection_list",
            )

    else:

        form = FeeCollectionForm()

    return render(
        request,
        "fees/fee_collection_form.html",
        {
            "form": form,
            "title": "Collect Fee",
        },
    )


# ==========================================================
# Fee Collection Update
# ==========================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def fee_collection_update(request, pk):

    collection = get_object_or_404(
        FeeCollection,
        pk=pk,
    )

    if request.method == "POST":

        form = FeeCollectionForm(
            request.POST,
            instance=collection,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee updated successfully.",
            )

            return redirect(
                "fee_collection_list",
            )

    else:

        form = FeeCollectionForm(
            instance=collection,
        )

    return render(
        request,
        "fees/fee_collection_form.html",
        {
            "form": form,
            "title": "Edit Fee",
        },
    )


# ==========================================================
# Fee Collection Delete
# ==========================================================

@login_required
@allowed_roles("Admin", "Principal", "Accountant")
def fee_collection_delete(request, pk):

    collection = get_object_or_404(
        FeeCollection,
        pk=pk,
    )

    if request.method == "POST":

        collection.delete()

        messages.success(
            request,
            "Fee record deleted successfully.",
        )

        return redirect(
            "fee_collection_list",
        )

    return render(
        request,
        "fees/fee_collection_delete.html",
        {
            "collection": collection,
        },
    )