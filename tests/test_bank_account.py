import pytest
from easyverein import EasyvereinAPI
from easyverein.models import BankAccount, BankAccountCreate, BankAccountFilter, BankAccountUpdate


@pytest.fixture(scope="module", autouse=True)
def _remove_test_bank_accounts(ev_connection: EasyvereinAPI):
    yield
    for account in ev_connection.bank_account.get_all(query="{id,name}"):
        if account.name and account.name.lower().startswith("test_"):
            ev_connection.bank_account.delete(account, delete_from_recycle_bin=True)


class TestBankAccount:
    def test_get_bank_accounts(self, ev_connection: EasyvereinAPI):
        accounts, total_count = ev_connection.bank_account.get()

        assert isinstance(accounts, list)
        assert total_count >= len(accounts)
        assert all(isinstance(account, BankAccount) for account in accounts)

    def test_create_get_update_and_filter_bank_account(self, ev_connection: EasyvereinAPI, random_string: str):
        account_model = BankAccountCreate(
            name=random_string,
            short=random_string[-4:],
            color="#112233",
            accountHolder="Test Account Holder",
            bankName="Test Bank",
            IBAN="DE89370400440532013000",
            BIC="COBADEFFXXX",
            sphere=1,
            computeStartsaldoOnImport=False,
        )
        account = ev_connection.bank_account.create(account_model)

        try:
            assert isinstance(account, BankAccount)
            assert account.id is not None

            fetched = ev_connection.bank_account.get_by_id(
                account.id,
                query="{id,name,short,color,accountHolder,bankName,IBAN,BIC,sphere,computeStartsaldoOnImport}",
            )
            assert fetched.id == account.id
            assert fetched.name == account_model.name
            assert fetched.short == account_model.short
            assert fetched.color == account_model.color
            assert fetched.accountHolder == account_model.accountHolder
            assert fetched.bankName == account_model.bankName
            assert fetched.IBAN == account_model.IBAN
            assert fetched.BIC == account_model.BIC
            assert fetched.sphere == account_model.sphere
            assert fetched.computeStartsaldoOnImport == account_model.computeStartsaldoOnImport

            matches, total_count = ev_connection.bank_account.get(search=BankAccountFilter(id__in=[account.id]))
            assert total_count == 1
            assert matches[0].id == account.id

            updated = ev_connection.bank_account.update(
                account.id, BankAccountUpdate(name=f"{random_string}_updated", bankName="Updated Test Bank")
            )
            assert updated.name == f"{random_string}_updated"
            assert updated.bankName == "Updated Test Bank"
            assert updated.short == account_model.short
        finally:
            ev_connection.bank_account.delete(account, delete_from_recycle_bin=True)
