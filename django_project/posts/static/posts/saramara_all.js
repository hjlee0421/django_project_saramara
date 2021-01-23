// #####################################################################
// 카카오계정 관련 함수들
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

// #####################################################################
// 카카오계정 관련 함수들
// #####################################################################


// #####################################################################
// 포스트 수정 관련 함수들
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

// var slideIndex = 1;
// showSlides(slideIndex);

// // Next/previous controls
// function plusSlides(n) {
//   showSlides((slideIndex += n));
// }

// // Thumbnail image controls
// function currentSlide(n) {
//   showSlides((slideIndex = n));
// }

// function showSlides(n) {
//   var i;
//   var slides = document.getElementsByClassName("mySlides");
//   var dots = document.getElementsByClassName("dot");
//   if (n > slides.length) {
//     slideIndex = 1;
//   }
//   if (n < 1) {
//     slideIndex = slides.length;
//   }
//   for (i = 0; i < slides.length; i++) {
//     slides[i].style.display = "none";
//   }
//   for (i = 0; i < dots.length; i++) {
//     dots[i].className = dots[i].className.replace(" active", "");
//   }
//   slides[slideIndex - 1].style.display = "block";
//   dots[slideIndex - 1].className += " active";
// }

// #####################################################################
// 마이페이지에 사용되는 함수들
// #####################################################################

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

// #####################################################################
// 마이페이지에 사용되는 함수들
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

// #####################################################################
// 마이페이지에서 유저정보 수정할때 사용되는 함수들
// #####################################################################
