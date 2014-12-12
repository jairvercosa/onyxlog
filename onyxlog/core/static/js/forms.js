/**
 * Objeto para post e validação de formulários
 *
 */
var form = {
    /**
     * Url de destino do post do form
     *
     * @var string urlAction
     */
    urlAction : '',
    /**
     * DOM do formulário da tela
     *
     * @var DOM Element formObject
     */
    formObject: null,
    /**
     * Url que será redirecionado após validação do formulário
     *
     * @var string urlRedirection
     */
    urlRedirection : '',
    /**
     * Button submit
     *
     * @var string btnSubmit
     */
    btnSubmit : '#btnSend',
    /**
     * Button cancel
     *
     * @var string btnCancel
     */
    btnCancel : '#btnCancel',
    /**
     * Indica se formulário foi chamado via ajax
     *
     * @var boolean fromAjax
     */
    fromAjax : '',

    /**
     * Função para execução no carregamento da página
     *
     * @return boolean
     */
    fnOnRead : function(){
        form.formObject = $('form')[0];
        form.urlAction = $(form.formObject).attr('action');
        form.urlRedirection = $(form.formObject).attr('redirect_data');
        $(form.btnSubmit).bind('click',form.fnSubmitForm);
        $(form.btnCancel).bind('click',form.fnOnCancel);
        $('input[behaveas=float]').number(true, 2);
        $('input[behaveas=number]').number(true, 0);
        return true;
    },
    /**
     * Evento de clique do botão de cancelar
     *
     * @return void
     */
    fnOnCancel: function(){
        if(form.urlRedirection == '')
            history.go(-1);
        else
            window.location.href = form.urlRedirection
    },
    /**
     * Retorna os dados do formulário como json
     *
     * @return object
     */
    fnGetDataAsJson : function(){
        var unindexed_array = $(form.formObject).serializeArray();
        var indexed_array = {};
        
        $.map(unindexed_array, function(i, item){
            if(!$(item).hasClass('custom-combobox-input')){ //Ignora campos vindos da customização de combo autocomplete
                //Tratamento para campos multseleção
                if ($('[name='+i['name']+'] :selected').length > 0 && typeof $('[name='+i['name']+']').attr('multiple') != 'undefined'){
                    if(typeof indexed_array[i['name']+'[]'] == 'undefined')
                        indexed_array[i['name']+'[]'] = [];

                    indexed_array[i['name']+'[]'].push(i['value']);
                }else{
                    indexed_array[i['name']] = i['value'];
                }
            }
        });

        return indexed_array;
    },
    /**
     * Submit do formulário via ajax
     *
     * @return boolean
     */
    fnSubmitForm : function(){
        var obj;
        app.addLoading(obj,true);
        $('.error-div-form').remove();
        $('.response_form').hide();
        $.ajax({
            type: 'post',
            url: form.urlAction,
            data: form.fnGetDataAsJson(),
            success: function(response){
                app.removeLoading();
                try{
                    var result = response;
                    form.fnAfterPost(result);
                }catch(err){
                    console.log(err.message+'\n\n'+response);
                    alert(err.message);
                }
            },
            error: function(response){
                app.removeLoading();
                try{
                    var result = $.parseJSON(response.responseText);
                    var objectsForm = $(form.formObject).serializeArray();
                    var focus = false;
                    $.each(objectsForm,function(i, item){
                        var obj = eval('result.'+item.name);
                        if(typeof obj != 'undefined') $('[name='+item.name+']').after('<div class="error-div-form"><small>'+obj[0]+'</small></div>');
                        if(!focus && item.name != 'csrfmiddlewaretoken'){
                            $('[name='+item.name+']').focus();
                            focus = true;
                        }
                    });
                    $('.response_form span').html(result.message);
                    $('.response_form').hide();
                    $('.response_form').removeClass('alert-success');
                    $('.response_form').addClass('alert-danger');
                    $('.response_form').fadeIn('fast');
                    $(document).scrollTop(0);
                    setTimeout(function(){
                        $('.response_form').fadeOut('fast');
                    },5000);

                    form.fnOnError(result);
                }catch(err){
                    console.log(err.message+'\n\n'+response.responseText);
                    alert('Ocorreu uma falha na operação');
                }
            }
        });
        return false;
    },
    /**
     * Função para ser executada após o post do formulário
     *
     * @param json result
     * @return boolean
     */
    fnAfterPost: function(result){
        $('.response_form span').html(result.message);
        $('.response_form').removeClass('alert-danger');
        $('.response_form').addClass('alert-success');
        $('.response_form').fadeIn('fast');
        $(document).scrollTop(0);
        setTimeout(function(){
            form.fnRedirectAfterPost(result);
        },500);
    },
    /**
     * Redirection depois do post
     *
     * @param json result
     * @return void
     */
    fnRedirectAfterPost: function(result){
        if(typeof result.pk == 'undefined')
            window.location.href = form.urlRedirection;
        else
            window.location.href = form.urlRedirection+result.pk+'/';
    },
    /**
     * Função para ser executada em caso de erro
     *
     * @param json result
     * @return boolean
     */
    fnOnError: function(result){
        return true;
    }
}

$(document).ready(form.fnOnRead);