// Навигационное меню
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
    
    initPhoneMasks();

    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 500);
        });
    }, 5000);
});

function openCallModal(serviceId = null) {
    const modal = document.getElementById('callModal');
    const serviceIdInput = document.getElementById('serviceId');

    if (serviceId) {
        serviceIdInput.value = serviceId;
    } else {
        serviceIdInput.value = '';
    }

    modal.style.display = 'block';
}

function closeCallModal() {
    const modal = document.getElementById('callModal');
    modal.style.display = 'none';
    document.getElementById('callForm').reset();
}

function openPrivacyModal() {
    const modal = document.getElementById('privacyModal');
    modal.style.display = 'block';
}

function closePrivacyModal() {
    const modal = document.getElementById('privacyModal');
    modal.style.display = 'none';
}

window.onclick = function(event) {
    const callModal = document.getElementById('callModal');
    const privacyModal = document.getElementById('privacyModal');

    if (event.target == callModal) {
        closeCallModal();
    }
    if (event.target == privacyModal) {
        closePrivacyModal();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const callForm = document.getElementById('callForm');
    const consultationForm = document.getElementById('consultationForm');

    if (callForm) {
        callForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitCallRequest(callForm);
        });
    }

    if (consultationForm) {
        consultationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitCallRequest(consultationForm);
        });
    }
});

function submitCallRequest(form) {
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/call-request/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            form.reset();
            closeCallModal();
            location.reload();
        } else {
            alert('Ошибка: ' + data.errors.join(', '));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Произошла ошибка при отправке заявки');
    });
}

function toggleFAQ(element) {
    const faqItem = element.parentElement;
    const allFaqItems = document.querySelectorAll('.faq-item');

    allFaqItems.forEach(item => {
        if (item !== faqItem) {
            item.classList.remove('active');
        }
    });

    faqItem.classList.toggle('active');
}

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

// ========== ИСПРАВЛЕННАЯ МАСКА ДЛЯ ТЕЛЕФОНА ==========
function initPhoneMasks() {
    const phoneInputs = document.querySelectorAll('.phone-input, #phone-input, #login-phone-input, #profile-phone-input');

    phoneInputs.forEach(input => {
        input.value = '';

        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            if (value.startsWith('8')) {
                value = '7' + value.slice(1);
            }

            if (value && !value.startsWith('7')) {
                value = '7' + value;
            }

            value = value.slice(0, 11);

            let formatted = '';
            if (value.length > 0) {
                formatted = '+7';
                if (value.length > 1) {
                    formatted += ' (' + value.slice(1, 4);
                }
                if (value.length >= 5) {
                    formatted += ') ' + value.slice(4, 7);
                }
                if (value.length >= 8) {
                    formatted += '-' + value.slice(7, 9);
                }
                if (value.length >= 10) {
                    formatted += '-' + value.slice(9, 11);
                }
                e.target.value = formatted;
            } else {
                e.target.value = '';
            }
        });

        input.addEventListener('keydown', function(e) {
            if ([46, 8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true) ||
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                return;
            }
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });

        input.addEventListener('focus', function(e) {
            if (!e.target.value) {
                e.target.value = '';
            }
        });

        input.addEventListener('blur', function(e) {
            if (e.target.value === '+7' || e.target.value === '+7 (') {
                e.target.value = '';
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.querySelector('.auth-form-container form');

    if (registerForm && window.location.pathname.includes('register')) {
        const password1 = document.getElementById('password1');
        const password2 = document.getElementById('password2');

        if (password1 && password2) {
            password1.addEventListener('copy', function(e) {
                e.preventDefault();
                return false;
            });

            password2.addEventListener('paste', function(e) {
                e.preventDefault();
                return false;
            });
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');

    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                if (file.size > 5 * 1024 * 1024) {
                    alert('Размер файла не должен превышать 5 МБ');
                    e.target.value = '';
                    return;
                }

                const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
                if (!allowedTypes.includes(file.type)) {
                    alert('Допустимые форматы: JPG, PNG, GIF, WEBP');
                    e.target.value = '';
                    return;
                }
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');

    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--color-yellow)';
            link.style.fontWeight = 'bold';
        }
    });
});