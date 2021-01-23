// #####################################################################
// 카카오 관련 함수들
// #####################################################################

function loginWithKakao() {
  if (!Kakao.Auth.getAccessToken()) {
    // 로그인
    Kakao.Auth.login({
      // authObj : accessToken, type, expires_in, scope 등 포함
      success: function (authObj) {
        // alert('login success: ' + JSON.stringify(authObj)),
        // 유저 인포 불러오기
        Kakao.API.request({
          url: "/v2/user/me",
          success: function (res) {
            var LOGIN_INFO = JSON.stringify(authObj);
            var USER_INFO = JSON.stringify(res);
            var current_url =
              $(location).attr("pathname") + "kakao_login/";
            $.ajax({
              type: "POST",
              // url: current_url,
              url: "/kakao_login/",
              dataType: "json",
              //csrfmiddlewaretoken: '{{ csrf_token }}',
              data: { LOGIN_INFO: LOGIN_INFO, USER_INFO: USER_INFO },
            }).done(function (res) {
              alert(Object.keys(res).length);
              if (Object.keys(res).length == 1) {
                window.location.replace(
                  "http://127.0.0.1:8000/user_profile/"
                );
              } else {
                location.reload();
              }
            });
          },
        });
      },
      fail: function (err) {
        alert("failed to login: " + JSON.stringify(err));
      },
    });
  }
}

function logoutWithKakao() {
  Kakao.Auth.logout(function () {
    $.ajax({
      type: "POST",
      url: "/kakao_logout/",
    }).done(function () {
      location.reload();
    });
  });
}

function unlinkApp() {
  Kakao.API.request({
    url: "/v1/user/unlink",
    success: function (res) {
      Kakao.Auth.setAccessToken(undefined);
      $.ajax({
        type: "POST",
        url: "/kakao_unlink/",
      }).done(function () {
        location.reload();
      });
      alert("success: " + JSON.stringify(res));
    },
    fail: function (err) {
      alert("fail: " + JSON.stringify(err));
    },
  });
}

function profileWithKakao() {
  Kakao.API.request({
    url: "/v2/user/me",
    success: function (response) {
      
      document.getElementById("userid").innerText = response.id;
      document.getElementById("nickname").innerText =
        response.kakao_account.profile.nickname;
      document.getElementById("profile_image").src =
        response.properties.profile_image;
      document.getElementById("thumbnail_image").src =
        response.properties.thumbnail_image;
    },
    fail: function (error) {
      console.log(error);
    },
  });
}

$(document).ready(function () {
  $("#after_login").click(function () {
    alert("카카오톡으로 로그인 후 이용해주세요");
  });
});

Kakao.Link.createDefaultButton({
  container: "#create-kakao-link-btn",
  objectType: "feed",
  content: {
    title: "포스트 제목을 여기에 가져와야 함",
    description:
      "여기에는 포스트 ckcontent 가져와야 함 #사라 #마라 #사이트 #테스트 #해쉬태그를 해야하나",
    imageUrl:
      "https://cdn.pixabay.com/photo/2018/06/04/00/29/women-3452067_1280.jpg",
    link: {
      // mobileWebUrl: "https://developers.kakao.com",
      // webUrl: "https://developers.kakao.com",
      mobileWebUrl: $(location).attr("href"),
      webUrl: $(location).attr("href"),
    },
  },
  social: {
    likeCount: 286, // 이걸 사라, 마라, 댓글, 조회수, 공유수 로 바꿀수가 있나?
    commentCount: 45,
    sharedCount: 845,
  },
  /*buttons: [
    {
      title: "웹으로 보기",
      link: {
        mobileWebUrl: "https://developers.kakao.com",
        webUrl: "https://developers.kakao.com",
      },
    },
    {
      title: "앱으로 보기",
      link: {
        mobileWebUrl: "https://developers.kakao.com",
        webUrl: "https://developers.kakao.com",
      },
    },
  ],*/
});

// #####################################################################
// 카카오 관련 함수들
// #####################################################################



// #####################################################################
// 포스트 이미지 관련 함수들
// #####################################################################

$(function () {
  // Multiple images preview in browser
  var imagesPreview = function (input, placeToInsertImagePreview) {
    if (input.files) {
      var filesAmount = input.files.length;

      for (i = 0; i < filesAmount; i++) {
        var reader = new FileReader();

        reader.onload = function (event) {
          $(
            $.parseHTML(
              "<img class='new_images' style='width: 100%; height: auto;'>"
            )
          )
            .attr("src", event.target.result)
            .appendTo(placeToInsertImagePreview);
        };

        reader.readAsDataURL(input.files[i]);
      }
    }
  };

  $("#gallery-photo-add").on("change", function () {
    // document.getElementById("current_post_image").style.display = "none";
    $(".current_post_image").remove();
    $(".new_images").remove();
    imagesPreview(this, "div.gallery");
  });
});

// #####################################################################
// 포스트 이미지 관련 함수들
// #####################################################################



// #####################################################################
// 포스트 수정 관련 함수들
// #####################################################################


