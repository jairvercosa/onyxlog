/**
 * objeto para controle do grid
 *
 */
var grid = {
    /**
     * Url para pegar os dados do grid
     *
     * @var string urlData
     */
    urlData : '',
    /**
     * Url para deletar um registro
     *
     * @var string urlDel
     */
    urlDel : '',
    /**
     * id Atual que está sendo manupulado
     *
     * @var string currId
     */
    currId : '',
    /**
     * id do elemento da caixa de mensagem
     *
     * @var string msgElementId
     */
    msgElementId : '#mdlMsg_TSM',
    /**
     * token para post do delete
     *
     * @var string urlDel
     */
    csrfToken : '',
    /**
     * Objeto do datatable
     *
     * @var datatable obj
     */
    obj : null,
    /**
     * id da table do grid
     *
     * @var string tableObj
     */
    tableObj : '',
    /**
     * Função para retornar colunas não ordenáveis
     *
     * @return Array
     */
    fnGetDontSort : function(){
        var dontSort = [];
        $(grid.tableObj+' thead th').each( function () {
            if ( $(this).hasClass( 'no_sort' )) {
                dontSort.push( { "bSortable": false } );
            } else {
                dontSort.push( null );
            }
        });
        return dontSort;
    },
    /**
     * Função para click do botão excluir
     *
     * @return boolean
     */
    fnOnClickDel: function(typeCall){
        if(typeof typeCall == 'undefined') typeCall = 0;

        switch(typeCall){
            case 1:
                  var url_del = grid.urlDel + grid.currId;
                $.ajax({
                    type: 'post',
                    data: {'csrfmiddlewaretoken': grid.csrfToken },
                    url: url_del,
                    success: function(response){
                        grid.obj.fnDraw();
                        grid.fnOnClickDel(2);
                    },
                    error: function(response){
                        var result = $.parseJSON(response.responseText);

                        if(typeof result.message == 'undefined'){
                            alert('Infelizmente ocorreu um problema na tentativa de exclusão. Por favor entre em contato com o administrador do sistema');
                            console.log(response);
                        }else{
                            $(grid.msgElementId).modal('hide')
                            app.msgboxInfo('Acesso negado',result.message);
                        }
                    }
                });        
                  break;
            case 2:
                  $(grid.msgElementId).modal('hide')
                  break;
        default:
            grid.currId = $(this).attr('alt')+'/';
            $(grid.msgElementId).modal();
        }
    },
    /**
     * Função para instanciar o objeto
     *
     * @return boolean
     */
    fnStartObject : function(option){
        var dontSort = grid.fnGetDontSort();
        grid.urlData = option.urlData;
        grid.urlDel = option.urlDel;
        grid.tableObj = option.tableObj;

        if(typeof option.aaSorting == 'undefined')
            option.aaSorting = [[0,""]]

        if(typeof option.fnCreatedRow == 'undefined')
            option.fnCreatedRow = function(){ return true; }

        if(typeof option.fnDrawCallback == 'undefined'){
            option.fnDrawCallback = function(oSettings){
                $(oSettings.nTable).find('tr').addClass('tr-selectable');
                $('.tr-selectable').bind('dblclick',grid.onDblClick);
            }
        }

        if(typeof option.fnServerParams == 'undefined')
            option.fnServerParams = function(){return true;}

        if(typeof option.fnFooterCallback == 'undefined')
            option.fnFooterCallback = null;
        

        var optionsDataTable = {
            "aoColumns": dontSort,
            "bProcessing": true,
            "bServerSide": true,
            "sAjaxSource": grid.urlData,
            "oLanguage": {
                "oPaginate" : {
                    "sFirst" : "<<",
                    "sLast" : ">>",
                    "sPrevious" : "<",
                    "sNext" : ">",
                },
                "sProcessing" : "Processando",
                "sSearch": "Pesquisar",
                "sLengthMenu": "_MENU_ registros por página",
                "sZeroRecords": "Nenhum registro encontrado",
                "sInfo": "Exibindo _START_ até _END_ de _TOTAL_ registros",
                "sInfoEmpty": "Exibindo 0 até 0 de 0 registros",
                "sInfoFiltered": "(Filtrado de _MAX_ total registros)"
            },
            "sDom": "<'row'<'col-lg-6 col-xs-5'l><'col-lg-6'<'pull-right'f>>r><'row'<'col-lg-12't>><'row'<'col-lg-6 col-xs-4'i><'col-lg-6'p>>",
            "sPaginationType": "full_numbers",
            "aaSorting": option.aaSorting,
            "fnCreatedRow": option.fnCreatedRow,
            "fnDrawCallback": option.fnDrawCallback,
            "fnServerParams": option.fnServerParams,
            "fnFooterCallback": option.fnFooterCallback,
            "bDestroy": true
        }

        grid.obj = $(grid.tableObj).dataTable(optionsDataTable);

        $('.dataTables_wrapper input').addClass('form-control');
        $('.dataTables_wrapper select').addClass('form-control');
        
        grid.csrfToken = $('input[name=csrfmiddlewaretoken]').val();
        $('.btnDel').live('click',grid.fnOnClickDel);
        
        $('#btnConfirmDel').bind('click',function(){
            grid.fnOnClickDel(1);
        });

        $.extend( $.fn.dataTableExt.oStdClasses, {
            "sWrapper": "dataTables_wrapper form-inline"
        });
    },

    /**
     * Evento de duplo clique da linha do grid
     *
     * @return void
     */
    onDblClick: function() {
        if($(this).find('.btnEdit').length > 0)
            window.location = $(this).find('.btnEdit').attr('href');
    }
}

