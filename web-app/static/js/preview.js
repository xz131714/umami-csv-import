// 数据预览和配置功能
document.addEventListener('DOMContentLoaded', function () {
  const dbTypeSelect = document.getElementById('dbType');
  const mysqlConfig = document.getElementById('mysqlConfig');
  const postgresConfig = document.getElementById('postgresConfig');
  const testConnectionBtn = document.getElementById('testConnectionBtn');
  const startImportBtn = document.getElementById('startImportBtn');
  const configForm = document.getElementById('configForm');

  // 数据库类型切换
  dbTypeSelect.addEventListener('change', function () {
    const selectedType = this.value;

    // 隐藏所有配置
    document.querySelectorAll('.db-config').forEach(config => {
      config.classList.add('d-none');
    });

    // 显示选中的配置
    if (selectedType === 'mysql') {
      mysqlConfig.classList.remove('d-none');
    } else if (selectedType === 'postgres') {
      postgresConfig.classList.remove('d-none');
    }

    // 重置连接状态
    resetConnectionStatus();
  });

  // 测试数据库连接
  testConnectionBtn.addEventListener('click', function () {
    const dbType = dbTypeSelect.value;
    if (!dbType) {
      Utils.showWarning('请先选择数据库类型');
      return;
    }

    const dbConfig = getDbConfig(dbType);
    if (!dbConfig) {
      Utils.showError('请填写完整的数据库配置');
      return;
    }

    testDatabaseConnection(dbType, dbConfig);
  });

  // 配置表单提交
  configForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const dbType = dbTypeSelect.value;
    const dbConfig = getDbConfig(dbType);
    const websiteId = document.getElementById('websiteId').value.trim();
    const clearTables = document.getElementById('clearTables').checked;

    if (!dbType || !dbConfig || !websiteId) {
      Utils.showError('请填写完整的配置信息');
      return;
    }

    if (!isValidUUID(websiteId)) {
      Utils.showError('Website ID格式不正确，应为UUID格式');
      return;
    }

    // 确认导入
    const confirmMessage = clearTables ?
      '确定要开始导入数据吗？\n⚠️ 此操作将清空目标表中的所有数据！' :
      '确定要开始导入数据吗？';

    if (!confirm(confirmMessage)) {
      return;
    }

    startDataImport({
      db_type: dbType,
      db_config: dbConfig,
      website_id: websiteId,
      clear_tables: clearTables,
      file_path: fileInfo.filepath
    });
  });

  function getDbConfig(dbType) {
    if (dbType === 'mysql') {
      const host = document.getElementById('mysqlHost').value.trim();
      const port = parseInt(document.getElementById('mysqlPort').value);
      const user = document.getElementById('mysqlUser').value.trim();
      const password = document.getElementById('mysqlPassword').value;
      const database = document.getElementById('mysqlDatabase').value.trim();

      if (!host || !port || !user || !password || !database) {
        return null;
      }

      return { host, port, user, password, database };
    } else if (dbType === 'postgres') {
      const host = document.getElementById('pgHost').value.trim();
      const port = parseInt(document.getElementById('pgPort').value);
      const user = document.getElementById('pgUser').value.trim();
      const password = document.getElementById('pgPassword').value;
      const database = document.getElementById('pgDatabase').value.trim();

      if (!host || !port || !user || !password || !database) {
        return null;
      }

      return { host, port, user, password, database };
    }
    return null;
  }

  function testDatabaseConnection(dbType, dbConfig) {
    // 更新按钮状态
    const originalText = testConnectionBtn.innerHTML;
    testConnectionBtn.disabled = true;
    testConnectionBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>测试中...';

    fetch('/test-db', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        db_type: dbType,
        db_config: dbConfig
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          Utils.showSuccess('数据库连接成功！');
          startImportBtn.disabled = false;
          testConnectionBtn.classList.remove('btn-outline-primary');
          testConnectionBtn.classList.add('btn-success');
          testConnectionBtn.innerHTML = '<i class="fas fa-check me-2"></i>连接成功';
        } else {
          Utils.showError('数据库连接失败: ' + data.message);
          resetConnectionStatus();
        }
      })
      .catch(error => {
        Utils.showError('连接测试出错: ' + error.message);
        resetConnectionStatus();
      })
      .finally(() => {
        if (testConnectionBtn.classList.contains('btn-outline-primary')) {
          testConnectionBtn.disabled = false;
          testConnectionBtn.innerHTML = originalText;
        }
      });
  }

  function startDataImport(config) {
    // 显示导入模态框
    const modal = new bootstrap.Modal(document.getElementById('importModal'));
    modal.show();

    // 更新进度
    updateImportProgress(0, '正在连接数据库...');

    fetch('/import', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ config })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          updateImportProgress(100, '数据导入完成！');
          showImportResults(data.results);
          document.getElementById('closeBtn').disabled = false;
          Utils.showSuccess('数据导入成功完成！');
        } else {
          updateImportProgress(0, '导入失败: ' + data.message);
          document.getElementById('closeBtn').disabled = false;
          Utils.showError('导入失败: ' + data.message);
        }
      })
      .catch(error => {
        updateImportProgress(0, '导入出错: ' + error.message);
        document.getElementById('closeBtn').disabled = false;
        Utils.showError('导入出错: ' + error.message);
      });
  }

  function updateImportProgress(percentage, message) {
    const progressBar = document.getElementById('progressBar');
    const importStatus = document.getElementById('importStatus');

    progressBar.style.width = percentage + '%';
    progressBar.textContent = percentage + '%';

    if (importStatus) {
      importStatus.innerHTML = '<p class="mb-0">' + message + '</p>';
    }
  }

  function showImportResults(results) {
    const importStatus = document.getElementById('importStatus');
    let html = '<h6>导入结果详情:</h6><div class="row">';

    for (const [table, result] of Object.entries(results)) {
      const statusClass = result.success ? 'text-success' : 'text-danger';
      const icon = result.success ? 'fas fa-check-circle' : 'fas fa-times-circle';

      html += `
                <div class="col-md-6 mb-2">
                    <div class="border rounded p-2">
                        <h6 class="${statusClass}">
                            <i class="${icon} me-2"></i>${table}
                        </h6>
                        ${result.success ?
          `<small>处理行数: ${result.processed_rows}<br>匹配字段: ${result.columns.length}</small>` :
          `<small class="text-danger">${result.message}</small>`
        }
                    </div>
                </div>
            `;
    }

    html += '</div>';
    importStatus.innerHTML = html;
  }

  function resetConnectionStatus() {
    startImportBtn.disabled = true;
    testConnectionBtn.disabled = false;
    testConnectionBtn.classList.remove('btn-success');
    testConnectionBtn.classList.add('btn-outline-primary');
    testConnectionBtn.innerHTML = '<i class="fas fa-plug me-2"></i>测试数据库连接';
  }

  function isValidUUID(uuid) {
    const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    return uuidRegex.test(uuid);
  }

  // 为了兼容性，确保Utils存在
  if (!window.Utils) {
    window.Utils = {
      showSuccess: function (msg) { alert('成功: ' + msg); },
      showError: function (msg) { alert('错误: ' + msg); },
      showWarning: function (msg) { alert('警告: ' + msg); }
    };
  }
});
