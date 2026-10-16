::: easyverein.models.mixins.base.EasyVereinBase
    options:
        show_root_heading: false
        heading_level: 2
        show_signature_annotations: true
        show_if_no_docstring: true
        show_category_heading: false
        show_docstring_modules: false
        show_root_toc_entry: false
        members: True

## Optional resource fields

Resources with recycle bin support use `WastebasketMixin`. Responses that expose `created_at` and `updated_at` use
`TimestampsMixin` independently.

::: easyverein.models.mixins.wastebasket.WastebasketMixin
    options:
        show_root_heading: true
        heading_level: 3
        show_bases: false

::: easyverein.models.mixins.timestamps.TimestampsMixin
    options:
        show_root_heading: true
        heading_level: 3
        show_bases: false