/*
 * Ajuste para paginação
 */
if ( $.fn.dataTable.Api ) {
    $.fn.dataTable.defaults.renderer = 'bootstrap';
    $.fn.dataTable.ext.renderer.pageButton.bootstrap = function ( settings, host, idx, buttons, page, pages ) {
        var api = new $.fn.dataTable.Api( settings );
        var classes = settings.oClasses;
        var lang = settings.oLanguage.oPaginate;
        var btnDisplay, btnClass;

        var attach = function( container, buttons ) {
            var i, ien, node, button;
            var clickHandler = function ( e ) {
                e.preventDefault();
                if ( e.data.action !== 'ellipsis' ) {
                    api.page( e.data.action ).draw( false );
                }
            };

            for ( i=0, ien=buttons.length ; i<ien ; i++ ) {
                button = buttons[i];

                if ( $.isArray( button ) ) {
                    attach( container, button );
                }
                else {
                    btnDisplay = '';
                    btnClass = '';

                    switch ( button ) {
                        case 'ellipsis':
                            btnDisplay = '&hellip;';
                            btnClass = 'disabled';
                            break;

                        case 'first':
                            btnDisplay = lang.sFirst;
                            btnClass = button + (page > 0 ?
                                '' : ' disabled');
                            break;

                        case 'previous':
                            btnDisplay = lang.sPrevious;
                            btnClass = button + (page > 0 ?
                                '' : ' disabled');
                            break;

                        case 'next':
                            btnDisplay = lang.sNext;
                            btnClass = button + (page < pages-1 ?
                                '' : ' disabled');
                            break;

                        case 'last':
                            btnDisplay = lang.sLast;
                            btnClass = button + (page < pages-1 ?
                                '' : ' disabled');
                            break;

                        default:
                            btnDisplay = button + 1;
                            btnClass = page === button ?
                                'active' : '';
                            break;
                    }

                    if ( btnDisplay ) {
                        node = $('<li>', {
                                'class': classes.sPageButton+' '+btnClass,
                                'aria-controls': settings.sTableId,
                                'tabindex': settings.iTabIndex,
                                'id': idx === 0 && typeof button === 'string' ?
                                    settings.sTableId +'_'+ button :
                                    null
                            } )
                            .append( $('<a>', {
                                    'href': '#'
                                } )
                                .html( btnDisplay )
                            )
                            .appendTo( container );

                        settings.oApi._fnBindAction(
                            node, {action: button}, clickHandler
                        );
                    }
                }
            }
        };

        attach(
            $(host).empty().html('<ul class="pagination"/>').children('ul'),
            buttons
        );
    }
}