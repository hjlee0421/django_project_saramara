
/* Close the dropdown menu if the user clicks outside of it */
// window.onclick = function (event) {
//   if (!event.target.matches(".dropbtn")) {
//     var dropdowns = document.getElementsByClassName("dropdown-content");
//     var i;
//     for (i = 0; i < dropdowns.length; i++) {
//       var openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains("show")) {
//         openDropdown.classList.remove("show");
//       }
//     }
//   }
// };

// var acc = document.getElementsByClassName("accordion");
// var i;

// for (i = 0; i < acc.length; i++) {
//   acc[i].addEventListener("click", function () {
//     /* Toggle between adding and removing the "active" class,
//     to highlight the button that controls the panel */
//     this.classList.toggle("active");

//     /* Toggle between hiding and showing the active panel */
//     var panel = this.nextElementSibling;
//     if (panel.style.display === "block") {
//       panel.style.display = "none";
//     } else {
//       panel.style.display = "block";
//     }
//   });
// }

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// 마이페이지 vertical tabs js 함수

function openCity(evt, cityName) {
  var i, tabcontent, tablinks;

  tabcontent = document.getElementsByClassName("tabcontent");

  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablinks");

  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//var myElements = $(".dropdown");

$(document).ready(function () {
  var myElement = $(".check1");
  myElement.text("Hello Sweden!");
});


$(document).ready(function () {
  $("#search-button").click(function () {
    $("div.items-sort-all").toggle();
  });
});



var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides((slideIndex = n));
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex - 1].style.display = "block";
  dots[slideIndex - 1].className += " active";
}

// #####################################################################
// 마이페이지에 사용되는 함수들
// #####################################################################

function logoutWithKakao() {
  console.log(Kakao.Auth.getAccessToken()); //before Logout
  Kakao.Auth.logout(function () {
    console.log(Kakao.Auth.getAccessToken()); //after Logout
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
      //if else 로 username 아래쪽에 가능하면 사용가능한 닉네임입니다.
      // 불가능하면, 이미 사용중인 닉네임입니다. 를 띄우기
      //location.reload();
      console.log(Object.keys(res).length == 1);
      if (Object.keys(res).length == 1) {
        // 이미 사용중인 아이디
        $("#check_duplicated").text("사용가능한 닉네임이에요 :)");
      } else {
        // 사용 가능한 아이디
        $("#check_duplicated").text("이미 사용중인 닉네임이에요 :(");
      }
    });
  }
}

function noSpaceForm(obj) {
  // 공백사용못하게
  var str_space = /\s/; // 공백체크
  if (str_space.exec(obj.value)) {
    //공백 체크
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
