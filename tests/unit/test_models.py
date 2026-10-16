"""Unit tests for Pydantic model validation (no API connection required)."""

import pytest
from easyverein.models import (
    BankAccount,
    BillingAccount,
    Booking,
    BookingProject,
    ContactDetails,
    ContactDetailsCreate,
    ContactDetailsGroup,
    CustomField,
    CustomFieldCreate,
    CustomFieldSelectOption,
    CustomFieldSelectOptionCreate,
    CustomFieldSelectOptionUpdate,
    CustomFieldUpdate,
    Invoice,
    InvoiceItem,
    InvoiceItemCreate,
    LsbDosbSport,
    Member,
    MemberCreate,
    MemberCustomField,
    MemberGroup,
    MemberMemberGroup,
    MemberUpdate,
)
from easyverein.models.mixins.base import EasyVereinBase
from pydantic import ValidationError


class TestMemberGroupModel:
    """Unit tests for MemberGroup model validation."""

    def test_payment_interval_negative_one(self):
        """Test that paymentInterval accepts -1 for one-time payments."""
        # The EasyVerein API returns -1 for groups with one-time payments (e.g., registration fees)
        member_group = MemberGroup(paymentInterval=-1)
        assert member_group.paymentInterval == -1

    def test_payment_interval_positive(self):
        """Test that paymentInterval accepts positive integers."""
        member_group = MemberGroup(paymentInterval=12)
        assert member_group.paymentInterval == 12

    def test_payment_interval_none(self):
        """Test that paymentInterval accepts None."""
        member_group = MemberGroup(paymentInterval=None)
        assert member_group.paymentInterval is None

    def test_payment_interval_invalid_negative(self):
        """Test that paymentInterval rejects invalid negative values (other than -1)."""
        with pytest.raises(ValidationError):
            MemberGroup(paymentInterval=-2)

    def test_payment_interval_zero_invalid(self):
        """Test that paymentInterval rejects zero."""
        with pytest.raises(ValidationError):
            MemberGroup(paymentInterval=0)


class TestSphere:
    """Unit tests for the SKR 42 sphere values."""

    @pytest.mark.parametrize("sphere", [1, 4, 9, 11, 31, 49])
    def test_valid_spheres(self, sphere: int):
        """Test that main spheres, Sammelposten and sub-spheres are accepted."""
        assert BillingAccount(defaultSphere=sphere).defaultSphere == sphere
        assert Booking(sphere=sphere).sphere == sphere
        assert InvoiceItem(sphere=sphere).sphere == sphere
        assert MemberGroup(sphere=sphere).sphere == sphere

    @pytest.mark.parametrize("sphere", [0, 5, 10, 20, 50])
    def test_invalid_spheres(self, sphere: int):
        """Test that values unknown to the API are rejected."""
        with pytest.raises(ValidationError):
            Booking(sphere=sphere)


@pytest.mark.parametrize(
    ("response", "create", "update", "name"),
    (
        (CustomField, CustomFieldCreate, CustomFieldUpdate, "additional"),
        (CustomField, CustomFieldCreate, CustomFieldUpdate, "placeHolder"),
        (
            CustomFieldSelectOption,
            CustomFieldSelectOptionCreate,
            CustomFieldSelectOptionUpdate,
            "availableForAssignment",
        ),
        (Member, MemberCreate, MemberUpdate, "cancelReason"),
        (Member, MemberCreate, MemberUpdate, "wantsToCancelAt"),
    ),
)
def test_api_generated_fields_are_response_only(response, create, update, name):
    assert name in response.model_fields
    assert name not in create.model_fields
    assert name not in update.model_fields


@pytest.mark.parametrize(
    "response",
    (
        BankAccount,
        Booking,
        BookingProject,
        ContactDetails,
        ContactDetailsGroup,
        CustomField,
        CustomFieldSelectOption,
        InvoiceItem,
        LsbDosbSport,
        Member,
        MemberCustomField,
        MemberGroup,
        MemberMemberGroup,
    ),
)
def test_timestamps_are_response_fields(response):
    assert "created_at" in response.model_fields
    assert "updated_at" in response.model_fields


