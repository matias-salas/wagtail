from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

from wagtail import __version__, hooks
from wagtail.admin.menu import (
    DismissibleMenuItem,
    DismissibleSubmenuMenuItem,
    MenuItem,
    SubmenuMenuItem,
    help_menu,
    reports_menu,
    settings_menu,
)

from django.utils.translation import gettext_lazy as _

from wagtail.templatetags.wagtailcore_tags import (
    wagtail_feature_release_editor_guide_link,
    wagtail_feature_release_whats_new_link,
)

@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    """Add /static/css/custom.css to the admin."""
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static("css/custom_admin.css")
    )


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/css/custom.js to the admin."""
    return format_html(
        '<script src="{}"></script>',
        static("js/custom_admin.js")
    )





@hooks.register("construct_main_menu")
def hide_help_menu_items(request, menu_items):
    # Itera a través de los elementos del menú principal

    menu_items[:] = [item for item in menu_items if item.name not in ("help", "reports")]
    return menu_items



