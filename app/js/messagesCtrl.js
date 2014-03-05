angular.module('App').controller('MessagesCtrl',
  ['$scope', '$routeParams','$http','$rootScope', function($scope, $routeParams, $http, $rootScope) {
   
   $scope.messages = null;

   $http.get('/mockData/' + $routeParams.id + '_course.json').success(function(data){$scope.messages = data.Messages;});
}]);
