angular.module('App').controller('CoursesCtrl',
  ['$scope', '$location', '$rootScope', '$http',function($scope,$location,$rootScope, $http) {
   
   //$scope.classes = userSvc.getUserData().classes;

   //alert(userSvc.getUserData());

   $scope.submit = function () {
      if ($scope.firstName == 'george' && $scope.lastName == 'washington') {
         //userSvc.updateUserData('george_washington_user.json');
         $http.get('/mockData/george_washington_user.json').success(function(data){$rootScope.userData = data;});
         $location.path('/courses');         
      }
      else if ($scope.firstName == 'honest' && $scope.lastName == 'abe') {
         //userSvc.updateUserData('honest_abe_user.json');
         $location.path('/courses');
      }
      else {
         $scope.message = 'Fail';
      }
   };
}]);
