# -*- coding: ISO-8859-1 -*-
from django_datatables_view.base_datatable_view import BaseDatatableView

import logging
logging.basicConfig()

class CoreBaseDatatableView(BaseDatatableView):
    use_absolute_url = False
    use_buttons = True
    url_base_form = None

    def render_column(self, row, column):
        """ Renders a column on a row
        """
        if column == 'buttons' and self.url_base_form and self.use_buttons:
            sReturn = '<div class="action-buttons">'
            sReturn +='     <a href="'+self.url_base_form+str(row.id)+'/" title="Editar" class="btnEdit"><i class="glyphicon glyphicon-pencil"></i> </a>'
            sReturn +='     <a href="javascript:;" class="btnDel" alt="'+str(row.id)+'" title="Remover"><i class="glyphicon glyphicon-remove"></i> </a>'
            sReturn +='</div>'
            return sReturn

        if hasattr(row, 'get_%s_display' % column):
            # It's a choice field
            text = getattr(row, 'get_%s_display' % column)()
        else:
            try:
                text = getattr(row, column)
            except AttributeError:
                obj = row
                for part in column.split('.'):
                    if obj is None:
                        break
                    obj = getattr(obj, part)

                text = obj

        if hasattr(row, 'get_absolute_url') and self.use_absolute_url:
            return '<a href="%s">%s</a>' % (row.get_absolute_url(), text)
        else:
            return text