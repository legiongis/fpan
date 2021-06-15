from arches.app.datatypes.datatypes import DomainListDataType
from arches.app.models.models import Widget

from hms.models import ManagementArea

widget = Widget.objects.get(name='management-area-widget')

details = {
    'widgetid': '0c298980-cbd9-11e7-b225-aaaa9cf754d0',
    'datatype': 'management-area-datatype',
    'iconclass': 'fa fa-file-code-o',
    'modulename': 'management_area.py',
    'classname': 'ManagementAreaDataType',
    'defaultwidget': widget,
    'defaultconfig': None,
    'configcomponent': None,
    'configname': None,
    'isgeometric': False
    }

class ManagementAreaDataType(DomainListDataType):

    def get_dropdown_options(self):

        return [{
            "id": str(i.pk),
            "selected": "false",
            "text": i.__str__()
        } for i in ManagementArea.objects.all() ]

    def get_option_text(self, node, option_id):

        return ManagementArea.objects.get(pk=option_id).__str__()

    def transform_export_values(self, value, *args, **kwargs):

        if value != None:
            return ManagementArea.objects.get(pk=value).__str__()

    def validate(self, values, row_number=None, source="", node=None, nodeid=None):

        return []