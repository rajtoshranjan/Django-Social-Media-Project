function changeToInput(id, type, sendTo) {
	// btn.style.display = 'none';
	let elm = document.getElementById(id);
    // console.log(sendTo)
    if (type == 'radio') {
        let malechecked = '';
        let femalechecked = '';
        let otherchecked = '';
        if (elm.innerText == "Male")
            malechecked = 'checked';
        else if (elm.innerText == "Female")
            femalechecked = 'checked'
        else if (elm.innerText == "Other")
            otherchecked = 'checked'

        let male = `<div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" name="gender" ${malechecked} id="inlineRadio1" value="Male">
              <label class="form-check-label" for="inlineRadio1">Male</label>
            </div>`
        let female = `
    <div class="form-check form-check-inline">
      <input class="form-check-input" type="radio" name="gender" ${femalechecked} id="inlineRadio2" value="Female">
      <label class="form-check-label" for="inlineRadio2">Female</label>
    </div>`
    let other = `<div class="form-check form-check-inline">
      <input class="form-check-input" type="radio" name="gender" ${otherchecked} id="inlineRadio3" value="Other">
      <label class="form-check-label" for="inlineRadio3">Other</label>
    </div>
    `;
        elm.innerHTML = `<div onchange="SendValue('${id}','gender','${sendTo}')">${male+female+other}</div>`;
    }
    else{
        elm.innerHTML = `<input type = ${type} 
        class = "form-control"
        value = '${elm.innerText}'
        name = 'value' 
        onchange="SendValue('${id}',this.value,'${sendTo}')"
        />
    `
    }
	
}


function SendValue(id,value,to) {
    console.log(value);
    if (id == 'gender')
        value = radioValue('gender');
	$.ajax(
    {
        type:"GET",
        url: to,
        data:{
                 value: value
        },	
        success: function(data) 
        {
        	console.log(id)

         	document.getElementById(id).innerHTML = data;
         	// btn.style.display = 'block';  
        }
     });
}

function radioValue(name) { 
            var ele = document.getElementsByName(name); 
              
            for(i = 0; i < ele.length; i++) { 
                if(ele[i].checked) 
                return ele[i].value; 
            } 
        } 


function Follow(btn, to){
     
    $.ajax(
    {
        type:"POST",
        url: "/follow",
        data:{
                 user: to
        },  
        success: function(data) 
        {
            btn.innerText = 'Unfollow';
            btn.setAttribute('onClick',`Unfollow(this, '${to}')`); 
            let cnt = document.getElementById('following_count');
            cnt.innerText = Number(cnt.innerHTML)+1
        }
     }); 
}

function Unfollow(btn, to){
    $.ajax(
    {
        type:"POST",
        url: "/unfollow",
        data:{
                 user: to
        },  
        success: function(data) 
        {
            btn.innerText = 'Follow';
            btn.setAttribute('onClick',`Follow(this, '${to}')`); 
            let cnt = document.getElementById('following_count');
            cnt.innerText = Number(cnt.innerHTML)-1
        }
     });
}



const getFollowers = () =>{
  $.ajax(
    {
        type:"POST",
        url: "/user/followers",
        data:{},  
        success: function(data) 
        {
          let elm = document.getElementById('followersandfollowings');  
          let f_elm = '';
          let btn = '';
          for(i in data)
          {
            if (data[i].followed_back){
              btn = ` <button class="followbtn" onclick="Unollow(this, '${data[i].username}')">
                            Unfollow
                    </button>`
            }
            else{
              btn = ` <button class="followbtn" onclick="Follow(this, '${data[i].username}')">
                            Follow Back
                    </button>`
            }
            f_elm += `
            <div class="card mb-1" style="max-width: 540px;">
              <div class="row no-gutters">
                <div class="col-3 text-center align-items-center d-flex" style="">
                  <a href="/user/${data[i].username}" class="m-auto">
                  <img src=${data[i].pic} class="card-img m-auto" style="width: 49px" ></a>
                </div>
                <div class="col-9">
                  <div class="card-body p-0 mb-1 mt-1">
                    <a href="/user/${data[i].username}"><b class="card-title">${data[i].first_name} ${data[i].last_name}</b></a><br>
                    ${btn}
                  </div>
                </div>
              </div>
            </div>
            `;
          }
          let followersModel = `
            <div class="modal fade" id="followersModal" tabindex="-1" aria-labelledby="followersModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-sm">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="followersModalLabel">Followers</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body" style="height: 75vh; overflow-y:scroll;">
                    ${f_elm}
                  </div>
                </div>
              </div>
            </div>
          ` ;
          elm.innerHTML = followersModel;
          $('#followersModal').modal('show')
        }
     });
}

