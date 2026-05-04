// Мобильное меню (бургер)
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    const navigation = document.querySelector('.navigation');
    const menuOverlay = document.getElementById('menuOverlay');

    console.log('=== ОТЛАДКА МЕНЮ ===');
    console.log('navToggle:', navToggle);
    console.log('navigation:', navigation);
    console.log('menuOverlay:', menuOverlay);



    if (!navToggle) {
        console.error('Кнопка navToggle не найдена!');
        return;
    }
    if (!navigation) {
        console.error('Блок navigation не найден!');
        return;
    }

    function closeMenu() {
        console.log('Закрытие меню');
        navigation.classList.remove('active');
        navToggle.classList.remove('active');
        if (menuOverlay) menuOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    function openMenu() {
        console.log('Открытие меню');
        navigation.classList.add('active');
        navToggle.classList.add('active');
        if (menuOverlay) menuOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        console.log('Клик по бургеру');
        if (navigation.classList.contains('active')) {
            openMenu();
        } else {
            closeMenu();
        }
    });

    if (menuOverlay) {
        menuOverlay.addEventListener('click', function() {
            console.log('Клик по оверлею');
            openMenu();
        });
    }

    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            console.log('Клик по ссылке');
            openMenu();
        });
    });

    window.addEventListener('resize', function() {
        if (window.innerWidth > 900) {
            openMenu();
        }
    });

    // Инициализация маски телефона
    initPhoneMasks();

    // Автоматическое закрытие сообщений через 5 секунд
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

// Модальное окно заказа звонка
function openCallModal(serviceId = null) {
    const modal = document.getElementById('callModal');
    const serviceIdInput = document.getElementById('serviceId');

    if (serviceId) {
        serviceIdInput.value = serviceId;
    } else {
        serviceIdInput.value = '';
    }

    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeCallModal() {
    const modal = document.getElementById('callModal');
    modal.style.display = 'none';
    document.getElementById('callForm').reset();
    document.body.style.overflow = '';
}

// Модальное окно политики конфиденциальности
function openPrivacyModal() {
    const modal = document.getElementById('privacyModal');
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closePrivacyModal() {
    const modal = document.getElementById('privacyModal');
    modal.style.display = 'none';
    document.body.style.overflow = '';
}

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
            // Запрет копирования пароля
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
                // Проверка размера (5MB)
                if (file.size > 5 * 1024 * 1024) {
                    alert('Размер файла не должен превышать 5 МБ');
                    e.target.value = '';
                    return;
                }

                // Проверка формата
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

// Принудительная привязка меню (финальная версия)
(function() {
    function initMobileMenu() {
        const toggle = document.getElementById('navToggle');
        const nav = document.querySelector('.navigation');
        const overlay = document.getElementById('menuOverlay');

        if (!toggle || !nav) {
            console.log('Элементы меню не найдены');
            return;
        }

        console.log('Инициализация меню');

        // Функция закрытия
        function closeMenu() {
            nav.classList.remove('active');
            toggle.classList.remove('active');
            if (overlay) overlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        // Функция открытия
        function openMenu() {
            nav.classList.add('active');
            toggle.classList.add('active');
            if (overlay) overlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        // Обработчик клика по бургеру
        toggle.onclick = function(e) {
            e.stopPropagation();
            if (nav.classList.contains('active')) {
                closeMenu();
            } else {
                openMenu();
            }
        };

        // Закрытие по оверлею
        if (overlay) {
            overlay.onclick = closeMenu;
        }

        // Закрытие по ссылкам в меню
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.onclick = closeMenu;
        });

        // Закрытие при изменении размера окна
        window.onresize = function() {
            if (window.innerWidth > 768) {
                closeMenu();
            }
        };
    }

    // Запускаем после загрузки DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileMenu);
    } else {
        initMobileMenu();
    }
})();