$(document).ready(function () {
  $("#add_comment_button").click(function () {
    var comment_input = $("#comment_input").val();
    var current_url = $(location).attr("pathname"); // + "add_comment/";
    $.ajax({
      type: "POST",
      url: current_url, //"/add_comment/",
      data: { comment_input: comment_input },
    }).done(function () {
      location.reload();
      $("#comment_input").val("");
    });
  });
});

function EditCommentBox(input) {
  var text = $(".comment_" + input + ">div.text")
    .html()
    .replaceAll("<p>", "")
    .replaceAll("</p>", "")
    .replaceAll("<br>", "\n")
    .replaceAll("      ", "")
    .replaceAll("\n    ", "");
  $(".comment_" + input + ">div.text").html(
    "<textarea id='newComment' rows='4' cols='40'>" + text + "</textarea>"
  );
  $(".edit_delete_button").hide();
  $(".edit_button_" + input + "").show();
}

function EditComment(input) {
  var new_comment = $("#newComment").val();
  var current_url = $(location).attr("pathname");
  $.ajax({
    type: "POST",
    url: current_url,
    data: { new_comment: new_comment, pk: input },
  }).done(function () {
    location.reload();
  });
}

function DeleteComment(input) {
  if (confirm("정말 삭제하시겠습니까?") == true) {
    //확인
    var current_url = $(location).attr("pathname");
    $.ajax({
      type: "POST",
      url: current_url,
      data: { delete_comment_pk: input },
      //csrfmiddlewaretoken: {{ csrf_token }},
    }).done(function () {
      location.reload();
    });
  } else {
    //취소
    return;
  }
}

function DeletePost(input) {
  if (confirm("정말 삭제하시겠습니까?") == true) {
    //확인
    var current_url = $(location).attr("pathname");

    $.ajax({
      type: "POST",
      url: current_url,
      data: { delete_post: input },
    }).done(function () {
      window.location.replace("http://127.0.0.1:8000/");
    });
  } else {
    //취소
    return;
  }
}

// #####################################################################
// 포스트 수정 관련 함수들
// #####################################################################



// #####################################################################
// 포스트 투표 관련 함수들
// #####################################################################

$("#plz_login_sara").click(function () {
  alert("이건 사야한다!! 투표하려면 로그인을 해주세요");
});

$("#plz_login_mara").click(function () {
  alert("이건 절대아니다!! 투표하려면 로그인을 해주세요");
});

$("#sarabutton").click(function () {
  var current_url = $(location).attr("pathname");
  var saramara_data = "sara";
  $.ajax({
    type: "POST",
    url: current_url,
    data: { saramara_input: saramara_data },
  }).done(function () {
    location.reload();
  });
});

$("#marabutton").click(function () {
  var current_url = $(location).attr("pathname");
  var saramara_data = "mara";
  $.ajax({
    type: "POST",
    url: current_url,
    data: { saramara_input: saramara_data },
  }).done(function () {
    location.reload();
  });
});

$(document).ready(function () {
  $("#vote-result").click(function () {
    $("div.vote-result-area").slideToggle(1000);
  });
});

// #####################################################################
// 포스트 투표 관련 함수들
// #####################################################################



// #####################################################################
// 마이페이지에서 유저정보 수정할때 사용되는 함수들
// #####################################################################

function confirmNewNickname() {
  var username_input = $("#username_input").val();
  if (username_input.length < 4 || username_input.length > 16) {
    $("#check_duplicated").text("4~16자리로 변경 가능합니다.");
  } else {
    $.ajax({
      type: "GET",
      url: "/user_profile/",
      data: { username_input: username_input },
    }).done(function (res) {
      if (Object.keys(res).length == 1) {
        $("#check_duplicated").text("사용가능한 닉네임이에요 :)");
      } else {
        $("#check_duplicated").text("이미 사용중인 닉네임이에요 :(");
      }
    });
  }
}

function noSpaceForm(obj) {
  // 공백사용못하게
  var str_space = /\s/; // 공백체크
  if (str_space.exec(obj.value)) {
    alert(
      "해당 항목에는 공백을 사용할수 없습니다.\n\n공백은 자동적으로 제거 됩니다."
    );
    obj.focus();
    obj.value = obj.value.replace(" ", ""); // 공백제거
    return false;
  }
  // onkeyup="noSpaceForm(this);" onchange="noSpaceForm(this);"
}

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    form_data = new FormData();

    reader.onload = function (e) {
      $(".image-upload-wrap").hide();
      $(".file-upload-image").attr("src", e.target.result);

      $(".file-upload-content").show();
      $(".image-title").html(input.files[0].name);
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    removeUpload();
  }
}

function removeUpload() {
  $(".file-upload-input").replaceWith($(".file-upload-input").clone());
  //$(".file-upload-content").hide();
  //$(".file-upload-content").show();
  $(".file-upload-image").attr("src", "{{ user.profile_image.url }}");
  $(".image-upload-wrap").hide();
  //$(".image-upload-wrap").show();
}

document.getElementById("submit_profile").onclick = function () {
  $.ajax({
    url: "/user_profile/",
    method: "POST",
    data: new FormData(imageForm),
    processData: false,
    contentType: false,
  }).done(function () {
    window.location.replace("http://127.0.0.1:8000/");
  });
};

// #####################################################################
// 마이페이지에서 유저정보 수정할때 사용되는 함수들
// #####################################################################
