import time

from easyverein import EasyvereinAPI
from easyverein.models.member_group import MemberGroup, MemberGroupCreate, MemberGroupUpdate


class TestMembeGropr:
    def test_create_member_group_with_added_fields(self, ev_connection: EasyvereinAPI):
        added_fields = {
            "user_allowICSExport": "a",
            "user_bankData": "d",
            "auto_group_start_date_mode": 1,
            "keepMembershipAfterAgeBasedGroupChange": True,
            "isMatrixSearchable": True,
            "matrixCommunicationPermission": 2,
            "use_automated_matrix_chat": True,
            "orderSequence": 3,
            "participationsPerWeek": 2,
        }
        member_group = ev_connection.member_group.create(
            MemberGroupCreate(name="Test-Group", color="#FF0000", short="TG", **added_fields)
        )
        assert isinstance(member_group, MemberGroup)
        assert member_group.name == "Test-Group"
        assert member_group.color == "#FF0000"
        assert member_group.short == "TG"

        # Check some defaults
        assert member_group.taxRate is None
        assert member_group.usePaymentFormula is False
        assert member_group.user_members_groupaccess == "n"
        assert member_group.id
        fetched = ev_connection.member_group.get_by_id(member_group.id)
        assert {name: getattr(fetched, name) for name in added_fields} == added_fields
        assert "matrix_moderator_ids" in fetched.model_fields_set
        assert "active_linked_items" in fetched.model_fields_set
        assert "linkedItems" in fetched.model_fields_set
        assert fetched.created_at is not None
        assert fetched.updated_at is not None

        # Change the color
        mg = ev_connection.member_group.update(member_group.id, MemberGroupUpdate(color="#00FF00"))
        assert isinstance(mg, MemberGroup)

        # Delete member group again
        ev_connection.member_group.delete(member_group)

        time.sleep(1)

        # Check waste basket
        member_groups, c = ev_connection.member_group.get_deleted()
        assert isinstance(member_groups, list)
        assert len(member_groups) == 1
        assert c == 1
        assert member_groups[0].id == member_group.id

        # Purge member group
        ev_connection.member_group.purge(member_group)

        # Check waste basket
        member_groups, c = ev_connection.member_group.get_deleted()
        assert isinstance(member_groups, list)
        assert len(member_groups) == 0
        assert c == 0
