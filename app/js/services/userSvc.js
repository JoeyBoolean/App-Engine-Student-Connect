angular.module('App').factory('userSvc', ['$http', function ($http) {
   
   var userData = null;

   var updateUserData = function (string) {
      $http.get('/mockData/' + string).success(function(data) {
         userData = data;
      });
      
   };

   var getUserData = function () {
      return userData;
   };

   return {
      updateUserData : updateUserData,
      getUserData : getUserData
   };
}]);
