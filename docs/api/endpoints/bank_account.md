| API Endpoint   | Namespace                            | Supported Generics |
|----------------|--------------------------------------|--------------------|
| `bank-account` | `evclient.bank_account.<method>`     | CRUD, RecycleBin   |

## Additional parameters

None

## Generic Model Mappings

| Generic Model     | BankAccount Model   |
|-------------------|---------------------|
| `ModelType`       | `BankAccount`       |
| `CreateModelType` | `BankAccountCreate` |
| `UpdateModelType` | `BankAccountUpdate` |

## Additional Methods

::: easyverein.modules.bank_account.BankAccountMixin
    options:
        inherited_members: false
        show_signature: true
        show_signature_annotations: true
        show_root_heading: false
        show_bases: false
        show_root_toc_entry: false
        separate_signature: true
        heading_level: 4
        filters:
            - "!^c$"
            - "!^logger$"
            - "!^endpoint_name"
            - "!^return_type"
            - "!^scope_params"
