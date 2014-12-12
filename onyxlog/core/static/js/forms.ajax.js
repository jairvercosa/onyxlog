/**
 * Objeto para post e validação de formulários
 *
 */
var formAjax = {
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
    btnSubmit : '#btnSendAjax',
    

    /**
     * Função para execução no carregamento da página
     *
     * @return boolean
     */
    fnOnRead : function(){
        formAjax.formObject = $('.formAjaxContent form')[0];
        formAjax.urlAction = $(formAjax.formObject).attr('action');
        formAjax.urlRedirection = $(formAjax.formObject).attr('redirect_data');
        $(formAjax.btnSubmit).bind('click',formAjax.fnSubmitForm);
        $('input[behaveas=float]').number(true, 2);
        $('input[behaveas=number]').number(true, 0);
        return true;
    },
    /**
     * Retorna os dados do formulário como json
     *
     * @return object
     */
    fnGetDataAsJson : function(){
        var unindexed_array = $(formAjax.formObject).serializeArray();
        var indexed_array = {};
        
        $.map(unindexed_array, function(i, item){
            //Tratamento para campos multseleção
            if ($('[name='+i['name']+'] :selected').length > 0 && typeof $('[name='+i['name']+']').attr('multiple') != 'undefined'){
                if(typeof indexed_array[i['name']+'[]'] == 'undefined')
                    indexed_array[i['name']+'[]'] = [];

                indexed_array[i['name']+'[]'].push(i['value']);
            }else{
                indexed_array[i['name']] = i['value'];
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
            url: formAjax.urlAction,
            data: formAjax.fnGetDataAsJson(),
            success: function(response){
                app.removeLoading();
                try{
                    var result = response;
                    formAjax.fnAfterPost(result);
                }catch(err){
                    console.log(err.message+'\n\n'+response);
                    alert(err.message);
                }
            },
            error: function(response){
                app.removeLoading();
                try{
                    console.log('Erros');
                    var result = $.parseJSON(response.responseText);
                    var objectsForm = $(formAjax.formObject).serializeArray();
                    var focus = false;
                    $.each(objectsForm,function(i, item){
                        var obj = eval('result.'+item.name);
                        if(typeof obj != 'undefined') $('[name='+item.name+']').after('<div class="error-div-form"><small>'+obj[0]+'</small></div>');
                        if(!focus && item.name != 'csrfmiddlewaretoken'){
                            $('[name='+item.name+']').focus();
                            focus = true;
                        }

                        console.log(item.name+': '+obj[0]);
                    });
                    $('.response_form span').html(result.message);
                    $('.response_form').hide();
                    $('.response_form').removeClass('alert-success');
                    $('.response_form').addClass('alert-danger');
                    $('.response_form').fadeIn('fast');
                    setTimeout(function(){
                        $('.response_form').fadeOut('fast');
                    },5000);
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
            if(typeof result.pk == 'undefined')
                window.location.href = formAjax.urlRedirection;
            else
                window.location.href = formAjax.urlRedirection+result.pk+'/';
        },500);
    }
}

$(document).ready(formAjax.fnOnRead);