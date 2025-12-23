// Инициализация Telegram WebApp
let tg = window.Telegram?.WebApp;

// Ссылка на Telegram канал
const TELEGRAM_LINK = "https://t.me/+b-pai-JnyCc1MGYy";
const INVITE_CODE = "b-pai-JnyCc1MGYy";

// Функция для открытия ссылки в нативном приложении Telegram
// Для платных каналов с оплатой звездами нужно использовать https://t.me/ формат через openTelegramLink
function openTelegramChannel() {
    // Если в Telegram WebApp, используем openTelegramLink с прямой https://t.me/ ссылкой
    // Это откроет канал в нативном приложении с поддержкой оплаты звездами
    if (tg) {
        if (tg.openTelegramLink) {
            // openTelegramLink с https://t.me/ ссылкой открывает в нативном приложении и поддерживает оплату звездами
            // Важно: используем прямую https://t.me/ ссылку, не tg:// протокол
            tg.openTelegramLink(TELEGRAM_LINK);
            return;
        } else if (tg.openLink) {
            // Fallback: используем openLink, но это может открыть в браузере
            // Для платных каналов лучше использовать openTelegramLink
            tg.openLink(TELEGRAM_LINK);
            return;
        }
    }
    
    // Если WebApp API недоступен, пробуем открыть через tg:// протокол
    // Но для платных каналов это может не работать правильно
    const tgProtocol = `tg://join?invite=${INVITE_CODE}`;
    
    // Определяем, мобильное ли устройство
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    if (isMobile) {
        try {
            // Пытаемся открыть через протокол (для мобильных)
            window.location.href = tgProtocol;
        } catch(e) {
            // Если не сработало, пробуем через iframe
            const iframe = document.createElement('iframe');
            iframe.style.display = 'none';
            iframe.src = tgProtocol;
            document.body.appendChild(iframe);
            setTimeout(() => {
                if (iframe.parentNode) {
                    document.body.removeChild(iframe);
                }
            }, 1000);
        }
    } else {
        // Для десктопа открываем обычную ссылку
        window.open(TELEGRAM_LINK, '_blank');
    }
}

// Инициализация WebApp
function initTelegramWebApp() {
    // Проверяем наличие Telegram WebApp
    if (window.Telegram && window.Telegram.WebApp) {
        tg = window.Telegram.WebApp;
        
        // Инициализируем WebApp
        tg.ready();
        tg.expand();
        
        // Настраиваем цвета под тему Telegram
        tg.setHeaderColor('#000000');
        tg.setBackgroundColor('#000000');
        
        return true;
    }
    return false;
}

// Инициализируем сразу
const isTelegram = initTelegramWebApp();

// Обработчик кнопки подписки
document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('subscribe-button');
    
    if (button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Открываем канал в нативном приложении Telegram через tg:// протокол
            openTelegramChannel();
            
            // Анимация клика
            createClickParticles(button);
        });
        
        // Эффект при наведении (для десктопа)
        button.addEventListener('mouseenter', function() {
            createParticles(button);
        });
        
        // Для мобильных - touchstart
        button.addEventListener('touchstart', function(e) {
            e.preventDefault();
            createParticles(button);
        }, { passive: false });
    }
    
    // Настраиваем MainButton в Telegram (только если в Telegram)
    if (tg && tg.MainButton) {
        tg.MainButton.setText('Подписаться');
        tg.MainButton.show();
        tg.MainButton.onClick(function() {
            openTelegramChannel();
        });
    }
    
    // Плавное появление элементов
    const elements = document.querySelectorAll('.content > *');
    elements.forEach((el, index) => {
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.animation = `fadeInUp 0.8s ease-out forwards`;
        }, index * 200);
    });
});

function createParticles(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    for (let i = 0; i < 8; i++) {
        const particle = document.createElement('div');
        particle.className = 'click-particle';
        particle.style.cssText = `
            position: fixed;
            left: ${centerX}px;
            top: ${centerY}px;
            width: 6px;
            height: 6px;
            background: #a855f7;
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            box-shadow: 0 0 15px rgba(168, 85, 247, 0.8);
        `;
        
        const angle = (Math.PI * 2 * i) / 8;
        const distance = 50 + Math.random() * 30;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        
        document.body.appendChild(particle);
        
        particle.animate([
            { transform: 'translate(0, 0) scale(1)', opacity: 1 },
            { transform: `translate(${x}px, ${y}px) scale(0)`, opacity: 0 }
        ], {
            duration: 800,
            easing: 'ease-out'
        }).onfinish = () => particle.remove();
    }
}

function createClickParticles(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    
    for (let i = 0; i < 15; i++) {
        const particle = document.createElement('div');
        particle.className = 'click-particle';
        particle.style.cssText = `
            position: fixed;
            left: ${centerX}px;
            top: ${centerY}px;
            width: ${4 + Math.random() * 4}px;
            height: ${4 + Math.random() * 4}px;
            background: ${i % 2 === 0 ? '#a855f7' : '#8b5cf6'};
            border-radius: 50%;
            pointer-events: none;
            z-index: 1000;
            box-shadow: 0 0 20px rgba(168, 85, 247, 1);
        `;
        
        const angle = Math.random() * Math.PI * 2;
        const distance = 80 + Math.random() * 50;
        const x = Math.cos(angle) * distance;
        const y = Math.sin(angle) * distance;
        
        document.body.appendChild(particle);
        
        particle.animate([
            { transform: 'translate(0, 0) scale(1)', opacity: 1 },
            { transform: `translate(${x}px, ${y}px) scale(0)`, opacity: 0 }
        ], {
            duration: 1000 + Math.random() * 500,
            easing: 'ease-out'
        }).onfinish = () => particle.remove();
    }
    
    // Создаем волну
    const wave = document.createElement('div');
    wave.style.cssText = `
        position: fixed;
        left: ${centerX}px;
        top: ${centerY}px;
        width: 0;
        height: 0;
        border: 2px solid rgba(168, 85, 247, 0.6);
        border-radius: 50%;
        pointer-events: none;
        z-index: 999;
        transform: translate(-50%, -50%);
    `;
    
    document.body.appendChild(wave);
    
    wave.animate([
        { width: '0', height: '0', opacity: 1 },
        { width: '200px', height: '200px', opacity: 0 }
    ], {
        duration: 600,
        easing: 'ease-out'
    }).onfinish = () => wave.remove();
}
