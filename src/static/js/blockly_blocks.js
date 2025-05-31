// Кастомные блоки для TestMaster
Blockly.Blocks['testmaster_start'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Начало цепочки тестов");
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip("Начальная точка цепочки тестов");
  }
};

Blockly.Blocks['testmaster_ui_test'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("UI Тест")
        .appendField(new Blockly.FieldDropdown([
          ["Логин", "test_login"],
          ["Регистрация", "test_register"],
          ["Поиск", "test_search"]
        ]), "TEST_NAME");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(230);
    this.setTooltip("Выполнить UI тест");
  }
};

Blockly.Blocks['testmaster_api_test'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("API Тест")
        .appendField(new Blockly.FieldDropdown([
          ["Пользователи", "users"],
          ["Товары", "products"],
          ["Заказы", "orders"]
        ]), "ENDPOINT");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
    this.setTooltip("Выполнить API тест");
  }
};

Blockly.Blocks['testmaster_db_check'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Проверка БД")
        .appendField(new Blockly.FieldTextInput("SELECT * FROM users"), "QUERY");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip("Выполнить проверку в базе данных");
  }
};

Blockly.Blocks['testmaster_end'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Конец цепочки");
    this.setPreviousStatement(true, null);
    this.setColour(120);
    this.setTooltip("Конечная точка цепочки тестов");
  }
};

// Генерация кода для блоков
Blockly.JavaScript['testmaster_start'] = function(block) {
  return '// Начало цепочки тестов\n';
};

Blockly.JavaScript['testmaster_ui_test'] = function(block) {
  const testName = block.getFieldValue('TEST_NAME');
  return `tester.runTest('ui', '${testName}');\n`;
};

Blockly.JavaScript['testmaster_api_test'] = function(block) {
  const endpoint = block.getFieldValue('ENDPOINT');
  return `tester.runTest('api', '/api/${endpoint}');\n`;
};

Blockly.JavaScript['testmaster_db_check'] = function(block) {
  const query = block.getFieldValue('QUERY');
  return `tester.runTest('db', \`${query}\`);\n`;
};

Blockly.JavaScript['testmaster_end'] = function(block) {
  return '// Конец цепочки тестов\n';
};