const getFollowings = () =>{
  $.ajax(
    {
        type:"POST",
        url: "/user/following",
        data:{},  
        success: function(data) 
        {
          let elm = document.getElementById('followersandfollowings');
          let f_elm = '';
          for(i in data)
          {
            f_elm += `
            <div class="card mb-1" style="max-width: 540px;">
              <div class="row no-gutters">
                <div class="col-3 text-center align-items-center d-flex" style="">
                  <a href="/user/${data[i].username}" class="m-auto">
                  <img src=${data[i].pic} class="card-img m-auto" style="width: 49px" ></a>
                </div>
                <div class="col-9">
                  <div class="card-body p-0 mb-1 mt-1">
                    <a href="/user/${data[i].username}"><b class="card-title">${data[i].first_name} ${data[i].last_name}</b></a><br>
                    <button class="followbtn" onclick="Unfollow(this, '${data[i].username}')">
                            Unfollow
                    </button>
                  </div>
                </div>
              </div>
            </div>
            `;
          }
          let followingModel = `
            <div class="modal fade" id="followingModal" tabindex="-1" aria-labelledby="followingModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-sm">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="followingModalLabel">Followings</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body" style="height: 75vh; overflow-y:scroll;">
                    ${
                       f_elm
                    }
                  </div>
                </div>
              </div>
            </div>
          `;
          elm.innerHTML = followingModel;
          $('#followingModal').modal('show')
        }
     });
}


const Post = (order, post_id) => {
  // console.log(this)
  $.ajax(
    {
        type:"POST",
        url: "/post",
        data:{
                 order: order,
                 post: post_id
        },  
        success: function(data) 
        {
            if(data=='deleted')
              document.getElementById(`post${post_id}`).innerHTML = "";
            else if(data=='liked'){
              let footer = document.getElementById(`post${post_id}`).getElementsByClassName('card-footer')[0];
              let body = document.getElementById(`post${post_id}`).getElementsByClassName('card-body')[0];
              let likebtn = footer.getElementsByClassName('click')[0];
              let dislikebtn = footer.getElementsByClassName('click')[1];
              let likes = body.getElementsByClassName('likes')[0];
              likebtn.setAttribute('class', 'card-link m-auto like_active click')
              likebtn.setAttribute('onclick', `Post('like-back', '${post_id}')`)
              dislikebtn.setAttribute('class', 'card-link m-auto click')
              dislikebtn.setAttribute('onclick', `Post('dislike', '${post_id}')`)
              likes.innerText = Number(likes.innerText)+1;
            }
            else if(data=='disliked'){
              let footer = document.getElementById(`post${post_id}`).getElementsByClassName('card-footer')[0];
              let body = document.getElementById(`post${post_id}`).getElementsByClassName('card-body')[0];
              let likebtn = footer.getElementsByClassName('click')[0];
              let dislikebtn = footer.getElementsByClassName('click')[1];
              let dislikes = body.getElementsByClassName('dislikes')[0]
              likebtn.setAttribute('class', 'card-link m-auto click')
              likebtn.setAttribute('onclick', `Post('like', '${post_id}')`)
              dislikebtn.setAttribute('class', 'card-link m-auto click like_active')
              dislikebtn.setAttribute('onclick', `Post('dislike-back', '${post_id}')`)
              dislikes.innerText = Number(dislikes.innerText)+1;
            }
            else if(data=='like-backed'){
              let footer = document.getElementById(`post${post_id}`).getElementsByClassName('card-footer')[0];
              let body = document.getElementById(`post${post_id}`).getElementsByClassName('card-body')[0];
              let likebtn = footer.getElementsByClassName('click')[0];
              let likes = body.getElementsByClassName('likes')[0];
              likebtn.setAttribute('class', 'card-link m-auto click')
              likebtn.setAttribute('onclick', `Post('like', '${post_id}')`)
              likes.innerText = Number(likes.innerText)-1;
            }
            else if(data=='dislike-backed'){
              let footer = document.getElementById(`post${post_id}`).getElementsByClassName('card-footer')[0];
              let body = document.getElementById(`post${post_id}`).getElementsByClassName('card-body')[0];
              let dislikebtn = footer.getElementsByClassName('click')[1];
              let dislikes = body.getElementsByClassName('dislikes')[0]
              dislikebtn.setAttribute('class', 'card-link m-auto click')
              dislikebtn.setAttribute('onclick', `Post('dislike', '${post_id}')`)
              dislikes.innerText = Number(dislikes.innerText)-1;
            }
        }
     });
}