def test_base_contains_only_identity_fields():
    assert set(EasyVereinBase.model_fields) == {"id", "org"}


@pytest.mark.parametrize(
    ("model", "supports_wastebasket"),
    (
        (BankAccount, True),
        (BillingAccount, True),
        (Booking, True),
        (BookingProject, True),
        (ContactDetails, True),
        (ContactDetailsGroup, True),
        (CustomField, True),
        (Invoice, True),
        (Member, True),
        (MemberGroup, True),
        (CustomFieldSelectOption, False),
        (InvoiceItem, False),
        (LsbDosbSport, False),
        (MemberCustomField, False),
        (MemberMemberGroup, False),
    ),
)
def test_wastebasket_fields_follow_resource_support(model, supports_wastebasket):
    assert {"deleteAfterDate", "deletedBy"}.issubset(model.model_fields) is supports_wastebasket


def test_mixins_preserve_v2_and_v3_wire_names():
    v2 = {
        "id": 17,
        "_deletedBy": "admin",
        "_deleteAfterDate": "2026-10-20T12:30:00",
        "created_at": "2026-10-16T12:30:00",
        "updated_at": "2026-10-17T12:30:00",
    }
    v3 = {
        "id": 17,
        "deleted_by": "admin",
        "delete_after_date": "2026-10-20T12:30:00",
        "created_at": "2026-10-16T12:30:00",
        "updated_at": "2026-10-17T12:30:00",
    }
    for version, payload in (("v2.0", v2), ("v3.0", v3)):
        booking = Booking.model_validate(payload, context={"api_version": version})
        assert booking.deletedBy == "admin"
        assert booking.created_at.isoformat() == "2026-10-16T12:30:00"
        assert booking.model_dump(by_alias=True, exclude_none=True, context={"api_version": version}) == payload


def test_timestamps_stay_out_of_create_models():
    for field in ("created_at", "updated_at"):
        assert field in InvoiceItem.model_fields
        assert field not in InvoiceItemCreate.model_fields


def test_member_matrix_names_on_create_and_update():
    created = MemberCreate(
        contactDetails=123,
        emailOrUserName="example@example.org",
        isMatrixSearchable=True,
        matrixCommunicationPermission=2,
    )
    updated = MemberUpdate(isMatrixSearchable=False, matrixCommunicationPermission=1)
    for model, expected in ((created, (True, 2)), (updated, (False, 1))):
        v2 = model.model_dump(by_alias=True, exclude_none=True, context={"api_version": "v2.0"})
        v3 = model.model_dump(by_alias=True, exclude_none=True, context={"api_version": "v3.0"})
        assert (v2["_isMatrixSearchable"], v2["_matrixCommunicationPermission"]) == expected
        assert (v3["is_matrix_searchable"], v3["matrix_communication_permission"]) == expected


def test_contact_change_requests_stays_a_list_in_v3():
    contact = ContactDetails.model_validate({"change_requests": []}, context={"api_version": "v3.0"})
    assert contact.changeRequests == []
    assert contact.model_dump(by_alias=True, context={"api_version": "v3.0"})["change_requests"] == []


def test_select_option_value_is_required_only_on_create():
    with pytest.raises(ValidationError):
        CustomFieldSelectOptionCreate(maxSelections=3)
    assert CustomFieldSelectOptionUpdate(maxSelections=3).maxSelections == 3


def test_custom_payment_method_is_a_reference():
    contact = ContactDetailsCreate(isCompany=True, customPaymentMethod=123)
    assert contact.model_dump(by_alias=True)["customPaymentMethod"] == 123


def test_removed_fields_are_absent():
    assert "user_importcalendar" not in MemberGroup.model_fields
    for model in (InvoiceItem, LsbDosbSport):
        assert "deleteAfterDate" not in model.model_fields
        assert "deletedBy" not in model.model_fields
        assert "organizationelement_ptr" in model.model_fields
        assert model.wire_name("organizationelement_ptr", "v3.0") is None
