angular.module('App').controller('LoginCtrl',
  ['$scope', '$location','$http','$rootScope', function($scope, $location, $http, $rootScope) {
   
   $scope.message = null;
   $scope.firstName = null;
   $scope.lastName = null;

   $scope.submit = function () {
      if ($scope.firstName == 'george' && $scope.lastName == 'washington') {
         $http.get('/mockData/george_washington_user.json').success(function(data){$rootScope.userData = data;});
         window.setTimeout($location.path('/courses'), 1000);         
      }
      else if ($scope.firstName == 'honest' && $scope.lastName == 'abe') {
         $http.get('/mockData/honest_abe_user.json').success(function(data){$rootScope.userData = data;});
         window.setTimeout($location.path('/courses'), 1000);         
      }
      else {
         $scope.message = 'Fail';
      }
   };
}]);