function CommentReplyForm(div_id, comm_id, img) {
                        let elm = `
                          <form class="card-footer p-0 m-0 input-group" style="border:none;">
                            <div class="input-group-prepend rounded-0">
                              <span class="input-group-text" style="border-radius:0">
                                <img class="rounded-circle" width="20" height="20"
                                  src="${img}" alt="">
                              </span>
                            </div>
                            <input type="text" class="form-control" aria-label="Write a Comment"
                              placeholder="Add a Public Reply" id="reply_comment_of_${comm_id}">
                            <div class="input-group-append">
                              <button class="input-group-text btn" type="button" 
                              onclick="addSubcomment('${comm_id}', 'reply_comment_of_${comm_id}','${div_id}')"
                              ><i class="fa fa-paper-plane"
                                  aria-hidden="true"></i></button>
                            </div>
                          </form>`;
                      document.getElementById(div_id).innerHTML = elm;
                      }


function addComment(post_id, comm_test_id, div_id){
    comm = document.getElementById(comm_test_id).value;
    $.ajax(
    {
        type:"POST",
        url: "/add_comment",
        data:{
                 post_id: post_id,
                 comm: comm
        },  
        success: function(data) 
        {
            elm = document.getElementById(div_id);
            elm.innerHTML += `
            <div class="media">
              <img src="${data.url}" width="40" height="40" alt="..." class="img-thumbnail rounded mr-3">
              <div class="media-body">
                <b>${data.name}</b>
                <p style="font-size: 13px;">${data.text}</p>
                <div id="comment${data.id}">
                  <button class="btn-sm mainbtn"  
                  onclick="CommentReplyForm('comment${data.id}',
                   '${data.id}', 
                   '${data.url}')">Reply</button>
                </div>
                <div id="comment${data.id}replys"></div>
              </div>
            </div>
            `;
            document.getElementById(comm_test_id).value = "";
        }
     });
}

function addSubcomment(comm_id, comm_test_id, div_id){
    comm = document.getElementById(comm_test_id).value;
    $.ajax(
    {
        type:"POST",
        url: "/add_subcomment",
        data:{
                 comm_id: comm_id,
                 comm: comm
        },  
        success: function(data) 
        {
            elm = document.getElementById(div_id);
            elm.innerHTML += `
            <div class="media">
              <img src="${data.url}" width="40" height="40" alt="..." class="img-thumbnail rounded mr-3">
              <div class="media-body">
                <b>${data.name}</b>
                <p style="font-size: 13px;">${data.text}</p>
                <div id="comment${data.id}replys"></div>
              </div>
            </div>
            
            `;
            document.getElementById(comm_test_id).value = "";
        }
     });
}