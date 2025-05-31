def test_login(page):
    page.goto("https://example.com/login")
    page.fill("#username", "admin")
    page.fill("#password", "password123")
    page.click("#login-button")
    assert page.url == "https://example.com/dashboard"
    assert page.inner_text(".welcome-message") == "Добро пожаловать, admin!"