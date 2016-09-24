'use strict';

var ustcRing = angular.module('ustc.ring', ['ui.router', 'ui.bootstrap']);

ustcRing.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('pool');
    $stateProvider
        .state('pool', {
            url: '/pool',
            controller: 'PoolCtrl',
            templateUrl: 'pool.html'
        })
        .state('upload', {
            url: '/upload',
            controller: 'UploadCtrl',
            templateUrl: 'upload.html'
        })
        .state('remove', {
            url: '/remove',
            controller: 'RemoveCtrl',
            templateUrl: 'remove.html'
        })
        .state('upload-success', {
            url: '/upload-success',
            templateUrl: 'upload-success.html'
        })
        .state('plus-one', {
            url: '/plus-one',
            controller: 'PlusOneCtrl',
            templateUrl: 'plus-one.html'
        })
        .state('help', {
            url: '/help',
            templateUrl: 'help.html'
        });
});

ustcRing.controller('PoolCtrl', function($scope, $http) {
    $scope.showTel = function(tel) {
        var text = parseInt(tel, 10);
        window.prompt("对方手机号", text.toString());
    };
    var fetch = function() {
        $http.get('/pool').then(function(res) {
            $scope.items = res.data;
        } , function() {
            console.log('err');
        });
    };
    fetch();
});

ustcRing.controller('UploadCtrl', function($scope, $http, $location) {
    $scope.updateInfo = function() {
        var data = {
            'id': $scope.user.id,
            'mobile': $scope.user.mobile,
            'ad': $scope.user.ad,
            'followRing1': parseInt($scope.user.followRing1, 10) == '' ? '0000' : parseInt($scope.user.followRing1, 10),
            'followRing2': parseInt($scope.user.followRing2, 10) == '' ? '0000' : parseInt($scope.user.followRing2, 10),
            'followRing3': parseInt($scope.user.followRing3, 10) == '' ? '0000' : parseInt($scope.user.followRing3, 10),
            'followRing4': parseInt($scope.user.followRing4, 10) == '' ? '0000' : parseInt($scope.user.followRing4, 10),
            'followRing5': parseInt($scope.user.followRing5, 10) == '' ? '0000' : parseInt($scope.user.followRing5, 10)
        };
        $http.post('/upload', data).then(function() {
            $location.path('upload-success');
        }, function() {
            console.log('err');
        });
    };
});

ustcRing.controller('PlusOneCtrl', function($scope, $http) {
    $scope.timeRaised = 0;
    $scope.plusOneSecond = function() {
        $http.get('/plus-one').then(function(res) {
            console.log(res.data);
            $scope.timeRaised = res.data['timeRaised'];
        } , function() {
            console.log('err');
        });
    };
    $scope.plusOneSecond();
});

ustcRing.controller('RemoveCtrl', function($scope, $http, $location) {
    $scope.removeUser = function() {
        var data = {
            'id': $scope.user.id,
            'mobile': $scope.user.mobile
        };
        $http.post('/remove', data).then(function() {
            $location.path('/pool');
        }, function() {
            console.log('err');
        });
    };
});