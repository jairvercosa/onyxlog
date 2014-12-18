/**
 * Controller para uso do angularjs na seleção de produtos
 *
 * @author Jair Verçosa
 * @date 14/12/2014
 */


//Aplicação front-end
var etiquetasApp = angular.module('etiquetasApp', [], function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
}).controller('controllerProduto', function controllerProduto($scope, $http){
    /*
     * @var array data - Lista de produtos para serem impressos
     */
    $scope.products = [];
    
    /*
     * busca dados de um produto
     */
    $scope.getProductData = function(productId){
        if(productId==null || typeof(productId) == 'undefined'){
            return false;
        }
        
        $.ajax({
            url: '/cadastros/produto/api/'+productId+'/',
            type: 'get',
            success: function(result){
                $scope.products.push({
                    id: result.id,
                    codigo: result.codigo,
                    desc: result.desc,
                    un: result.unidade,
                    nota: "",
                    pedido: "",
                    fornecedor: result.fornecedor,
                    recebimento: ""
                });

                $scope.$apply();

                $('input[name="dtRecebimento"]').datepicker(app.datePickerBr);
            },
            error: function(response){
                result = $.parseJSON(response.responseText);
                alert(result.message);
            }
        });
    };

    /*
     * adiciona produtos à lista 
     */
    $scope.addProduct = function(){
        var productId = $('#id_produto').val();
        $scope.getProductData(productId);

        $('#id_produto').find('option').selected = false
        $('.custom-combobox-input').val('');
    };

    /*
     * remove itens da lista
     */
    $scope.removeItem = function(item){
        $scope.products.splice($scope.products.indexOf(item),1);
    };

    /*
     * gera as etiquetas
     */
    $scope.generateLabels = function(){
        app.addLoading();
        if($scope.validateData()){
            var data = []

            $.each($('#table-print-label tbody tr'),function( i, obj){
                var item = {
                    "id": $scope.products[i].id,
                    "codigo": $scope.products[i].codigo,
                    "nota": $(obj).find('input[name=nota]').val(),
                    "pedido": $(obj).find('input[name=pedido]').val(),
                    "dtRecebimento": $(obj).find('input[name=dtRecebimento]').val(),
                    "fornecedor": $(obj).find('input[name=fornecedor]').val(),
                }

                data.push(item);
            });

            $('#table-print-label').find('input[value=""]').removeClass('in-error');
            $.ajax({
                url: '/etiquetas/produto/',
                type: 'POST',
                data: {
                    "csrfmiddlewaretoken":$('input[name=csrfmiddlewaretoken]').val(),
                    "data": $.stringify(data)
                },
                success: function(response){
                    app.removeLoading();

                    $('.response_form span').html('Etiquetas geradas com sucesso. Download do arquivo foi inicializado.');
                    $('.response_form').hide();
                    $('.response_form').addClass('alert-success');
                    $('.response_form').removeClass('alert-danger');
                    $('.response_form').fadeIn('fast');
                    $(document).scrollTop(0);
                    setTimeout(function(){
                        $('.response_form').fadeOut('fast');
                    },5000);        

                    window.location.href = "/etiquetas/produto/pdf/";
                },
                error: function(response){
                    app.removeLoading();
                    try{
                        var result = $.parseJSON(response.responseText);
                        
                        $('.response_form span').html(result.message);
                        $('.response_form').hide();
                        $('.response_form').removeClass('alert-success');
                        $('.response_form').addClass('alert-danger');
                        $('.response_form').fadeIn('fast');
                        $(document).scrollTop(0);
                        setTimeout(function(){
                            $('.response_form').fadeOut('fast');
                        },5000);
                    }catch(err){
                        console.log(err.message+'\n\n'+response.responseText);
                        alert('Ocorreu uma falha na operação');
                    }
                }
            });
        }else{
            app.removeLoading();
        }
    };

    /*
     * Valida dados
     */
    $scope.validateData = function(){
        var msg = "";

        if($scope.products.length==0){
            msg = "Selecione ao menos um produto e clique em adicionar.";
        }

        if(msg!=""){
            $('.response_form span').html(msg);
            $('.response_form').hide();
            $('.response_form').removeClass('alert-success');
            $('.response_form').addClass('alert-danger');
            $('.response_form').fadeIn('fast');
            $(document).scrollTop(0);
            setTimeout(function(){
                $('.response_form').fadeOut('fast');
            },5000);

            return false;
        }

        return true;
    };

    $('#id_produto').combobox();
});