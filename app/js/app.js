'use strict';

var App = angular.module('App', ['ngRoute']);

App.factory('myHttpInterceptor', function($rootScope, $q) {
  return {
    'requestError': function(config) {
      $rootScope.status = 'HTTP REQUEST ERROR ' + config;
      return config || $q.when(config);
    },
    'responseError': function(rejection) {
      $rootScope.status = 'HTTP RESPONSE ERROR ' + rejection.status + '\n' +
                          rejection.data;
      return $q.reject(rejection);
    },
  };
});

App.factory('messageService', function($rootScope, $http, $q, $log) { //guestService
  $rootScope.status = 'Retrieving data...';
  var deferred = $q.defer();
  $http.get('rest/query')
  .success(function(data, status, headers, config) {
    $rootScope.messages = data;
    deferred.resolve();
    $rootScope.status = '';
  });
  return deferred.promise;
});

App.config(function($routeProvider) {
  $routeProvider.when('/', {
    controller : 'MainCtrl',
    templateUrl: '/partials/main.html',
    resolve    : { 'messageService': 'messageService' },
  });
  $routeProvider.when('/invite', {
    controller : 'InsertCtrl',
    templateUrl: '/partials/insert.html',
  });
  $routeProvider.when('/update/:id', {
    controller : 'UpdateCtrl',
    templateUrl: '/partials/update.html',
    resolve    : { 'messageService': 'messageService' },
  });
  $routeProvider.otherwise({
    redirectTo : '/'
  });
});

App.config(function($httpProvider) {
  $httpProvider.interceptors.push('myHttpInterceptor');
});

App.controller('MainCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.invite = function() {
    $location.path('/invite');
  };

  $scope.update = function(message) {
    $location.path('/update/' + message.id);
  };

  $scope.delete = function(message) {
    $rootScope.status = 'Deleting message ' + message.id + '...';
    $http.post('/rest/delete', {'id': message.id})
    .success(function(data, status, headers, config) {
      for (var i=0; i<$rootScope.messages.length; i++) {
        if ($rootScope.messages[i].id == message.id) {
          $rootScope.messages.splice(i, 1);//removes messages from list
          break;
        }
      }
      $rootScope.status = '';
    });
  };

});

App.controller('InsertCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route) {

  $scope.submitInsert = function() {
    var message = {
      first : $scope.first,
      last : $scope.last, 
      msg : $scope.msg, 
    };
    $rootScope.status = 'Creating...';
    $http.post('/rest/insert', message)
    .success(function(data, status, headers, config) {
      $rootScope.messages.push(data);
      $rootScope.status = '';
    });
    $location.path('/');
  }
});

App.controller('UpdateCtrl', function($routeParams, $rootScope, $scope, $log, $http, $location) {

  for (var i=0; i<$rootScope.messages.length; i++) {
    if ($rootScope.messages[i].id == $routeParams.id) {
      $scope.message = angular.copy($rootScope.messages[i]);
    }
  }

  $scope.submitUpdate = function() {
    $rootScope.status = 'Updating...';
    $http.post('/rest/update', $scope.message)
    .success(function(data, status, headers, config) {
      for (var i=0; i<$rootScope.messages.length; i++) {
        if ($rootScope.messages[i].id == $scope.message.id) {
          $rootScope.messages.splice(i,1);
          break;
        }
      }
      $rootScope.messages.push(data);
      $rootScope.status = '';
    });
    $location.path('/');
  };

});

