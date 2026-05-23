// Мобильное меню (бургер)
document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('navToggle');
    const nav = document.querySelector('.navigation');
    const overlay = document.getElementById('menuOverlay');
    let saveScrollY = 0;
    let callModalScrollY = 0;
    let privacyModalScrollY = 0;
    if (!toggle || !nav) return;

    function closeMenu() {
        nav.classList.remove('active');
        toggle.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        document.body.style.overflow = '';
        document.documentElement.style.overflow = '';
    }

    function openMenu() {
        saveScrollY = window.scrollY;
        nav.classList.add('active');
        toggle.classList.add('active');
        if (overlay) overlay.classList.add('active');
        document.body.style.position = 'fixed';
        document.body.style.top = `-${saveScrollY}px`;
        document.body.style.width = '100%';
        document.body.style.overflow = 'hidden';
        document.documentElement.style.overflow = 'hidden';
    }

    toggle.addEventListener('click', function(e) {
        e.stopPropagation();
        if (nav.classList.contains('active')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }

    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 1110) {
            closeMenu();
        }
    });
});
// Инициализация карусели преимуществ
document.addEventListener('DOMContentLoaded', function() {
    const glideElement = document.querySelector('.advantages-glide');
    if (glideElement) {
        new Glide('.advantages-glide', {
            type: 'carousel',
            perView: 4,
            gap: 25,
            breakpoints: {
                1150: { perView: 3 },
                890: { perView: 2 },
                610: { perView: 1 }
            },
            autoplay: 2000,
            hoverpause: true,
            animationDuration: 400
        }).mount();
    }
});
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

// Модальное окно заказа звонка
function openCallModal(serviceId = null) {
    const modal = document.getElementById('callModal');
    const serviceIdInput = document.getElementById('serviceId');

    if (serviceId) {
        serviceIdInput.value = serviceId;
    } else {
        serviceIdInput.value = '';
    }
    callModalScrollY = window.scrollY;
    modal.style.display = 'block';
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
}

function closeCallModal() {
    const modal = document.getElementById('callModal');
    modal.style.display = 'none';
    document.getElementById('callForm').reset();
    const privacyModal = document.getElementById('privacyModal');
    const isPrivacyOpen = privacyModal.style.display === 'flex' || privacyModal.style.display === 'block';
    if (!isPrivacyOpen) {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        document.body.style.overflow = '';
        document.documentElement.style.overflow = '';
        window.scrollTo(0, callModalScrollY);
    }
}

// Модальное окно политики конфиденциальности
function openPrivacyModal() {
    const modal = document.getElementById('privacyModal');
    privacyModalScrollY = window.scrollY;
    modal.style.display = 'block';
    modal.style.overflow = 'auto';
    modal.style.maxHeight = '100vh';
    document.body.style.position = 'fixed';
    document.body.style.top = `-${privacyModalScrollY}px`;
    document.body.style.width = '100%';
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
}

function closePrivacyModal() {
    const modal = document.getElementById('privacyModal');
    modal.style.display = 'none';
    modal.style.overflow = '';
    modal.style.maxHeight = '';
    const callModal = document.getElementById('callModal');
    const isCallOpen = callModal.style.display === 'flex' || callModal.style.display === 'block';
    if (!isCallOpen) {
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        document.body.style.overflow = '';
        document.documentElement.style.overflow = '';
        window.scrollTo(0, privacyModalScrollY);
    }
}

// Модальное окно просмотра фотографии в услугах
function openImageViewer(imageSrc) {
    const modal = document.getElementById('imageViewerModal');
    const fullImage = document.getElementById('fullImageView');
    modal.style.display = 'block';
    fullImage.src = imageSrc;
    document.body.style.overflow = 'hidden';
}
function closeImageViewer() {
    const modal = document.getElementById('imageViewerModal');
    modal.style.display = 'none';
    document.body.style.overflow = '';
}
const imageModal = document.getElementById('imageViewerModal');
if (imageModal) {
    imageModal.addEventListener('click', function(event) {
        if (event.target === imageModal) {
            closeImageViewer();
        }
    });
}
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('imageViewerModal');
        if (modal && modal.style.display === 'block') {
            closeImageViewer();
        }
    }
});

// Закрытие модального окна при клике вне его
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

// Обработка формы заказа звонка
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

// Toggle для FAQ
function toggleFAQ(element) {
    const faqItem = element.parentElement;
    const allFaqItems = document.querySelectorAll('.faq-item');

    // Закрываем все остальные
    allFaqItems.forEach(item => {
        if (item !== faqItem) {
            item.classList.remove('active');
        }
    });

    // Переключаем текущий
    faqItem.classList.toggle('active');
}

// Показать/скрыть пароль
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
    } else {
        input.type = 'password';
    }
}

// Маска для телефона
function initPhoneMasks() {
    const phoneInputs = document.querySelectorAll('.phone-input, #phone-input, #login-phone-input');

    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');

            // Если начинается с 8, заменяем на 7
            if (value.startsWith('8')) {
                value = '7' + value.slice(1);
            }

            // Если не начинается с 7, добавляем
            if (!value.startsWith('7') && value.length > 0) {
                value = '7' + value;
            }

            // Ограничиваем длину (7 + 10 цифр)
            value = value.slice(0, 11);

            // Форматируем
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
            // Разрешаем: backspace, delete, tab, escape, enter
            if ([46, 8, 9, 27, 13].indexOf(e.keyCode) !== -1 ||
                // Разрешаем: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true) ||
                // Разрешаем: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                return;
            }
            // Запрещаем все, кроме цифр
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });

        // При фокусе: если пусто, начинаем ввод
        input.addEventListener('focus', function(e) {
            if (!e.target.value) {
                e.target.value = '';
            }
        });

        // При потере фокуса: если осталась только '+7', очищаем
        input.addEventListener('blur', function(e) {
            if (e.target.value === '+7' || e.target.value === '+7 (') {
                e.target.value = '';
            }
        });
    });
}

// Валидация формы регистрации
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

// Предпросмотр изображения при загрузке
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

// Подсветка текущей страницы в навигации
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.style.color = 'var(--color-yellow)';
            link.style.fontWeight = 'bold';
        }
    });
});
