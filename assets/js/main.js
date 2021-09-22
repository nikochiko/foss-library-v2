require('@fortawesome/fontawesome-free/js/all.js');
require('jquery');
require('bootstrap');
require('bootstrap/js/dist/alert.js');

require.context(
  '../img', // context folder
  true, // include subdirectories
  /.*/, // RegExp
);
