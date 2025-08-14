// 文件上传功能
document.addEventListener('DOMContentLoaded', function () {
  const uploadArea = document.getElementById('uploadArea');
  const fileInput = document.getElementById('fileInput');
  const uploadForm = document.getElementById('uploadForm');
  const uploadBtn = document.getElementById('uploadBtn');
  const fileInfo = document.getElementById('fileInfo');
  const fileName = document.getElementById('fileName');
  const fileSize = document.getElementById('fileSize');
  const fileType = document.getElementById('fileType');

  // 拖拽上传功能
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, unhighlight, false);
  });

  uploadArea.addEventListener('drop', handleDrop, false);
  uploadArea.addEventListener('click', () => fileInput.click());

  // 文件选择处理
  fileInput.addEventListener('change', function (e) {
    handleFiles(e.target.files);
  });

  // 表单提交处理
  uploadForm.addEventListener('submit', function (e) {
    e.preventDefault();
    if (fileInput.files.length > 0) {
      showUploadModal();
      // 模拟上传进度
      simulateUploadProgress();
      // 实际提交表单
      this.submit();
    }
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    uploadArea.classList.add('dragover');
  }

  function unhighlight() {
    uploadArea.classList.remove('dragover');
  }

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    if (files.length > 0) {
      const file = files[0];

      // 验证文件类型
      if (!isValidFileType(file)) {
        Utils.showError('请选择CSV文件（.csv 或 .txt）');
        return;
      }

      // 验证文件大小 (50MB)
      if (file.size > 50 * 1024 * 1024) {
        Utils.showError('文件大小不能超过50MB');
        return;
      }

      // 显示文件信息
      showFileInfo(file);

      // 启用上传按钮
      uploadBtn.disabled = false;
    }
  }

  function isValidFileType(file) {
    const allowedTypes = ['text/csv', 'text/plain', 'application/csv'];
    const allowedExtensions = ['.csv', '.txt'];

    const hasValidType = allowedTypes.includes(file.type);
    const hasValidExtension = allowedExtensions.some(ext =>
      file.name.toLowerCase().endsWith(ext)
    );

    return hasValidType || hasValidExtension;
  }

  function showFileInfo(file) {
    fileName.textContent = file.name;
    fileSize.textContent = Utils.formatFileSize(file.size);
    fileType.textContent = file.type || '未知';

    fileInfo.classList.remove('d-none');

    // 更新文件输入框
    const dt = new DataTransfer();
    dt.items.add(file);
    fileInput.files = dt.files;
  }

  function showUploadModal() {
    const modal = new bootstrap.Modal(document.getElementById('uploadModal'));
    modal.show();
  }

  function simulateUploadProgress() {
    const progressBar = document.getElementById('uploadProgress');
    let progress = 0;

    const interval = setInterval(() => {
      progress += Math.random() * 15;
      if (progress > 95) {
        progress = 95;
        clearInterval(interval);
      }
      progressBar.style.width = progress + '%';
    }, 200);
  }

  // 清除文件
  window.clearFile = function () {
    fileInput.value = '';
    fileInfo.classList.add('d-none');
    uploadBtn.disabled = true;
    unhighlight();
  };

  // 文件大小格式化（如果main.js中没有）
  if (!window.Utils) {
    window.Utils = {
      formatFileSize: function (bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
      },
      showError: function (message) {
        alert(message); // 简单实现，实际应该使用更好的通知系统
      }
    };
  }
});
