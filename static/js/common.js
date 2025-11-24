const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuBackdrop = document.getElementById('mobile-menu-backdrop');
const themeToggle = document.getElementById('theme-toggle');
const mobileThemeToggle = document.getElementById('mobile-theme-toggle');

// 主题切换功能
function toggleTheme() {
    document.documentElement.classList.toggle('dark');
    // 保存用户选择的偏好
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('vueuse-color-scheme', isDark ? 'dark' : 'light');
}

// 初始化主题
function initTheme() {
    const savedTheme = localStorage.getItem('vueuse-color-scheme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme) {
        document.documentElement.classList.toggle('dark', savedTheme === 'dark');
    } else {
        document.documentElement.classList.toggle('dark', prefersDark);
    }
}

// 初始加载主题
initTheme();

// 监听主题切换按钮
themeToggle.addEventListener('click', toggleTheme);
if (mobileThemeToggle) {
    mobileThemeToggle.addEventListener('click', toggleTheme);
}

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    mobileMenuBackdrop.classList.toggle('active');

    // 阻止页面滚动
    if (mobileMenu.classList.contains('active')) {
        document.body.style.overflow = 'hidden';
    } else {
        document.body.style.overflow = '';
    }
});

// 点击背景遮罩关闭菜单
mobileMenuBackdrop.addEventListener('click', () => {
    hamburger.classList.remove('active');
    mobileMenu.classList.remove('active');
    mobileMenuBackdrop.classList.remove('active');
    document.body.style.overflow = '';
});

// 点击关闭按钮关闭菜单
const closeMenuBtn = document.getElementById('close-menu-btn');
closeMenuBtn.addEventListener('click', () => {
    hamburger.classList.remove('active');
    mobileMenu.classList.remove('active');
    mobileMenuBackdrop.classList.remove('active');
    document.body.style.overflow = '';
});

// 点击菜单项后关闭菜单
document.querySelectorAll('.mobile-menu .nav-link, .mobile-menu .btn').forEach(item => {
    item.addEventListener('click', () => {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        mobileMenuBackdrop.classList.remove('active');
        document.body.style.overflow = '';
    });
});