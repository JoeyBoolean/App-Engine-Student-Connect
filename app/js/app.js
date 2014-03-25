'use strict';

var App = angular.module('App', ['ngRoute', 'ngCookies']);

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
    //deferred.resolve();
    $rootScope.status = '';
  });
  $http.get('rest/query-user')
  .success(function(data, status, headers, config) {
    $rootScope.usernames = data;
    deferred.resolve();
    $rootScope.status = '';
  });
  return deferred.promise;
});

App.factory('nameService', function($rootScope, $http, $q, $log) { //guestService
  $rootScope.status = 'Retrieving name...';
  var deferred = $q.defer();
  $http.get('rest/query-name')
  .success(function(data, status, headers, config) {
    $rootScope.usernames = data;
    deferred.resolve();
    $rootScope.status = '';
  });
  return deferred.promise;
});

App.factory('userNameService', function($rootScope, $http, $q) {
  var userInfo = {
    id: '',
    first: 'test',
    last:'last',
    courses:[
      {
        courseID: '',
        crn: '34525',
        name: 'Intro to World'
      },
      {
        courseID: '12',
        crn: '23455',
        name: 'Fun Stuff'
      }
    ]
  };
  return {
    
    retrieveInfo: function(value) {
      var deferred = $q.defer();
      if ( userInfo.id != value){

        var u = '';
        u = value;
        var userID = {
          user: u,
          test: 'Test'
        };
        console.log(u);
        console.log(userID);
        $http.post('rest/query-user-id', userID)
        .success(function(data, status, headers, config){
          userInfo.id = data.id;
          userInfo.first = data.first;
          userInfo.last = data.last;
          userInfo.courses = data.courses;
          console.log(userInfo.courses)
          console.log(userInfo.courses)
        });
      }
      deferred.resolve();
      return deferred.promise;
    },
    setInfo: function(value) {
      userInfo.id = value.id;
      userInfo.first = value.first;
      userInfo.last = value.last;
      userInfo.courses = value.courses;
      console.log(value.last);
    },
    getInfo: function() {
      return userInfo;
    },
    setName: function(value){
      userInfo.first =value.first;
      userInfo.last = value.last;
    },
    addCourse: function(value){
      userInfo.courses.push(value);
    }
  } 
});


App.config(function($routeProvider) {
  $routeProvider.when('/home', {
    controller : 'MainCtrl',
    templateUrl: '/partials/message.html',
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
  $routeProvider.when('/courses/:id', {
    controller : 'CourseCtrl',
    templateUrl: '/partials/courses.html',
  });
  $routeProvider.when('/courses/add/:id', {
    controller : 'CourseCtrl',
    templateUrl: '/partials/course_add.html',
  });
  $routeProvider.when('/user', {
    controller : 'UserCtrl',
    templateUrl: '/partials/user.html',
  });
  $routeProvider.otherwise({
    redirectTo : '/user'
  });
});

App.config(function($httpProvider) {
  $httpProvider.interceptors.push('myHttpInterceptor');
});

App.controller('UserCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route, userNameService) {

  $scope.newUser = function(user) {

    var user = {
      first : $scope.first,
      last : $scope.last,
    };
    userNameService.setName(user);
    $rootScope.status = 'Adding new user... ';
    $http.post('/rest/insert_user', user)
    .success(function(data, status, headers, config){
      //$cookies.userId = data.id;
      userNameService.setInfo(data);
      console.log(data)
      var test = userNameService.getInfo()
      console.log(test.first);
      $rootScope.status = 'success';
      $rootScope.status = '';
      //console.log($cookies.userId);
    });
    $location.path('/home');

  };
});

App.controller('CourseCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route, userNameService) {

  var userID = $routeParams.id;
  console.log(userID);
  userNameService.retrieveInfo(userID);
  var userData = userNameService.getInfo();
  $scope.userData = userData;
  $scope.courses = userData.courses;
  console.log(userData);

  $scope.gotoCourse = function(course) {
    console.log(course.name);
  };

  $scope.addCourse = function() {
    $location.path('/courses/add/' + userData.id);
  };

  $scope.sendCourse = function() {
    var course_data = {
      id : userData.id,
      crn : $scope.crn,
      name : $scope.name
    };
    $rootScope.status = 'Adding Course....';
    $http.post('/rest/insert_course', course_data)
    .success(function(data, status, headers, config){
      userNameService.addCourse(data);
      var test = userNameService.getInfo();
      console.log(test);
      $rootScope.status = '';
    });
    $location.path('/courses/' + userData.id);
  };

});


App.controller('MainCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route, userNameService) {

 
  var userData = userNameService.getInfo();
  $scope.userData = userData;
  console.log(userData);
  
  
  //$rootScope.filt = userId;
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

App.controller('InsertCtrl', function($scope, $rootScope, $log, $http, $routeParams, $location, $route, userNameService) {

  var userData = userNameService.getInfo();
  $scope.userName = userData;
  console.log(userData);
  $scope.submitInsert = function() {
    var message = {
      first : userData.first,
      last : userData.last, 
      msg : $scope.msg, 
    };
    $rootScope.status = 'Creating...';
    $http.post('/rest/insert', message)
    .success(function(data, status, headers, config) {
      $rootScope.messages.push(data);
      $rootScope.status = '';
    });
    $location.path('/home');
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
    $location.path('/home');
  };

});

App.controller('NavController', function($scope, $rootScope, $log, $http, $routeParams, $location, $route, userNameService) {

  var userData = userNameService.getInfo();
  $rootScope.gotoUser = function() {
    $location.path('/user');
  };

  $rootScope.gotoCourses = function() {
    $location.path('/courses/' + userData.id);
  };
});
