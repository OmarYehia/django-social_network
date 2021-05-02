const toFollowModelBody = document.getElementById('to-follow-body');
const toFollowBtn = document.getElementById('to-follow-btn')
const spinnerBox = document.getElementById('spinner-box');
let toFollowLoaded = false

toFollowBtn.addEventListener('click', ()=>{
$.ajax({
     type: 'GET',
     url: '/profiles/my-profile-json/',
     success: function(response){
         if(!toFollowLoaded){
             const profileData = response.profile_data
              setTimeout(()=>{
                    spinnerBox.classList.add('not-visible')
                     profileData.forEach(el=>{
                            toFollowModelBody.innerHTML += `
                                <div class="row mb-2 align-items-center">
                                    <div class="col-2">
                                       <img class="avatar" src="${el.avatar}" alt="${el.user}">
                                    </div>
                                    <div class="col-3">
                                        <div class="text-muted">${el.user}</div>
                                    </div>
                                    <div class="col text-right">
                                      <button class="btn btn-success">follow</button>
                                    </div>

                                </div>
                              `
                            })
                },2000)
         }

         toFollowLoaded = true
     },
     error: function(error){
        console.log(error)
     }
})
})
