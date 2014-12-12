
/**
 * Objeto application para controle da aplicação de frontend
 */

var app = {
    /**
     * Adiciona o gif de loading
     *
     * @param obj - Classe, Id ou elemento HTML para seleção
     * @param elementWait - Indica se o body vai ficar com status de wating
     * @return bool
     */
    addLoading : function(obj, elementWait){
        if(typeof obj == 'undefined') obj = ".ajaxLoading";
        if(typeof elementWait == 'undefined') elementWait = false;
        
        if(elementWait) $('body').css('cursor','wait');
        $(obj).fadeIn('fast');
        return true;
    },
    /**
     * Remove o gif de loading
     *
     * @param obj - Classe, Id ou elemento HTML para seleção
     * @return bool
     */
    removeLoading : function(obj){
        if(typeof obj == 'undefined') obj = ".ajaxLoading";

        $('body').css('cursor','auto');
        $(obj).fadeOut('fast');
        return true;
    },
    /**
     * Remove todas as marcações de panel de um objeto
     *
     * @param element obj
     * @return bool
     */
    removeClassPanel : function(obj){
        $(obj).removeClass('panel-danger');
        $(obj).removeClass('panel-primary');
        $(obj).removeClass('panel-success');
        $(obj).removeClass('panel-warning');
        $(obj).removeClass('panel-info');
    },
    /**
     * Exibe uma message box para informação
     *
     * @param string text
     * @return bool
     */
    msgboxInfo : function(title,text){
        app.removeClassPanel('#app_msg_box .panel');
        $('#app_msg_box .panel').addClass('panel-info');
        $('#app_msg_box .modal-title').html(title);
        $('#app_msg_box .panel-body').html(text);
        $('#app_msg_box').modal();
    },
    /**
     * Exibe valor em formato real
     *
     * @param int val
     * @return bool
     */
    formatReal: function ( val ){
        var tmp = val+'';
        tmp = tmp.replace(/([0-9]{2})$/g, ",$1");
        if( tmp.length > 6 )
                tmp = tmp.replace(/([0-9]{3}),([0-9]{2}$)/g, ".$1,$2");

        return tmp;
    },
    /**
     * Adiciona um modal carregado via ajax
     *
     * @param string url
     * @param function callback
     * @return void
     */
    addModal: function(url, callback){
        if($('.modalFromAjax').length==0){
            $('body').append(
                '<div class="modal fade modalFromAjax"> \
                    <div class="modal-dialog"> \
                        <div class="modal-content"> \
                            <div class="modal-header"> \
                                <h2>Carregando...</h2> \
                            </div> \
                            <div class="modal-body"> \
                                <span class="ajaxLoadingModal"> \
                                    <img src="/static/img/ajax-loader.gif" /> \
                                </span> \
                            </div> \
                            <div class="modal-footer"> \
                                <button class="btn btn-sm btn-outline btn-default" data-dismiss="modal"><i class="glyphicon glyphicon-remove"></i> Cancelar</button> \
                            </div> \
                        </div> \
                    </div> \
                </div>'
            );
        }

        $('.modalFromAjax').modal();
        app.addLoading($('.ajaxLoadingModal'));
        $.get(url,function(result){
            app.removeLoading($('.ajaxLoadingModal'));
            $('.modalFromAjax .modal-content').html(result);
            if(typeof callback=='function'){
                callback();
            }
        });
    },

    /**
     * @var object datePickerBr - Formatação para datepicker padrão da aplicação
     */
    datePickerBr : {
        dateFormat: 'dd/mm/yy',
        dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
        dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
        dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
        monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
        monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
        nextText: 'Próximo',
        prevText: 'Anterior'
    }

}