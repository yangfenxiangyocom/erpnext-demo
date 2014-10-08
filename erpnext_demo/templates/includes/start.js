$(document).ready(function() {    
    $("#login_btn").click(function() {
        var me = this;
        $(this).html("登陆中...").prop("disabled", true);
        frappe.call({
            "method": "login",
            args: {
                usr: "demo@erpboost.com",
                pwd: "demo",
                lead_email: $("#lead-email").val(),
            },
            callback: function(r) {
                $(me).prop("disabled", false);
                if(r.exc) {
                    alert("有错误发生，请联系support@erpboost.com");
                } else {
                    console.log("Logged In");
                    window.location.href = "desk";
                }
            }
        })
        return false;
    })
    .prop("disabled", false);
})
