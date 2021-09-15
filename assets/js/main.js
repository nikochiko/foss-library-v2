require('@fortawesome/fontawesome-free');
require('jquery');
require('bootstrap');

require.context(
  '../img', // context folder
  true, // include subdirectories
  /.*/, // RegExp
);
