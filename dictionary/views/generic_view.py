"""Base class for dictionary entities."""
from functools import reduce

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import path
from soupsieve.util import lower


class GenericView():
    """Base class for dictionary entities."""
    
    def __init__(self, model_class, form_class, item_view: str, item_edit: str):
        self.model_class = model_class
        self.item_view_template = item_view
        self.item_edit_template = item_edit
        self.form_class = form_class
        self.integrity_error_msg = "There was an error saving your item."
        self.edit_successful_msg = "Item was edited successfully."
        self.add_successful_msg = "Item was added successfully."
    
    # pylint: disable=no-self-use
    def get_success_response(self):
        """Base method for successful edit/add response."""
        return HttpResponse(status=204)
    
    # pylint: disable=no-self-use, unused-argument
    def get_default_formset_dict(self, item, is_adding: bool) -> dict:
        """Base method for entity specific formsets.
                These formset are populated using database .
                You can specific title for formset.
                Each formset has to have unique prefix.
                Return dict so you can access formsets by name in template.
                Example:
                    ret = dict()
                    ret["example"] = self.ExampleFormSet(post, prefix="formset-example")
                    ret["example"].title = "Example formset"
                    return ret
                """
        return dict()
    
    # pylint: disable=no-self-use, unused-argument
    def get_formset_dict(self, post) -> dict:
        """Base method for entity specific formsets.
        These formset are populated using POST. So they handle
        You can specific title for formset.
        Each formset has to have unique prefix.
        Return dict so you can access formsets by name in template.
        Example:
            ret = dict()
            ret["example"] = self.ExampleFormSet(post, prefix="formset-example")
            ret["example"].title = "Example formset"
            return ret
        """
        return dict()
    
    # pylint: disable=no-self-use
    def get_edit_context(self) -> dict:
        """Base method for entity specific context in edit and add.
        You can specify includes into header.
        Example:
            return {
                'header_includes': [
                    "includes/tooltipster.html"
                ]
            }
        """
        return dict()
    
    # pylint: disable=no-self-use
    def get_view_context(self):
        """Base method for entity specific context in view.
        You can specify title and includes into header.
        Example:
            return {
                'title': "Entity",
                'header_includes': [
                    "includes/tooltipster.html"
                ]
            }
        """
        return dict()
    
    # pylint: disable=no-self-use, unused-argument
    def get_data_list(self, search: str) -> list:
        """Base method for list of entities to show in table.
        Returns list of dictionaries containing data you want to use in table.
        Content of search field is propagated here.
        There has to be unique identifier.
        Example:
            return [
                {
                    'pk': entity.pk,
                    'group': entity.group,
                    'name': entity.name,
                } for entity in Entity.objects.filter(name__contains=search)
            ]
        """
        return list()
    
    # pylint: disable=no-self-use
    def get_data_total(self) -> int:
        """Base method for overall count of entities in table without restriction.
        (Should be equal of number of records in DB.)"""
        return 0
    
    # pylint: disable=no-self-use
    def get_table_context(self) -> dict:
        """Base method for entity specific context in table.
        Here should be defined collumns, group collumn number if wanted, title, add_label, etc.
        Each columns has to have at least identifier.
        Also you can disable ordering, etc. Anything you can do in datatables.
        Example:
            Init table for showing name and grouped by group:
            return {
                'columns': [{"data": 'pk', "visible": False},
                             {"data": 'group', "visible": False},
                             {"data": 'name'},
                             ],
                'group_column': 1,
                'title': "Example table",
                'add_label': "Add new record",
            }
        """
        
        return dict()
    
    def generate_edit(self):
        """Generator for edit and add."""

        # pylint: disable=too-many-branches
        @login_required
        def _method(request, primary_key: int = None):
            if primary_key:
                item = get_object_or_404(self.model_class, pk=primary_key)
                is_adding = False
            else:
                item = self.model_class()
                is_adding = True
            
            form_item = self.form_class(request.POST or None, instance=item)
            
            if request.POST:
                formset_dict = self.get_formset_dict(request.POST)
                
                formset_valid = True
                if formset_dict is not None:
                    formset_valid = reduce(
                        lambda x, y: x and y,
                        map(lambda formset: formset.is_valid(), formset_dict.values())
                    )
                
                if form_item.is_valid() and formset_valid:
                    item = form_item.save()
                    
                    save_ok = True
                    if formset_dict is not None:
                        try:
                            for formset in formset_dict.values():
                                formset.save_all(item)
                        except IntegrityError:
                            messages.error(request, self.integrity_error_msg)
                            save_ok = False
                    if save_ok:
                        if is_adding:
                            messages.success(request, self.add_successful_msg)
                        else:
                            messages.success(request, self.edit_successful_msg)
                        return self.get_success_response()
            
            else:
                formset_dict = self.get_default_formset_dict(item, is_adding)
            
            action = "add" if is_adding else "edit"
            context = self.get_edit_context()
            if not is_adding:
                context['pk'] = primary_key
            context['action'] = action
            context['form_item'] = form_item
            context['formset_dict'] = formset_dict
            context['edit_template'] = self.item_edit_template
            
            return render(request, 'generic_base.html', context)
        
        return _method
    
    def generate_view(self):
        """Generator for view."""
        
        @login_required
        def _method(request, primary_key: int):
            context = self.get_view_context()
            context['action'] = "view"
            context['item'] = get_object_or_404(self.model_class, pk=primary_key)
            context['view_template'] = self.item_view_template
            return render(request, 'generic_base.html', context)
        
        return _method
    
    def generate_delete(self):
        """Generator for delete."""
        
        @login_required
        def _method(request, primary_key: int):
            if primary_key:
                item = get_object_or_404(self.model_class, pk=primary_key)
                item.delete()
            return HttpResponse(status=200)
        
        return _method
    
    def generate_list(self):
        """Generator for list GET. In datatables it means initialize."""
        
        def _method(request):
            context = self.get_table_context()
            dummy_item = self.model_class()
            context['dummy_item'] = dummy_item
            model_name_l = lower(self.model_class.__name__)
            context['urls'] = {
                'ajax_url': 'dictionary:' + model_name_l + '_table',
                'delete': 'dictionary:' + model_name_l + '_delete',
                'edit': 'dictionary:' + model_name_l + '_edit',
                'view': 'dictionary:' + model_name_l + '_view',
                'add': 'dictionary:' + model_name_l + '_edit',
            }
            return render(request, 'generic_list.html', context)
        
        return _method
    
    def generate_list_post(self):
        """Generator for list POST. In datatables it means server side ajax endpoint."""
        
        def _method(request):
            datatables = request.POST
            
            # Ambil draw
            draw = int(datatables.get('draw'))
            # Ambil start
            start = int(datatables.get('start'))
            # Ambil length (limit)
            length = int(datatables.get('length'))
            # Ambil data search
            search = datatables.get('search[value]')
            # Ambil order column
            order = datatables.get('order[0][column]')
            order = datatables.get('columns[' + order + '][data]')
            # Ambil order dir
            order_dir = datatables.get('order[0][dir]')
            
            data = self.get_data_list(search)
            
            data.sort(key=lambda x: x[order], reverse=order_dir != "asc")
            data_filtered = len(data)
            del data[:start]
            if length > 0:
                del data[length:]
            
            data_total = self.get_data_total()
            
            return JsonResponse({
                'draw': draw,
                'recordsTotal': data_total,
                'recordsFiltered': data_filtered,
                'data': data,
            })
        
        return _method

    # pylint: disable=line-too-long
    def generate_path(self) -> list:
        """Generate path for urls.
        Create path for table (GET and POST), edit, view and delete of entity.
        """
        model_name_l = lower(self.model_class.__name__)
        return [path(model_name_l + '/', self.generate_list(), name=model_name_l),
                path(model_name_l + '_table/', self.generate_list_post(), name=model_name_l + '_table'),
                path(model_name_l + '/item/', self.generate_edit(), name=model_name_l + '_edit'),
                path(model_name_l + '/item/<int:primary_key>/edit/', self.generate_edit(), name=model_name_l + '_edit'),
                path(model_name_l + '/item/<int:primary_key>/', self.generate_view(), name=model_name_l + '_view'),
                path(model_name_l + '/item/<int:primary_key>/delete/', self.generate_delete(), name=model_name_l + '_delete')]
