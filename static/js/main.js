'use strict';


var onyxlogApp = angular.module('onyxlogApp', ['ngRoute']);


onyxlogApp.config(['$routeProvider', function($routeProvider){
    
    // Routes for Core templates
    $routeProvider.when('/', {
        templateUrl : '/core/main/',
        controller  : 'mainController'
    }).when('/login', {
        templateUrl : '/autho/login/',
        controller  : 'loginController'
    });
}]);

onyxlogApp.controller('mainController', function($scope){
    
});

onyxlogApp.controller('loginController', function($scope){
    
});
