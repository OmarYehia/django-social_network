const toFollowModelBody = document.getElementById('to-follow-body');
const spinnerBox = document.getElementById('spinner-box');

$.ajax({
     type: 'GET',
     url: '/profiles/my-profile-json/',
     success: function(response){
         console.log(response)
     },
     error: function(error){
        console.log("erroooor")
     }
})