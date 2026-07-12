"use strict";

document.addEventListener("DOMContentLoaded", function () {
    // إخفاء رسائل النجاح والخطأ تلقائيًا بعد خمس ثوانٍ
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alertElement) {
        window.setTimeout(function () {
            if (typeof bootstrap !== "undefined") {
                const alertInstance =
                    bootstrap.Alert.getOrCreateInstance(alertElement);

                alertInstance.close();
            } else {
                alertElement.remove();
            }
        }, 5000);
    });

    // تأكيد العمليات الحساسة مثل حذف أو تعطيل المستخدم
    const confirmationForms =
        document.querySelectorAll("form[data-confirm]");

    confirmationForms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            const message =
                form.dataset.confirm ||
                "Are you sure you want to continue?";

            const confirmed = window.confirm(message);

            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // منع الضغط المتكرر على زر إرسال النموذج
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function () {
            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (!submitButton) {
                return;
            }

            window.setTimeout(function () {
                submitButton.disabled = true;
            }, 50);
        });
    });
});