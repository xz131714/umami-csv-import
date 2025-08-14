// 主要JavaScript功能
document.addEventListener('DOMContentLoaded', function () {
  // 初始化工具提示
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // 平滑滚动
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });

  // 页面加载动画
  const cards = document.querySelectorAll('.card');
  cards.forEach((card, index) => {
    card.style.animationDelay = `${index * 0.1}s`;
  });
});

// 通用工具函数
const Utils = {
  // 显示成功消息
  showSuccess: function (message) {
    this.showAlert(message, 'success');
  },

  // 显示错误消息
  showError: function (message) {
    this.showAlert(message, 'danger');
  },

  // 显示警告消息
  showWarning: function (message) {
    this.showAlert(message, 'warning');
  },

  // 显示信息消息
  showInfo: function (message) {
    this.showAlert(message, 'info');
  },

  // 显示警告框
  showAlert: function (message, type) {
    const alertContainer = document.getElementById('alertContainer') || this.createAlertContainer();

    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

    alertContainer.appendChild(alertDiv);

    // 自动隐藏
    setTimeout(() => {
      alertDiv.remove();
    }, 5000);
  },

  // 创建警告容器
  createAlertContainer: function () {
    const container = document.createElement('div');
    container.id = 'alertContainer';
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '9999';
    container.style.minWidth = '300px';
    document.body.appendChild(container);
    return container;
  },

  // 格式化文件大小
  formatFileSize: function (bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  },

  // 验证邮箱格式
  isValidEmail: function (email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  },

  // 防抖函数
  debounce: function (func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  },

  // 节流函数
  throttle: function (func, limit) {
    let inThrottle;
    return function () {
      const args = arguments;
      const context = this;
      if (!inThrottle) {
        func.apply(context, args);
        inThrottle = true;
        setTimeout(() => inThrottle = false, limit);
      }
    };
  },

  // 复制到剪贴板
  copyToClipboard: function (text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        this.showSuccess('已复制到剪贴板');
      }).catch(() => {
        this.fallbackCopyTextToClipboard(text);
      });
    } else {
      this.fallbackCopyTextToClipboard(text);
    }
  },

  // 备用复制方法
  fallbackCopyTextToClipboard: function (text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
      this.showSuccess('已复制到剪贴板');
    } catch (err) {
      this.showError('复制失败');
    }
    document.body.removeChild(textArea);
  }
};

// 全局变量
window.Utils = Utils;
