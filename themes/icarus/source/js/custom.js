console.log('Khan的博客...');

(function() {
    /**
     * Icarus 夜间模式 by iMaeGoo
     * https://www.imaegoo.com/
     */ 
    var isNight = localStorage.getItem('night');
    var nightNav;
  
    function applyNight(value) {
        if (value.toString() === 'true') {
            document.body.classList.remove('light');
            document.body.classList.add('night');
            // 选择 <meta name="theme-color"> 标签
            var metaTag = document.querySelector('meta[name="theme-color"]');
            // 修改 meta 标签的 content 属性
            metaTag.setAttribute('content', '#282c34');  // 将主题颜色设置为暗色
            VANTA.DOTS({
                el: "#vantajs",
                mouseControls: false,
                touchControls: false,
                gyroControls: false,
                minHeight: 200.00,
                minWidth: 200.00,
                scale: 1.00,
                scaleMobile: 1.00,
                color: 0x3273dc,
                color2: 0x3273dc,
                backgroundColor: 0x0e1225,
                showLines: false
            });
        } else {
            document.body.classList.remove('night');
            document.body.classList.add('light');
            // 选择 <meta name="theme-color"> 标签
            var metaTag = document.querySelector('meta[name="theme-color"]');
            // 修改 meta 标签的 content 属性
            metaTag.setAttribute('content', '#ffffff');  // 将主题颜色设置为亮色
            VANTA.DOTS({
                el: "#vantajs",
                mouseControls: false,
                touchControls: false,
                gyroControls: false,
                minHeight: 200.00,
                minWidth: 200.00,
                scale: 1.00,
                scaleMobile: 1.00,
                color: 0xc0c0c0,
                color2: 0xc0c0c0,
                backgroundColor: 0xf5f5fa,
                showLines: false
            });
        }
    }
  
    function findNightNav() {
        nightNav = document.getElementById('night-nav');
        if (!nightNav) {
            setTimeout(findNightNav, 100);
        } else {
            nightNav.addEventListener('click', switchNight);
        }
    }
  
    function switchNight() {
        isNight = isNight ? isNight.toString() !== 'true' : true;
        applyNight(isNight);
        localStorage.setItem('night', isNight);
    }
  
    findNightNav();
    isNight && applyNight(isNight);
  }());