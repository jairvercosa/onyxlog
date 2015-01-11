(function( $ ) {
    $.widget( "custom.comboboxprod", {
        _create: function() {
            this.wrapper = $( "<span>" )
                .addClass( "custom-combobox" )
                .insertAfter( this.element );

            this.element.hide();
            this._createAutocomplete();
            this._createShowAllButton();
        },

        _createAutocomplete: function() {
            var selected = this.element.children( ":selected" ),
                value = selected.val() ? selected.text() : "";

            this.input = $( "<input>" )
                .appendTo( this.wrapper )
                .val( value )
                .attr( "title", "" )
                .addClass( "custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left" )
                .autocomplete({
                    delay: 0,
                    minLength: 0,
                    source: $.proxy( this, "_source" )
                })
                .tooltip({
                    tooltipClass: "ui-state-highlight"
                });

            this._on( this.input, {
                autocompleteselect: function( event, ui ) {
                    var match = false;
                    var opt;
                    $('#id_produto_id').val(ui.item.value);
                    $('#id_produto_id').parent().find('.custom-combobox-input').val(ui.item.label)

                    $('#id_produto_id').find('option').selected = false;
                    opt = $('#id_produto_id').find('option[value='+ui.item.id+']');
                    if(opt.length==0){
                        $('#id_produto_id').append('<option value="'+ui.item.id+'">'+ui.item.label+'</option>');
                        opt = $('#id_produto_id').find('option[value='+ui.item.id+']')
                    }
                    
                    opt[0].selected = true;
                    this._trigger( "select", event, {
                        item: opt
                    });
                },

                autocompletechange: "_removeIfInvalid"
            });
        },

        _createShowAllButton: function() {
            var input = this.input,
                wasOpen = false;

            $( "<a>" )
                .attr( "tabIndex", -1 )
                .attr( "title", "Exibir todos" )
                .tooltip()
                .appendTo( this.wrapper )
                .button({
                    icons: {
                        primary: "ui-icon-triangle-1-s"
                    },
                    text: false
                })
                .removeClass( "ui-corner-all" )
                .addClass( "custom-combobox-toggle ui-corner-right" )
                .mousedown(function() {
                    wasOpen = input.autocomplete( "widget" ).is( ":visible" );
                })
                .click(function() {
                    input.focus();

                    // Close if already visible
                    if ( wasOpen ) {
                        return;
                    }

                    // Pass empty string as value to search for, displaying all results
                    input.autocomplete( "buscar", "" );
                });
        },

        _source: function( request, response ) {
            $.ajax({
                url: '/cadastros/produto/api/fit/',
                dataType: "json",
                data: {
                    term: request.term
                },
                type: "GET",
                success: function(data){
                    if(data.length == 0)
                        return response(["Não foram encontrados produtos para " + request.term]);

                    response( 
                        $.map(data, function(item){
                            return{
                                label: item.desc,
                                value: item.desc,
                                id: item.id
                            };
                        })
                    );
                }
            });


        },

        _removeIfInvalid: function( event, ui ) {

            // Selected an item, nothing to do
            if ( ui.item ) {
                return;
            }

            // Search for a match (case-insensitive)
            var value = this.input.val(),
                valueLowerCase = value.toLowerCase(),
                valid = false;
            this.element.children( "option" ).each(function() {
                if ( $( this ).text().toLowerCase() === valueLowerCase ) {
                    this.selected = valid = true;
                    return false;
                }
            });

            // Found a match, nothing to do
            if ( valid ) {
                return;
            }

            // Remove invalid value
            this.input
                .val( "" )
                .attr( "title", value + " não foi encontrado" )
                .tooltip( "open" );
            this.element.val( "" );
            this._delay(function() {
                this.input.tooltip( "close" ).attr( "title", "" );
            }, 2500 );
            this.input.data( "ui-autocomplete" ).term = "";
        },

        _destroy: function() {
            this.wrapper.remove();
            this.element.show();
        }
    });
})( jQuery );