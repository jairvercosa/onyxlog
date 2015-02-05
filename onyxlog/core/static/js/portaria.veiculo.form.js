/**
 * Controller para formulário
 * de movimento de veículos de portaria
 *
 * @author Jair Verçosa
 * @date 17/01/2015
 */

var formVeiculo = {
    id: veiculo_id,
    ocupantes: ocupates_veiculo,
    
    /* Função para adicionar um ocupante
     *
     * @return void
     */
    onClickAddOcupante: function(){
        var item = {};

        formVeiculo.ocupantes.push({
            cpf: '',
            nome: '',
            empresa: ''
        });

        item = formVeiculo.ocupantes[formVeiculo.ocupantes.length - 1];
        formVeiculo.addFieldsTable(item);
    },

    /* Função que adiciona os campos na tabela
     *
     * @return void
     */
    addFieldsTable: function(item){
        var buttons = '';
        var html = '';

        if(formVeiculo.id == 0){
            buttons = '\
                <button class="btn btn-sm btn-danger btn-remove-ocupante"><i class="glyphicon glyphicon-remove"></i></button> \
            ';

            html = '\
                <tr> \
                    <td> \
                        <div class="control"> \
                            <input type="text" maxlength="11" name="cpf" value="'+ item.cpf +'"/> \
                        </div> \
                    </td> \
                    <td> \
                        <div class="control"> \
                            <input type="text" maxlength="100" name="nome" value="'+ item.nome +'"/> \
                        </div> \
                    </td> \
                    <td> \
                        <div class="control"> \
                            <input type="text" maxlength="60" name="empresa" value="'+ item.empresa +'"/> \
                        </div> \
                    </td> \
                    <td> \
                        '+buttons+' \
                    </td> \
                </tr>';
        }else{
            html = '\
                <tr> \
                    <td>'+ item.cpf +'</td> \
                    <td>'+ item.nome +'</td> \
                    <td>'+ item.empresa +'</td> \
                    <td></td> \
                </tr>';
        }

        $('#table-ocupantes tbody').append(html);
        $('.btn-remove-ocupante').bind('click',formVeiculo.onClickRemoveOcupante);
        $('input[name="cpf"]').bind('blur',function(){
            nomeEle = $(this).parent().parent().parent().find('input[name="nome"]')
            empresaEle = $(this).parent().parent().parent().find('input[name="empresa"]')

            if($(nomeEle).val() == ''){
                $.get(
                    '/portaria/movimento/visitante/api/'+ $(this).val() +'/',
                    {},
                    function(response){
                        $(nomeEle).val(response.nome);
                        $(empresaEle).val(response.empresa);
                    }
                );
            }
        });
    },

    /* Função para remover um ocupante
     *
     * @return void
     */
    onClickRemoveOcupante: function(){
        $(this).parent().parent().remove();
    }

}

$(document).ready(function(){
    $('#btn-add-ocupante').bind('click',formVeiculo.onClickAddOcupante);
    form.fnGetDataAsJson = function(){
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

        indexed_array['ocupantes[]'] = []
        $.each($('#table-ocupantes tbody tr'),function(i, obj){
            var fields = $(obj).find('input');
            var dict = "{";
            $.each(fields,function(x, item){
                dict += '"'+$(item).attr('name')+'": "'+$(item).val()+'",';
            });

            dict = dict.substr(0,dict.length-1) + "}";
            indexed_array['ocupantes[]'].push(dict);
        });

        return indexed_array;
    };

    if(formVeiculo.ocupantes.length > 0){
        $.each(formVeiculo.ocupantes,function(i,obj){
            formVeiculo.addFieldsTable(obj);
        });
    }
});

