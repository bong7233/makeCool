// 비밀번호에 자동커서 설정
$(document).ready(() => {
  $("#input-password").focus();
});

// 정보 검증
const change_up = () => {
  let password = $("#input-password").val();
  let password2 = $("#input-password2").val();
  let name = $("#input-name").val();
  let age = $("#input-age").val();

  if (password == "") {
    $("#help-password")
      .text("비밀번호를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password").focus();
    return;
  } else if (!is_password(password)) {
    $("#help-password")
      .text(
        "비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자"
      )
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password").focus();
    return;
  } else {
    $("#help-password")
      .text("사용할 수 있는 비밀번호입니다.")
      .removeClass("is-danger")
      .addClass("is-success");
  }
  if (password2 == "") {
    $("#help-password2")
      .text("비밀번호를 입력해주세요.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password2").focus();
    return;
  } else if (password2 != password) {
    $("#help-password2")
      .text("비밀번호가 일치하지 않습니다.")
      .removeClass("is-safe")
      .addClass("is-danger");
    $("#input-password2").focus();
    return;
  } else {
    $("#help-password2")
      .text("비밀번호가 일치합니다.")
      .removeClass("is-danger")
      .addClass("is-success");
  }
  $.ajax({
    type: "POST",
    url: "/api/information",
    data: {
      password_give: password,
      name_give: name,
      age_give: age,
    },
    success: (response) => {
      if (response.success == "success") {
        alert(response.msg);
        window.location.replace("/api/profile");
      } else {
        if (response.result === "success") {
          alert(response.msg);
          window.location.href = "/";
        } else {
          alert(response.msg);
          window.location.reload("/api/profile");
        }
      }
    },
  });
};

// 검증 토글
$(document).ready(() => {
  toggle_change_up();
});
const toggle_change_up = () => {
  $("#sign-up-box").toggleClass("is-hidden");
  $("#div-sign-in-or-up").toggleClass("is-hidden");
  $("#btn-check-dup").toggleClass("is-hidden");
  $("#help-password").toggleClass("is-hidden");
  $("#help-password2").toggleClass("is-hidden");
  $("#help-name").toggleClass("is-hidden");
  $("#help-age").toggleClass("is-hidden");
};

const is_password = (asValue) => {
  let regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
  return regExp.test(asValue);
};

const is_name = (asValue) => {
  let regExp = /^[가-힣]+$/;
  return regExp.test(asValue);
};

// 로그아웃
$(document).ready(() => {
  $("#logout").click(() => {
    $.removeCookie("mytoken");
    alert("안녕히가세요");
    window.location.href = "/";
  });
});
